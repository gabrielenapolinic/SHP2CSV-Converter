#!/usr/bin/env python
# coding: utf-8

# In[2]:


import geopandas as gpd
import pandas as pd
import os

# Configuration
INPUT_DIR = "ShapefileFolderPath"
OUTPUT_DIR = "ShapefiletoCSVFolderPath"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_shp_to_csv(input_dir, output_dir):
    """
    Convert all shapefiles to CSV with WKT geometry
    """
    processed_files = 0
    error_files = 0
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".shp"):
            file_path = os.path.join(input_dir, filename)
            try:
                print(f"Processing: {filename}")
                
                # Read shapefile and convert to DataFrame
                gdf = gpd.read_file(file_path)
                df = pd.DataFrame(gdf)  # Convert to regular DataFrame
                
                # Convert geometry to WKT string
                df['geometry'] = df['geometry'].apply(lambda x: x.wkt)
                
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




