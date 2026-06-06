# Prompt Log - Experiment 4: Flood Inundation Analysis

## Experiment Goal
In this experiment, I used OpenCode / AI assistance to help build a DEM-based flood inundation analysis. The goal was to create DEM data, calculate flooded cells for different water levels, visualize flood extent, and check that the results are physically reasonable.

## Prompt 1: DEM Preparation
**Tool used:** OpenCode / AI assistant

**My prompt:** I need to create a simple DEM for a flood inundation experiment. The guide says I can generate a 100 by 100 grid with elevation values between 30 m and 80 m. Please help me make synthetic DEM data using NumPy.

**AI output summary:** The AI suggested using NumPy to create a 2D terrain grid with a slope and some random variation.

**My check/correction:** I kept the DEM size as 100 by 100 and rescaled the elevation values to stay between about 30 m and 80 m. I also saved it as `dem_data.npy` so it can be submitted.

## Prompt 2: Flood Calculation
**Tool used:** OpenCode / AI assistant

**My prompt:** I have a 2D NumPy array called dem. Help me calculate flooded cells for a water level. A cell should be flooded if elevation is less than the water level. I also need inundation depth and flooded area percentage.

**AI output summary:** The AI suggested using a boolean mask `dem < water_level` and NumPy `where` to calculate depth.

**My check/correction:** I checked that non-flooded cells have depth 0. I also checked that the flooded percentage is calculated using the number of flooded cells divided by the total number of cells.

## Prompt 3: Visualization
**Tool used:** OpenCode / AI assistant

**My prompt:** Help me create flood visualizations with matplotlib. I need the original DEM, flood extent as a blue overlay, and inundation depth as a heatmap.

**AI output summary:** The AI suggested using `imshow`, grayscale for the DEM, and a blue colormap for flood depth.

**My check/correction:** I added titles, colorbars, labels, and saved the required figures for 40 m and 50 m water levels.

## Prompt 4: Dynamic Simulation and Validation
**Tool used:** OpenCode / AI assistant

**My prompt:** Help me loop through water levels from 40 m to 50 m and calculate flooded percentage at each level. I also need to validate that flooded area increases with water level.

**AI output summary:** The AI suggested storing the water level results in a list and plotting water level versus flooded percentage.

**My check/correction:** I added validation checks for monotonic increase, flooded percentage between 0 and 100, maximum depth, and edge cases where water level is below the minimum DEM elevation or above the maximum DEM elevation.

## Validation Notes
- The DEM file was generated and saved as `dem_data.npy`.
- Flooded cells are calculated using `Elevation < Water_Level`.
- Inundation depth is calculated as `Water_Level - Elevation` only for flooded cells.
- Flooded percentage increases as water level rises.
- The 40 m and 50 m flood maps were generated.
- The water level vs flooded percentage curve was generated.
