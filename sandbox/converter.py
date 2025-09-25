import geopandas as gpd
import pandas as pd
import json
import os


if __name__ == "__main__":
    with open('all_diagrams.json', 'r') as f:
        all_diagrams = json.load(f)
    combined_gdf = gpd.GeoDataFrame()
    for diagram in all_diagrams:
        gdf = gpd.GeoDataFrame.from_features(diagram['geojson'])

        for key in diagram:
            if key not in ['geojson', 'name']:
                gdf[key] = diagram[key]
                for feature in diagram['geojson']['features']:
                    feature['properties'][key] = diagram[key]

        combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)
    os.makedirs('diagrams', exist_ok=True)
    combined_gdf.to_file("diagrams/combined.geojson", driver='GeoJSON')

    