# Creating City Maps to svg which can be edited in Fusion and ready for 3d printing

Generate beautiful, minimalist map posters for any city and export them as **SVG files** ready for import into Fusion for 3D printing.

## Features

- Generate maps for any city in the world
- Export as **SVG** (perfect for Fusion 360) or PNG
- Multiple themes available
- Customizable map radius
- Based on OpenStreetMap data

## Installation

1. Install Python 3.8+ if you haven't already

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Generate an SVG map for Fusion 360:

```bash
python create_map_poster.py -c "San Francisco" -C "USA" -t feature_based -d 10000
```

This creates an SVG file in the `posters/` directory.

### Import into Fusion 360:

1. Open Fusion 360
2. Create a new design
3. Go to **Insert** → **Insert SVG**
4. Select your generated SVG file
5. Position and scale as needed
6. **Extrude** the paths to create 3D geometry:
   - Select the sketch
   - Use **Extrude** command
   - Set your desired height (e.g., 2-5mm for roads)
   - For multiple layers, you can create separate extrusions with different heights:
     - Motorways: 3mm
     - Primary roads: 2.5mm
     - Secondary roads: 2mm
     - Residential roads: 1.5mm
7. Export as STL for 3D printing

### Workflow Tips for 3D Printing:

1. **Import SVG as sketch** - The SVG imports as vector paths, making it easy to edit
2. **Clean up if needed** - Remove or simplify any paths that are too complex
3. **Create separate extrusions** - Different road types can have different heights
4. **Add a base** - Create a solid base (2-3mm thick) under the roads
5. **Scale appropriately** - MapToPoster uses meters; scale to your print size
   - Example: 10000m radius → 200mm print (1:50 scale)
6. **Export STL** - Use Fusion 360's **Make** → **3D Print** to export STL

## Usage

```bash
python create_map_poster.py -c "City Name" [OPTIONS]
```

### Arguments

- `-c, --city` (required): City name
- `-C, --country`: Country name (helps with geocoding)
- `-t, --theme`: Theme name (default: `feature_based`)
- `-d, --distance`: Radius in meters (default: 10000)
- `-f, --format`: Output format - `svg` (default, for Fusion 360) or `png`
- `--dpi`: DPI for PNG output (default: 300)
- `--list-themes`: List all available themes

### Examples

```bash
# Generate SVG for San Francisco
python create_map_poster.py -c "San Francisco" -C "USA" -t feature_based -d 10000

# Generate SVG for Barcelona with noir theme
python create_map_poster.py -c "Barcelona" -C "Spain" -t noir -d 8000

# Generate PNG instead
python create_map_poster.py -c "Tokyo" -C "Japan" -f png -d 15000

# List available themes
python create_map_poster.py --list-themes
```

## Themes

Themes define colors and styling. Available themes:

- `feature_based` - Classic black & white with road hierarchy
- `noir` - Pure black background, white roads

More themes can be added in the `themes/` directory. See existing theme files for format.

## Output

Files are saved to `posters/` directory with format:
```
{city}_{theme}_{YYYYMMDD_HHMMSS}.svg
```

## Fusion 360 Import Settings

When importing SVG into Fusion 360:

1. **Units**: Check that units match (the SVG uses points, scale as needed)
2. **Origin**: Place at origin (0,0) for easier manipulation
3. **Scale**: Consider your print size vs. actual map distance
4. **Grouping**: Roads may import as separate paths - you can combine or extrude separately

## Distance Guide

| Distance     | Best for                                           |
| ------------ | -------------------------------------------------- |
| 4000-6000m   | Small/dense cities (Venice, Amsterdam center)      |
| 8000-12000m  | Medium cities, focused downtown (Paris, Barcelona) |
| 15000-20000m | Large metros, full city view (Tokyo, Mumbai)       |

## 3D Printing Tips

1. **Thickness**: Roads should be at least 0.5mm thick for printing
2. **Base**: Add a 2-3mm base layer for stability
3. **Supports**: Usually not needed for map prints (they're relatively flat)
4. **Orientation**: Print with roads facing up for best detail
5. **Material**: PLA works well; consider color contrast (white/black PLA)

## Project Structure

```
.
├── create_map_poster.py  # Main script
├── requirements.txt       # Python dependencies
├── themes/               # Theme JSON files
├── posters/              # Generated outputs
└── README.md
```

## License

MIT License - Based on [originalankur/maptoposter](https://github.com/originalankur/maptoposter)

## Credits

- OpenStreetMap contributors
- OSMnx library
- Original MapToPoster project
