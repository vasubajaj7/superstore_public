# Databricks notebook source
# MAGIC %md
# MAGIC # Upload Sample Data to Raw Volume

# COMMAND ----------

# MAGIC %python
import os

# Configuration
catalog_name = "superstore_dev"  # Use dev catalog for testing
schema_name = "stage"
volume_name = "raw"

print(f"Uploading data to: /Volumes/{catalog_name}/{schema_name}/{volume_name}/")

# COMMAND ----------

# MAGIC %python
# Create sample data directly in the notebook
sample_data = """Row ID,Order ID,Order Date,Ship Date,Ship Mode,Customer ID,Customer Name,Segment,Country,City,State,Postal Code,Region,Product ID,Category,Sub-Category,Product Name,Sales,Quantity,Discount,Profit
1,CA-2016-152156,11/8/2016,11/11/2016,Second Class,CG-12520,Claire Gute,Consumer,United States,Henderson,Kentucky,42420,South,FUR-BO-10001798,Furniture,Bookcases,Bush Somerset Collection Bookcase,261.96,2,0,41.9136
2,CA-2016-152156,11/8/2016,11/11/2016,Second Class,CG-12520,Claire Gute,Consumer,United States,Henderson,Kentucky,42420,South,FUR-CH-10000454,Furniture,Chairs,Hon Deluxe Fabric Upholstered Stacking Chairs,731.94,3,0,219.582
3,CA-2016-138688,6/12/2016,6/16/2016,Second Class,DV-13045,Darrin Van Huff,Corporate,United States,Los Angeles,California,90036,West,OFF-LA-10000240,Office Supplies,Labels,Self-Adhesive Address Labels for Typewriters by Universal,14.62,2,0,6.8714
4,US-2015-108966,10/11/2015,10/18/2015,Standard Class,SO-20335,Sean O'Donnell,Consumer,United States,Fort Lauderdale,Florida,33311,South,FUR-TA-10000577,Furniture,Tables,Bretford CR4500 Series Slim Rectangular Table,957.5775,5,0.45,-383.031
5,US-2015-108966,10/11/2015,10/18/2015,Standard Class,SO-20335,Sean O'Donnell,Consumer,United States,Fort Lauderdale,Florida,33311,South,OFF-ST-10000760,Office Supplies,Storage,Eldon Fold 'N Roll Cart System,22.368,2,0.2,2.5164"""

# Write to volume
volume_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/superstore.csv"

with open("/tmp/superstore_sample.csv", "w") as f:
    f.write(sample_data)

# Copy to volume using dbutils
dbutils.fs.cp("file:/tmp/superstore_sample.csv", volume_path)

print(f"Sample data uploaded to: {volume_path}")

# COMMAND ----------

# MAGIC %python
# Verify the upload
files = dbutils.fs.ls(f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/")
for file in files:
    print(f"File: {file.name}, Size: {file.size} bytes")

# COMMAND ----------

# MAGIC %python
# Preview the data
df = spark.read.option("header", "true").csv(f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/superstore.csv")
display(df)