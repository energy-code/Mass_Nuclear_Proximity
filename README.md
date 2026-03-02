# Massachusetts Nuclear Proximity Analysis

## Overview
This project analyzes the geospatial relationship between Massachusetts ZIP codes and seven regional nuclear power plants. It compares two different proximity metrics to understand how overlapping spheres of influence affect geographic risk profiles.

## Analysis Methodology
1.  **Data Acquisition**: 
    *   ZIP Code Tabulation Areas (ZCTAs) from the US Census Bureau.
    *   Geographic coordinates for regional nuclear facilities (Seabrook, Pilgrim, Millstone, etc.).
2.  **Metrics Calculated**:
    *   **Nearest Plant Distance**: The absolute geodesic distance (km) to the single closest facility.
    *   **Nuclear Proximity Score**: A cumulative metric calculated as the sum of inverse distances ($\sum 1/d$) for all plants within a 120km radius.
    *   **Rank Shift**: A comparison index showing where the cumulative proximity score makes a region 'closer' in risk terms than its physical distance to a single plant would suggest.

## Key Findings
*   **Multi-Plant Overlap**: Several ZIP codes in central and eastern Massachusetts are influenced by up to 3 plants simultaneously, leading to higher cumulative proximity scores than areas physically closer to a single plant.
*   **Correlation**: A correlation of -0.51 between absolute distance and cumulative score highlights significant shifts caused by facility overlap.

## Visualizations
*   **Interactive Choropleths**: Visualizing absolute distance vs. cumulative proximity.
*   **Influence Maps**: Highlighting the 120km radii and plant counts per ZIP.
*   **Rank Shift Map**: Pinpointing 'hotspots' where multi-plant influence is most pronounced.

## Technologies Used
*   Python (GeoPandas, Folium, Shapely, Geopy, Pandas)
*   US Census Bureau TIGER/Line Datasets
