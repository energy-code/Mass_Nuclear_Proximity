
import geopandas as gpd
import folium
from shapely.geometry import Point
import geopy.distance
import requests
import zipfile
import io

# US Census Bureau ZCTA shapefile (Massachusetts specific filter usually requires the full dataset or a state-specific source)
# Using the Census TIGER/Line file for 2020 ZCTAs
url = "https://www2.census.gov/geo/tiger/TIGER2020/ZCTA520/tl_2020_us_zcta520.zip"

print("Downloading Massachusetts ZIP code data from US Census Bureau...")
try:
    # Load the national dataset (this may take a moment)
    # We use a stream and filter to keep it manageable, but for this task, we'll read and filter by prefix/bounds
    usa_zips = gpd.read_file(url)

    # Massachusetts ZIP codes start with 010 through 027
    ma_zips = usa_zips[usa_zips['ZCTA5CE20'].str.startswith(('010', '011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027'))].copy()

    # Project to EPSG:26986 (Massachusetts Mainland) for accurate centroid calculation
    ma_zips_projected = ma_zips.to_crs(epsg=26986)

    # Calculate centroids and add as a new column
    ma_zips['centroid'] = ma_zips_projected.centroid.to_crs(epsg=4326)

    print(f"Successfully loaded {len(ma_zips)} ZIP codes.")
    print(ma_zips[['ZCTA5CE20', 'geometry', 'centroid']].head())
except Exception as e:
    print(f"An error occurred: {e}")

## Generate Interactive Map

### Initialize a Folium map centered on Massachusetts and visualize the ZIP code boundaries and centroids.
ma_center = [42.4, -71.4]
m = folium.Map(location=ma_center, zoom_start=8)

# Add ZIP code boundaries to the map
folium.GeoJson(
    ma_zips[['ZCTA5CE20', 'geometry']],
    name='MA ZIP Codes',
    tooltip=folium.GeoJsonTooltip(fields=['ZCTA5CE20'], aliases=['ZIP Code:'])
).add_to(m)

# Add centroids as CircleMarkers
for _, row in ma_zips.iterrows():
    centroid = row['centroid']
    if centroid:
        folium.CircleMarker(
            location=[centroid.y, centroid.x],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"ZIP: {row['ZCTA5CE20']}"
        ).add_to(m)

# Display the map
m

#location of zip codes
# Initialize the map centered on Massachusetts
ma_center = [42.4, -71.4]
m = folium.Map(location=ma_center, zoom_start=8)

# Add ZIP code boundaries to the map
folium.GeoJson(
    ma_zips[['ZCTA5CE20', 'geometry']],
    name='MA ZIP Codes',
    tooltip=folium.GeoJsonTooltip(fields=['ZCTA5CE20'], aliases=['ZIP Code:'])
).add_to(m)

# Add centroids as CircleMarkers
for _, row in ma_zips.iterrows():
    centroid = row['centroid']
    if centroid:
        folium.CircleMarker(
            location=[centroid.y, centroid.x],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"ZIP: {row['ZCTA5CE20']}"
        ).add_to(m)

# Display the map
m

# Re-loading/ensuring ma_zips is available since it was lost in previous execution state
url = "https://www2.census.gov/geo/tiger/TIGER2020/ZCTA520/tl_2020_us_zcta520.zip"
usa_zips = gpd.read_file(url)
ma_zips = usa_zips[usa_zips['ZCTA5CE20'].str.startswith(('010', '011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027'))].copy()

# Project and calculate centroids
ma_zips_projected = ma_zips.to_crs(epsg=26986)
ma_zips['centroid'] = ma_zips_projected.centroid.to_crs(epsg=4326)

# Initialize the map centered on Massachusetts
ma_center = [42.4, -71.4]
m = folium.Map(location=ma_center, zoom_start=8)

# Add ZIP code boundaries to the map
folium.GeoJson(
    ma_zips[['ZCTA5CE20', 'geometry']],
    name='MA ZIP Codes',
    tooltip=folium.GeoJsonTooltip(fields=['ZCTA5CE20'], aliases=['ZIP Code:'])
).add_to(m)

# Add centroids as CircleMarkers
for _, row in ma_zips.iterrows():
    centroid = row['centroid']
    if centroid:
        folium.CircleMarker(
            location=[centroid.y, centroid.x],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"ZIP: {row['ZCTA5CE20']}"
        ).add_to(m)

# Display the map
m

import geopy.distance
import pandas as pd

def calculate_distances(input_coords, gdf):
    """
    Calculates geodesic distance from input_coords to all centroids in the GeoDataFrame.
    input_coords: tuple of (lat, lon)
    gdf: GeoDataFrame containing a 'centroid' column with shapely Point objects
    """
    # Create a copy to avoid modifying the original dataframe
    result_df = gdf.copy()

    # Function to extract lat/lon from shapely point and calculate distance
    def get_dist(centroid_point):
        if centroid_point is None:
            return None
        # geopy expects (lat, lon), shapely point is (x, y) which is (lon, lat)
        centroid_coords = (centroid_point.y, centroid_point.x)
        return geopy.distance.geodesic(input_coords, centroid_coords).km

    # Apply distance calculation and store as scalar float (km)
    result_df['distance_km'] = result_df['centroid'].apply(get_dist)
    return result_df

# Test the function with Boston coordinates (42.3601, -71.0589)
boston_coords = (42.3601, -71.0589)
distance_results = calculate_distances(boston_coords, ma_zips)

# Display the top 10 nearest ZIP codes to the test coordinates
nearest_zips = distance_results[['ZCTA5CE20', 'distance_km']].sort_values(by='distance_km').head(10)
print("Nearest ZIP codes to Boston (42.3601, -71.0589):")
print(nearest_zips)

# Define the nuclear plant data
nuclear_data = [
    {"Plant": "Vermont Yankee", "Latitude": 42.7781, "Longitude": -72.5133},
    {"Plant": "Millstone", "Latitude": 41.3122, "Longitude": -72.1678},
    {"Plant": "Seabrook", "Latitude": 42.8997, "Longitude": -70.8487},
    {"Plant": "Pilgrim", "Latitude": 41.9444, "Longitude": -70.5794},
    {"Plant": "Indian Point", "Latitude": 41.2706, "Longitude": -73.9526},
    {"Plant": "Maine Yankee", "Latitude": 43.9508, "Longitude": -69.6961},
    {"Plant": "Yankee Rowe", "Latitude": 42.7297, "Longitude": -72.9289}
]

# Create the DataFrame
nuclear_plants_df = pd.DataFrame(nuclear_data)

# Display the DataFrame to verify the data
print("Nuclear Power Plants Dataset:")
print(nuclear_plants_df)

all_distances = []

for index, plant_row in nuclear_plants_df.iterrows():
    plant_name = plant_row['Plant']
    plant_coords = (plant_row['Latitude'], plant_row['Longitude'])

    # Calculate distances to all centroids for this specific plant
    plant_dist_df = calculate_distances(plant_coords, ma_zips)

    # Select relevant columns and add the plant name identifier
    temp_df = plant_dist_df[['ZCTA5CE20', 'distance_km']].copy()
    temp_df['Plant'] = plant_name

    all_distances.append(temp_df)

# Combine all results into a single DataFrame
final_distance_results = pd.concat(all_distances, ignore_index=True)

# Verify the shape: 7 plants * 539 ZIP codes = 3773 rows
print(f"Total distance calculations: {final_distance_results.shape[0]}")
print(f"Expected calculations: {len(nuclear_plants_df) * len(ma_zips)}")
print("\nPreview of distance results:")
print(final_distance_results.head())


###Location of plants and zip codes
# Add Nuclear Power Plant locations to the map
for _, plant_row in nuclear_plants_df.iterrows():
    folium.Marker(
        location=[plant_row['Latitude'], plant_row['Longitude']],
        popup=folium.Popup(plant_row['Plant'], parse_html=True),
        tooltip=plant_row['Plant'],
        icon=folium.Icon(color='black', icon='info-sign')
    ).add_to(m)

# Display the updated map
m

# 1. Remove Yankee Rowe and Connecticut Yankee from the calculation
# Note: Connecticut Yankee was not in the original list, but we filter safely
plants_to_exclude = ['Yankee Rowe', 'Connecticut Yankee']
filtered_distances = final_distance_results[~final_distance_results['Plant'].isin(plants_to_exclude)].copy()

# 2. Filter out plants farther than 120km
close_plants = filtered_distances[filtered_distances['distance_km'] <= 120].copy()

# 3. Calculate 1/distance
close_plants['inv_dist'] = 1 / close_plants['distance_km']

# 4. Sum (1/distance) for each ZIP code
proximity_scores = close_plants.groupby('ZCTA5CE20')['inv_dist'].sum().reset_index()
proximity_scores.columns = ['ZCTA5CE20', 'nuclear_proximity_score']

# 5. Display top findings
top_scores = proximity_scores.sort_values(by='nuclear_proximity_score', ascending=False).head(10)
print('Updated Top 10 ZIP Codes by Nuclear Proximity Score (Excluding Yankee Rowe):')
display(top_scores)


###Recreate map from the Massachusetts paper
# Prepare the data for mapping
map_df = ma_zips.drop(columns=['centroid']).merge(proximity_scores, on='ZCTA5CE20', how='left')
map_df['nuclear_proximity_score'] = map_df['nuclear_proximity_score'].fillna(0)

# Initialize the map
m_choropleth = folium.Map(location=[42.4, -71.4],
                          tiles='cartodbpositron',  # Cleaner background for reports,
                          zoom_start=8)

# Create the Choropleth layer
folium.Choropleth(
    geo_data=map_df,
    name='Choropleth',
    data=map_df,
    columns=['ZCTA5CE20', 'nuclear_proximity_score'],
    key_on='feature.properties.ZCTA5CE20',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Updated Nuclear Proximity Score (Sum of 1/d)',
    nan_fill_color='white'
).add_to(m_choropleth)

# Add a Tooltip layer
folium.GeoJson(
    map_df,
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent', 'weight': 0},
    tooltip=folium.GeoJsonTooltip(fields=['ZCTA5CE20', 'nuclear_proximity_score'], aliases=['ZIP Code:', 'Proximity Score:'])
).add_to(m_choropleth)

# Display the map
m_choropleth

# Static report version of the Nuclear Proximity Map
import folium

# Define bounding box for Massachusetts to clip surrounding states
# Format: [[min_lat, min_lon], [max_lat, max_lon]]
ma_bounds = [[41.2, -73.6], [42.9, -69.8]]

# Initialize map with static constraints
m_static = folium.Map(
    location=[42.4, -71.4],
    zoom_start=8,
    tiles='cartodbpositron',  # Cleaner background for reports
    min_lat=ma_bounds[0][0], max_lat=ma_bounds[1][0],
    min_lon=ma_bounds[0][1], max_lon=ma_bounds[1][1],
    max_bounds=True,
    zoom_control=False,       # Remove UI elements for a cleaner static look
    scrollWheelZoom=False,
    dragging=False
)

# Add the Choropleth layer
folium.Choropleth(
    geo_data=map_df,
    name='Nuclear Proximity',
    data=map_df,
    columns=['ZCTA5CE20', 'nuclear_proximity_score'],
    key_on='feature.properties.ZCTA5CE20',
    fill_color='YlOrRd',
    fill_opacity=0.8,
    line_opacity=0.4,
    line_weight=0.5,
    legend_name='Nuclear Proximity Score (Sum of 1/distance)',
    nan_fill_color='white'
).add_to(m_static)

# Fit the map strictly to the MA bounds
m_static.fit_bounds(ma_bounds)

# Display the static map
display(m_static)


###Map showing distance from the nearest plant
# 1. Filter out the excluded plants
excluded = ['Yankee Rowe', 'Connecticut Yankee']
filtered_df = final_distance_results[~final_distance_results['Plant'].isin(excluded)].copy()

# 2. For each ZIP code, find the minimum distance to ANY of the remaining plants
min_distance_df = filtered_df.groupby('ZCTA5CE20')['distance_km'].min().reset_index()
min_distance_df.columns = ['ZCTA5CE20', 'min_dist_km']

# 3. Merge with geospatial data
map_dist_df = ma_zips.drop(columns=['centroid']).merge(min_distance_df, on='ZCTA5CE20', how='left')
map_dist_df['min_dist_km'] = map_dist_df['min_dist_km'].fillna(map_dist_df['min_dist_km'].max())

# 4. Initialize the map
m_min_dist = folium.Map(location=[42.4, -71.4], zoom_start=8)

# 5. Create the Choropleth layer based on absolute distance (using a reversed scale so closer is 'hotter')
folium.Choropleth(
    geo_data=map_dist_df,
    name='Nearest Plant Distance',
    data=map_dist_df,
    columns=['ZCTA5CE20', 'min_dist_km'],
     tiles='cartodbpositron',  # Cleaner background for reports,
    key_on='feature.properties.ZCTA5CE20',
    fill_color='YlOrRd_r',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Distance to Nearest Nuclear Plant (km)',
    nan_fill_color='white'
).add_to(m_min_dist)

# 6. Add Tooltip
folium.GeoJson(
    map_dist_df,
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent', 'weight': 0},
    tooltip=folium.GeoJsonTooltip(fields=['ZCTA5CE20', 'min_dist_km'], aliases=['ZIP Code:', 'Distance (km):'])
).add_to(m_min_dist)


### Display map
m_min_dist

# 1. Prepare comparison data
# We already have min_distance_df and proximity_scores
comparison_df = min_distance_df.merge(proximity_scores, on='ZCTA5CE20')

# 2. Calculate the count of plants within the 120km radius for each ZIP
plant_counts = close_plants.groupby('ZCTA5CE20').size().reset_index(name='plants_in_range')
comparison_df = comparison_df.merge(plant_counts, on='ZCTA5CE20', how='left')
comparison_df['plants_in_range'] = comparison_df['plants_in_range'].fillna(0)

# 3. Identify ZIP codes influenced by multiple plants
# We look for ZIPs with a relatively high min_dist but high proximity score
multi_influence = comparison_df[comparison_df['plants_in_range'] > 1].sort_values(by='nuclear_proximity_score', ascending=False)

print("Comparison of Nearest Distance vs. Cumulative Proximity Score:")
print("Note how ZIPs with more 'plants_in_range' gain higher scores even with larger min_dist_km.")
display(multi_influence.head(15))

# 4. Correlation check
correlation = comparison_df['min_dist_km'].corr(comparison_df['nuclear_proximity_score'])
print(f"\nCorrelation between Nearest Distance and Proximity Score: {correlation:.2f}")
print("(A lower negative correlation suggests multi-plant overlap is significantly shifting the scores)")


###Chart showing overlap of multiple plants
# Prepare the data for mapping the plant counts
map_influence_df = ma_zips.drop(columns=['centroid']).merge(comparison_df[['ZCTA5CE20', 'plants_in_range', 'nuclear_proximity_score']], on='ZCTA5CE20', how='left')

# Initialize the map
m_influence = folium.Map(location=[42.4, -71.4], zoom_start=8, tiles='cartodbpositron')

# Create the Choropleth layer based on the NUMBER of plants in range
folium.Choropleth(
    geo_data=map_influence_df,
    name='Multi-Plant Influence Count',
    data=map_influence_df,
    columns=['ZCTA5CE20', 'plants_in_range'],
     tiles='cartodbpositron',  # Cleaner background for reports,
    key_on='feature.properties.ZCTA5CE20',
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Count of Nuclear Plants within 120km',
    nan_fill_color='white'
).add_to(m_influence)

### Add Nuclear Power Plants as markers to see the overlap clearly
for _, plant_row in nuclear_plants_df.iterrows():
    if plant_row['Plant'] not in excluded:
        folium.Circle(
            location=[plant_row['Latitude'], plant_row['Longitude']],
            radius=120000, # 120km radius
            color='blue',
            fill=True,
            fill_opacity=0.05,
            weight=1
        ).add_to(m_influence)
        folium.Marker(
            location=[plant_row['Latitude'], plant_row['Longitude']],
            tooltip=plant_row['Plant'],
            icon=folium.Icon(color='black', icon='bolt', prefix='fa')
        ).add_to(m_influence)

# Add Tooltip showing both count and cumulative score
folium.GeoJson(
    map_influence_df,
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent', 'weight': 0},
    tooltip=folium.GeoJsonTooltip(
        fields=['ZCTA5CE20', 'plants_in_range', 'nuclear_proximity_score'],
        aliases=['ZIP Code:', 'Plants in 120km Range:', 'Total Proximity Score:']
    )
).add_to(m_influence)

display(m_influence)


###Correlation of higher proximity values to lower distances to plants.
# 1. Calculate ranks for both metrics (lower distance = higher rank, higher proximity = higher rank)
comparison_df['dist_rank'] = comparison_df['min_dist_km'].rank(ascending=True)
comparison_df['proximity_rank'] = comparison_df['nuclear_proximity_score'].rank(ascending=False)

# 2. Calculate the Shift: High positive value means the cumulative score makes it 'seem' closer
# than its physical distance to the nearest plant would suggest.
comparison_df['rank_shift'] = comparison_df['dist_rank'] - comparison_df['proximity_rank']

# 3. Merge with geospatial data
map_shift_df = ma_zips.drop(columns=['centroid']).merge(comparison_df[['ZCTA5CE20', 'rank_shift', 'min_dist_km', 'nuclear_proximity_score', 'plants_in_range']], on='ZCTA5CE20', how='left')

# 4. Initialize the map
m_shift = folium.Map(location=[42.4, -71.4], zoom_start=8, tiles='cartodbpositron')

# 5. Create the Choropleth layer based on Rank Shift
# Areas in Red are those where the 'proximity score' is much higher than the 'nearest distance' suggests
folium.Choropleth(
    geo_data=map_shift_df,
    name='Proximity Rank Shift',
    data=map_shift_df,
    columns=['ZCTA5CE20', 'rank_shift'],
    key_on='feature.properties.ZCTA5CE20',
    fill_color='RdYlGn_r',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Rank Shift (Cumulative Proximity vs. Nearest Distance)',
    nan_fill_color='white'
).add_to(m_shift)

# 6. Add Tooltip
folium.GeoJson(
    map_shift_df,
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent', 'weight': 0},
    tooltip=folium.GeoJsonTooltip(
        fields=['ZCTA5CE20', 'rank_shift', 'min_dist_km', 'nuclear_proximity_score', 'plants_in_range'],
        aliases=['ZIP Code:', 'Rank Shift Index:', 'Nearest Plant (km):', 'Total Proximity Score:', 'Plants in Range:']
    )
).add_to(m_shift)

display(m_shift)


###Recreate chart from paper with the highest value zip codes removed as stated in paper
# 1. Identify the top 2 ZIP codes to exclude
top_2_zips = proximity_scores.sort_values(by='nuclear_proximity_score', ascending=False).head(2)['ZCTA5CE20'].tolist()
print(f"Excluding top 2 ZIP codes: {top_2_zips}")

# 2. Filter the map data
map_df_filtered = map_df[~map_df['ZCTA5CE20'].isin(top_2_zips)].copy()

# 3. Initialize the second map
m_choropleth_filtered = folium.Map(location=[42.4, -71.4], zoom_start=8, tiles='cartodbpositron')  # Cleaner background for reports)

# 4. Create the filtered Choropleth layer
folium.Choropleth(
    geo_data=map_df_filtered,
    name='Filtered Choropleth',
    data=map_df_filtered,
    columns=['ZCTA5CE20', 'nuclear_proximity_score'],
    key_on='feature.properties.ZCTA5CE20',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Proximity Score (Excluding Top 2 ZCTAs)',
    nan_fill_color='white'
).add_to(m_choropleth_filtered)

# 5. Add a Tooltip layer for the filtered map
folium.GeoJson(
    map_df_filtered,
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent', 'weight': 0},
    tooltip=folium.GeoJsonTooltip(fields=['ZCTA5CE20', 'nuclear_proximity_score'], aliases=['ZIP Code:', 'Proximity Score:'])
).add_to(m_choropleth_filtered)

# Display the filtered map
m_choropleth_filtered