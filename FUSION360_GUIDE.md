# Fusion 360 Import & 3D Printing Guide

This guide walks you through importing your generated SVG maps into Fusion 360 and preparing them for 3D printing.

## Step 1: Generate Your Map

Generate an SVG map using the script:

```bash
python create_map_poster.py -c "San Francisco" -C "USA" -t feature_based -d 10000 -f svg
```

This creates a file in the `posters/` directory like: `san_francisco_feature_based_20260108_120000.svg`

## Step 2: Import SVG into Fusion 360

1. **Open Fusion 360** and create a new design
2. **Insert SVG**: Go to **Insert** → **Insert SVG**
3. **Select your SVG file** from the `posters/` directory
4. **Position the sketch**: 
   - Choose a plane (Top, Front, or Side)
   - Click to place the origin (0,0) where you want it
   - Adjust size if needed using the scale slider
   - Click **OK**

## Step 3: Prepare the Sketch

The SVG imports as a sketch with all road paths. You may want to:

1. **Inspect the sketch** - Zoom in to see all the paths
2. **Clean up if needed** - Remove or simplify any overly complex paths
3. **Group paths by road type** (optional) - If you want different heights for different road types

## Step 4: Extrude the Map

### Option A: Single Height Extrusion (Simplest)

1. Select the entire sketch (or use Select → Select All)
2. Go to **Create** → **Extrude**
3. Set your desired height (e.g., 2-3mm for a relief map)
4. Click **OK**

This creates a flat relief map with all roads at the same height.

### Option B: Layered Extrusion (More Detailed)

Create different heights for different road types:

1. **First layer - Motorways** (thickest):
   - Select motorway paths (you may need to manually select them)
   - Extrude to 3mm
   
2. **Second layer - Primary roads**:
   - Select primary road paths
   - Extrude to 2.5mm
   
3. **Third layer - Secondary roads**:
   - Select secondary road paths
   - Extrude to 2mm
   
4. **Fourth layer - Residential roads**:
   - Select residential road paths
   - Extrude to 1.5mm

> **Tip**: Use the **Project** tool to create sketches from the original SVG for each road type if needed.

## Step 5: Add a Base

For stability and a clean finish:

1. Create a new sketch on the bottom face
2. Draw a rectangle covering the entire map area
3. Extrude downward 2-3mm (this becomes the base)
4. The base will be thicker/more stable than just the road network

## Step 6: Scale Appropriately

The map is generated in meters, but your print needs to fit on your printer bed:

1. Select your entire body
2. Use **Modify** → **Scale**
3. Calculate your scale:
   - Example: 10000m radius → 200mm print = 1:50 scale
   - Example: 5000m radius → 150mm print = 1:33 scale
4. Apply the scale

> **Tip**: A 100-200mm diameter print is usually good for detail and printability.

## Step 7: Final Preparation

Before exporting for 3D printing:

1. **Check thickness**: Minimum feature size should be at least 0.4mm (nozzle width)
2. **Combine bodies** (if you made separate extrusions):
   - Go to **Modify** → **Combine**
   - Select all bodies to merge
3. **Remove unnecessary details**: Simplify if there are too many tiny roads
4. **Add fillets** (optional): Round edges for better printing

## Step 8: Export STL

1. Right-click your body in the browser
2. Select **Save as STL**
3. Choose your resolution:
   - **High**: Better detail, larger file
   - **Medium**: Good balance (recommended)
   - **Low**: Smaller file, less detail
4. Save the STL file

## Step 9: Slice and Print

Import your STL into your slicer (Cura, PrusaSlicer, etc.):

1. **Orientation**: Print with roads facing up (top-down view)
2. **Supports**: Usually not needed (map prints are relatively flat)
3. **Layer height**: 0.2mm is a good balance (0.1mm for fine detail)
4. **Infill**: 20-30% is usually sufficient
5. **Material**: PLA works great; consider white/black for contrast

## Troubleshooting

### SVG import is too complex
- **Solution**: Reduce the map distance (`-d`) to generate a smaller area
- Or manually simplify the sketch in Fusion 360

### Roads are too thin to print
- **Solution**: Increase extrusion height, or thicken paths in the sketch before extruding

### File is too large/slow to process
- **Solution**: 
  - Use a smaller distance (`-d 5000` instead of `-d 20000`)
  - Simplify the geometry in Fusion 360
  - Use fewer road types

### Print warps or doesn't stick
- **Solution**: 
  - Add a larger base (4-5mm thick)
  - Use a brim or raft in your slicer
  - Ensure bed is level and at correct temperature

## Tips for Best Results

1. **Start simple**: Try a small area first (4000-6000m) to test
2. **Test print**: Do a small test print to check scale and detail
3. **Color choice**: White or light colored PLA shows detail better
4. **Layer lines**: Consider orientation - roads facing up hides layer lines
5. **Post-processing**: Light sanding can smooth the top surface

## Example Dimensions

| Map Radius | Print Diameter | Scale | Best For |
|-----------|---------------|-------|----------|
| 4000m     | 120mm         | 1:33  | Small cities, districts |
| 8000m     | 160mm         | 1:50  | Medium cities |
| 10000m    | 200mm         | 1:50  | Large cities |
| 15000m    | 250mm         | 1:60  | Metro areas |

Adjust based on your printer bed size!

## Alternative: Direct Heightmap Approach

If you want terrain/relief instead of flat roads:

1. Generate a PNG with `-f png`
2. Use Fusion 360's **Insert** → **Canvas** to insert as image
3. Use **Create** → **Form** to create a surface
4. Use **Sculpt** tools to manually create relief based on the image

This is more advanced but gives more artistic control.

---

Happy printing! 🗺️🖨️
