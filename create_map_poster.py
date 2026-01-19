#!/usr/bin/env python3
"""
City Map Poster Generator - Modified for Fusion 360 / 3D Printing
Generates SVG output suitable for CAD import and 3D printing
Based on https://github.com/originalankur/maptoposter
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

# Set matplotlib backend before importing pyplot
import matplotlib
matplotlib.use('Agg')  # Use Agg backend (works for both SVG and PNG)

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
from geopy.geocoders import Nominatim

# Configure OSMnx
ox.settings.log_console = True
ox.settings.use_cache = True

THEMES_DIR = Path(__file__).parent / "themes"
POSTERS_DIR = Path(__file__).parent / "posters"
FONTS_DIR = Path(__file__).parent / "fonts"


def load_theme(theme_name: str) -> dict:
    """Load theme from JSON file."""
    theme_path = THEMES_DIR / f"{theme_name}.json"
    
    if not theme_path.exists():
        print(f"Theme '{theme_name}' not found. Using default theme.")
        return get_default_theme()
    
    with open(theme_path, 'r') as f:
        theme = json.load(f)
    
    # Set defaults for missing keys
    defaults = get_default_theme()
    for key, value in defaults.items():
        if key not in theme:
            theme[key] = value
    
    return theme


def get_default_theme() -> dict:
    """Return default theme configuration."""
    return {
        "name": "Default",
        "description": "Default theme",
        "bg": "#FFFFFF",
        "text": "#000000",
        "gradient_color": "#FFFFFF",
        "water": "#C0C0C0",
        "parks": "#F0F0F0",
        "coastline": "#000000",
        "road_motorway": "#0A0A0A",
        "road_primary": "#1A1A1A",
        "road_secondary": "#2A2A2A",
        "road_tertiary": "#3A3A3A",
        "road_residential": "#4A4A4A",
        "road_default": "#3A3A3A"
    }


def get_coordinates(city: str, country: str = None) -> tuple:
    """Get coordinates for a city using Nominatim."""
    geolocator = Nominatim(user_agent="map_poster_generator")
    
    query = city
    if country:
        query = f"{city}, {country}"
    
    print(f"Geocoding: {query}")
    location = geolocator.geocode(query)
    
    if not location:
        raise ValueError(f"Could not find coordinates for {query}")
    
    return (location.latitude, location.longitude)


def get_edge_colors_by_type(edges: gpd.GeoDataFrame, theme: dict) -> list:
    """Get road colors based on highway type."""
    colors = []
    for _, edge in edges.iterrows():
        highway = edge.get('highway', 'default')
        if isinstance(highway, list):
            highway = highway[0] if highway else 'default'
        
        if 'motorway' in str(highway):
            colors.append(theme['road_motorway'])
        elif highway in ['trunk', 'primary']:
            colors.append(theme['road_primary'])
        elif highway == 'secondary':
            colors.append(theme['road_secondary'])
        elif highway == 'tertiary':
            colors.append(theme['road_tertiary'])
        elif highway in ['residential', 'living_street', 'unclassified']:
            colors.append(theme['road_residential'])
        else:
            colors.append(theme['road_default'])
    
    return colors


def get_edge_widths_by_type(edges: gpd.GeoDataFrame) -> list:
    """Get road widths based on highway type."""
    widths = []
    for _, edge in edges.iterrows():
        highway = edge.get('highway', 'default')
        if isinstance(highway, list):
            highway = highway[0] if highway else 'default'
        
        if 'motorway' in str(highway):
            widths.append(1.2)
        elif highway in ['trunk', 'primary']:
            widths.append(1.0)
        elif highway == 'secondary':
            widths.append(0.8)
        elif highway == 'tertiary':
            widths.append(0.6)
        else:
            widths.append(0.4)
    
    return widths


def create_poster(city: str, country: str = None, theme_name: str = "feature_based", 
                  distance: int = 10000, output_format: str = "svg", dpi: int = 300):
    """Create a map poster for the given city."""
    
    # Load theme
    theme = load_theme(theme_name)
    print(f"Using theme: {theme.get('name', theme_name)}")
    
    # Get coordinates
    lat, lon = get_coordinates(city, country)
    point = (lat, lon)
    print(f"Coordinates: {lat}, {lon}")
    
    # Fetch road network
    print(f"Fetching road network (radius: {distance}m)...")
    G = ox.graph_from_point(point, dist=distance, network_type='drive')
    
    # Convert to GeoDataFrame
    nodes, edges = ox.graph_to_gdfs(G)
    
    # Fetch water bodies
    print("Fetching water bodies...")
    try:
        water = ox.features_from_point(point, tags={'natural': 'water'}, dist=distance)
    except:
        water = None
    
    # Fetch parks
    print("Fetching parks...")
    try:
        parks = ox.features_from_point(point, tags={'leisure': 'park'}, dist=distance)
    except:
        parks = None
    
    # Fetch coastline/boundary
    print("Fetching coastline/boundary...")
    coastline = None
    try:
        # Try to fetch coastline data (coastlines are typically LineString ways in OSM)
        # Use a larger distance to ensure we get the full coastline
        coastline = ox.features_from_point(point, tags={'natural': 'coastline'}, dist=distance * 1.5)
        if coastline.empty:
            coastline = None
            print("  No coastline data found, trying alternative methods...")
    except Exception as e:
        print(f"  Coastline fetch error: {e}")
        coastline = None
    
    # If no coastline found, try getting boundaries or water edges
    if coastline is None or (hasattr(coastline, 'empty') and coastline.empty):
        try:
            # Try getting water polygons and use their boundaries
            if water is not None and not water.empty:
                print("  Using water body boundaries as coastline...")
                coastline = water
        except:
            coastline = None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), facecolor=theme['bg'])
    ax.set_facecolor(theme['bg'])
    
    # Plot water
    if water is not None and not water.empty:
        water.plot(ax=ax, color=theme['water'], edgecolor='none', zorder=1)
    
    # Plot parks
    if parks is not None and not parks.empty:
        parks.plot(ax=ax, color=theme['parks'], edgecolor='none', zorder=2)
    
    # Plot coastline/boundary (before roads so roads appear on top)
    coastline_color = theme.get('coastline', theme['text'])
    coastline_plotted = False
    
    if coastline is not None and not coastline.empty:
        print("Rendering coastline/boundary...")
        # Plot coastline as a visible border
        for idx, feature in coastline.iterrows():
            geom = feature.geometry
            if geom is not None:
                if geom.geom_type == 'LineString':
                    coords = list(geom.coords)
                    x_coords = [coord[0] for coord in coords]
                    y_coords = [coord[1] for coord in coords]
                    ax.plot(x_coords, y_coords, color=coastline_color, linewidth=2.5, 
                           solid_capstyle='round', zorder=2.5)
                    coastline_plotted = True
                elif geom.geom_type == 'MultiLineString':
                    for line in geom.geoms:
                        coords = list(line.coords)
                        x_coords = [coord[0] for coord in coords]
                        y_coords = [coord[1] for coord in coords]
                        ax.plot(x_coords, y_coords, color=coastline_color, linewidth=2.5, 
                               solid_capstyle='round', zorder=2.5)
                        coastline_plotted = True
                elif geom.geom_type == 'Polygon':
                    # For polygons (water bodies), plot the exterior boundary
                    exterior = geom.exterior
                    coords = list(exterior.coords)
                    x_coords = [coord[0] for coord in coords]
                    y_coords = [coord[1] for coord in coords]
                    ax.plot(x_coords, y_coords, color=coastline_color, linewidth=2.5, 
                           solid_capstyle='round', zorder=2.5)
                    coastline_plotted = True
                elif geom.geom_type == 'MultiPolygon':
                    # For MultiPolygons, plot each exterior boundary
                    for poly in geom.geoms:
                        exterior = poly.exterior
                        coords = list(exterior.coords)
                        x_coords = [coord[0] for coord in coords]
                        y_coords = [coord[1] for coord in coords]
                        ax.plot(x_coords, y_coords, color=coastline_color, linewidth=2.5, 
                               solid_capstyle='round', zorder=2.5)
                        coastline_plotted = True
    
    # If coastline wasn't found from coastline tag, try using water body edges
    if not coastline_plotted and water is not None and not water.empty:
        print("Rendering water body boundaries as coastline...")
        for idx, feature in water.iterrows():
            geom = feature.geometry
            if geom is not None:
                if geom.geom_type == 'Polygon':
                    exterior = geom.exterior
                    coords = list(exterior.coords)
                    x_coords = [coord[0] for coord in coords]
                    y_coords = [coord[1] for coord in coords]
                    ax.plot(x_coords, y_coords, color=coastline_color, linewidth=2.5, 
                           solid_capstyle='round', zorder=2.5)
                elif geom.geom_type == 'MultiPolygon':
                    for poly in geom.geoms:
                        exterior = poly.exterior
                        coords = list(exterior.coords)
                        x_coords = [coord[0] for coord in coords]
                        y_coords = [coord[1] for coord in coords]
                        ax.plot(x_coords, y_coords, color=coastline_color, linewidth=2.5, 
                               solid_capstyle='round', zorder=2.5)
    
    # Get edge colors and widths
    edge_colors = get_edge_colors_by_type(edges, theme)
    edge_widths = get_edge_widths_by_type(edges)
    
    # Plot roads
    print("Rendering roads...")
    # Plot roads by iterating through edges and drawing them individually
    # This gives us better control over zorder for SVG output
    for i, (idx, edge) in enumerate(edges.iterrows()):
        color = edge_colors[i] if i < len(edge_colors) else theme['road_default']
        width = edge_widths[i] if i < len(edge_widths) else 0.4
        geom = edge.geometry
        if geom is not None:
            if geom.geom_type == 'LineString':
                coords = list(geom.coords)
                x_coords = [coord[0] for coord in coords]
                y_coords = [coord[1] for coord in coords]
                ax.plot(x_coords, y_coords, color=color, linewidth=width, 
                       solid_capstyle='round', zorder=3)
            elif geom.geom_type == 'MultiLineString':
                for line in geom.geoms:
                    coords = list(line.coords)
                    x_coords = [coord[0] for coord in coords]
                    y_coords = [coord[1] for coord in coords]
                    ax.plot(x_coords, y_coords, color=color, linewidth=width, 
                           solid_capstyle='round', zorder=3)
    
    # Remove axes
    ax.axis('off')
    ax.set_aspect('equal')
    
    # Add text labels
    city_label = city.upper()
    country_label = country.upper() if country else ""
    coord_label = f"{lat:.4f}°N, {abs(lon):.4f}°{'W' if lon < 0 else 'E'}"
    
    # City name (spaced letters)
    for i, letter in enumerate(city_label):
        x_pos = 0.05 + (i * 0.06)
        ax.text(x_pos, 0.14, letter, transform=ax.transAxes, 
                fontsize=24, fontweight='bold', color=theme['text'],
                family='sans-serif', va='bottom')
    
    # Decorative line
    ax.add_patch(mpatches.Rectangle((0.05, 0.125), 0.15, 0.003, 
                                    transform=ax.transAxes, 
                                    facecolor=theme['text'], edgecolor='none'))
    
    # Country name
    if country_label:
        ax.text(0.05, 0.10, country_label, transform=ax.transAxes,
                fontsize=14, color=theme['text'], family='sans-serif', va='bottom')
    
    # Coordinates
    ax.text(0.05, 0.07, coord_label, transform=ax.transAxes,
            fontsize=10, color=theme['text'], family='sans-serif', va='bottom')
    
    # Attribution
    ax.text(0.98, 0.02, "© OpenStreetMap contributors", transform=ax.transAxes,
            fontsize=8, color=theme['text'], family='sans-serif', 
            ha='right', va='bottom', alpha=0.6)
    
    # Save output
    POSTERS_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    city_safe = city.lower().replace(' ', '_')
    theme_safe = theme_name.lower()
    
    if output_format.lower() == "svg":
        output_file = POSTERS_DIR / f"{city_safe}_{theme_safe}_{timestamp}.svg"
        plt.savefig(output_file, format='svg', bbox_inches='tight', 
                   facecolor=theme['bg'], edgecolor='none', dpi=dpi)
        print(f"\n✓ SVG saved: {output_file}")
        print(f"  Import this file into Fusion 360 as a sketch to extrude for 3D printing")
    else:
        output_file = POSTERS_DIR / f"{city_safe}_{theme_safe}_{timestamp}.png"
        plt.savefig(output_file, format='png', bbox_inches='tight', 
                   facecolor=theme['bg'], edgecolor='none', dpi=dpi)
        print(f"\n✓ PNG saved: {output_file}")
    
    plt.close()
    
    return output_file


def list_themes():
    """List all available themes."""
    themes = []
    if THEMES_DIR.exists():
        for theme_file in THEMES_DIR.glob("*.json"):
            with open(theme_file, 'r') as f:
                theme = json.load(f)
                themes.append({
                    'name': theme_file.stem,
                    'display': theme.get('name', theme_file.stem),
                    'description': theme.get('description', '')
                })
    
    if themes:
        print("\nAvailable themes:")
        for theme in sorted(themes, key=lambda x: x['name']):
            print(f"  {theme['name']:20s} - {theme['display']}")
            if theme['description']:
                print(f"    {theme['description']}")
    else:
        print("No themes found. Using default theme.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate beautiful map posters for any city",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-c', '--city', required=True, help='City name')
    parser.add_argument('-C', '--country', help='Country name (optional)')
    parser.add_argument('-t', '--theme', default='feature_based', help='Theme name (default: feature_based)')
    parser.add_argument('-d', '--distance', type=int, default=10000, 
                       help='Radius in meters (default: 10000)')
    parser.add_argument('-f', '--format', choices=['svg', 'png'], default='svg',
                       help='Output format: svg (for Fusion 360) or png (default: svg)')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for PNG output (default: 300)')
    parser.add_argument('--list-themes', action='store_true', help='List available themes')
    
    args = parser.parse_args()
    
    if args.list_themes:
        list_themes()
        return
    
    try:
        create_poster(args.city, args.country, args.theme, args.distance, 
                     args.format, args.dpi)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
