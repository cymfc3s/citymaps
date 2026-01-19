# Quick Start: Generate Map → Fusion 360 → 3D Print

## Step 1: Install Dependencies

First, make sure Python is installed (with pip). Then install required packages:

```powershell
pip install -r requirements.txt
```

This installs: osmnx, geopandas, matplotlib, geopy, numpy, shapely

## Step 2: Generate Your Map

Run the map generator script:

```powershell
python create_map_poster.py -c "San Francisco" -C "USA" -t feature_based -d 10000 -f svg
```

**Parameters explained:**
- `-c "San Francisco"` - City name
- `-C "USA"` - Country (optional but helps with accuracy)
- `-t feature_based` - Theme (options: feature_based, noir, blueprint, sunset)
- `-d 10000` - Radius in meters (5000-20000 recommended)
- `-f svg` - Output format (svg for Fusion 360, or png)

**Output:** File saved to `posters/` folder:
```
posters/san_francisco_feature_based_20260108_120000.svg
```

### Example Commands

```powershell
# Small city (6km radius)
python create_map_poster.py -c "Venice" -C "Italy" -t blueprint -d 4000 -f svg

# Medium city (10km radius)
python create_map_poster.py -c "Barcelona" -C "Spain" -t noir -d 8000 -f svg

# Large city (15km radius)
python create_map_poster.py -c "Tokyo" -C "Japan" -t feature_based -d 15000 -f svg
```

## Step 3: Import into Fusion 360

1. **Open Fusion 360** and create a new design

2. **Insert SVG:**
   - Go to **Insert** → **Insert SVG**
   - Browse to `posters/` folder
   - Select your generated `.svg` file
   - Choose a plane (Top is recommended)

3. **Position the sketch:**
   - Click to place the origin (0,0) where you want it
   - Adjust size using the scale slider if needed
   - Click **OK**

The SVG imports as a sketch with all road paths.

## Step 4: Prepare for 3D Printing

### Option A: Simple Single Height Extrusion

1. Select all paths in the sketch (Ctrl+A or drag to select)
2. Go to **Create** → **Extrude**
3. Set height to **2-3mm** (for relief map)
4. Click **OK**

### Option B: Layered Extrusion (More Detail)

Create different heights for different road types:

1. **Motorways (thickest):**
   - Select motorway paths
   - Extrude to **3mm**

2. **Primary roads:**
   - Select primary road paths
   - Extrude to **2.5mm**

3. **Secondary roads:**
   - Select secondary road paths
   - Extrude to **2mm**

4. **Residential roads:**
   - Select residential road paths
   - Extrude to **1.5mm**

### Add a Base

1. Create a new sketch on the bottom face
2. Draw a rectangle covering the entire map
3. Extrude downward **2-3mm** to create a stable base

## Step 5: Scale for Your Printer

The map uses real-world meters, so you need to scale it down:

1. Select all bodies
2. Go to **Modify** → **Scale**
3. Calculate your scale:
   - Example: 10000m radius → 200mm print = **1:50 scale** (0.02)
   - Example: 5000m radius → 150mm print = **1:33 scale** (0.03)
4. Apply the scale

**Common scales:**
- 4000m → 120mm print: scale factor **0.03**
- 8000m → 160mm print: scale factor **0.02**
- 10000m → 200mm print: scale factor **0.02**
- 15000m → 250mm print: scale factor **0.0167**

## Step 6: Export STL

1. Right-click your body in the browser
2. Select **Save as STL**
3. Choose **Medium** resolution (good balance)
4. Save the `.stl` file

## Step 7: Slice and Print

1. **Open in your slicer** (Cura, PrusaSlicer, etc.)
2. **Orientation:** Print with roads facing up
3. **Supports:** Usually not needed (relatively flat)
4. **Layer height:** 0.2mm (0.1mm for fine detail)
5. **Infill:** 20-30%
6. **Material:** PLA recommended (white or black for contrast)

## Complete Example Workflow

```powershell
# 1. Generate map
python create_map_poster.py -c "San Francisco" -C "USA" -t feature_based -d 10000 -f svg

# 2. Import SVG into Fusion 360
#    Insert → Insert SVG → Select posters/san_francisco_*.svg

# 3. In Fusion 360:
#    - Select all paths
#    - Create → Extrude (2mm height)
#    - Add base (2mm thick)
#    - Modify → Scale (0.02 for 200mm print)
#    - Save as STL

# 4. Slice and print!
```

## Troubleshooting

**Problem:** SVG too complex
- **Solution:** Reduce distance (`-d 5000` instead of `-d 20000`)

**Problem:** Roads too thin
- **Solution:** Increase extrusion height (try 3-4mm)

**Problem:** File too large
- **Solution:** Use smaller distance or simplify in Fusion 360

**Problem:** Scale doesn't match
- **Solution:** Check your actual map dimensions in Fusion 360 and adjust scale factor

## Tips

- ✅ Start with small areas (4000-6000m) for testing
- ✅ Use `feature_based` or `noir` theme for best contrast
- ✅ Test print a small section first
- ✅ Consider print bed size when choosing distance
- ✅ White/light PLA shows detail better

---

**Need more detail?** See `FUSION360_GUIDE.md` for comprehensive instructions.
