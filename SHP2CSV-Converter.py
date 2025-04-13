#!/usr/bin/env python
# coding: utf-8

# In[2]:

import geopandas as gpd
import pandas as pd
import os
import warnings

# Configuration
INPUT_DIR = '/home/gabriele/Scrivania/4326'
OUTPUT_DIR = '/home/gabriele/Scrivania/Napoli_EGU/CSV'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_shp_to_csv(input_dir, output_dir):
    """
    Convert all shapefiles to CSV with WKT geometry, handling None geometries.
    """
    processed_files = 0
    error_files = 0
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".shp"):
            file_path = os.path.join(input_dir, filename)
            try:
                print(f"Processing: {filename}")
                
                # Read shapefile
                gdf = gpd.read_file(file_path)
                
                # Check for None geometries and warn
                if gdf.geometry.isnull().any():
                    invalid_count = gdf.geometry.isnull().sum()
                    warnings.warn(
                        f"{filename} contains {invalid_count} rows with None geometry. "
                        "These will be converted to empty strings in CSV."
                    )
                
                # Convert to DataFrame and handle None geometries
                df = pd.DataFrame(gdf)
                df['geometry'] = df['geometry'].apply(
                    lambda x: x.wkt if x is not None else ''
                )
                
                # Save CSV
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.csv")
                df.to_csv(output_path, index=False)
                
                print(f"Successfully converted: {filename}")
                processed_files += 1
                
            except Exception as e:
                error_files += 1
                print(f"Error processing {filename}: {str(e)}")
    
    print("\nConversion complete!")
    print(f"Successfully processed files: {processed_files}")
    print(f"Files with errors: {error_files}")

convert_shp_to_csv(INPUT_DIR, OUTPUT_DIR)

# In[ ]:
