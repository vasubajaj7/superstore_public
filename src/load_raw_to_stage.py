# Databricks notebook source
# MAGIC %md
# MAGIC # Load Raw Data to Stage Schema using Autoloader

# COMMAND ----------

# MAGIC %python
# Get parameters
catalog_name = dbutils.widgets.get("catalog_name")
schema_name = dbutils.widgets.get("schema_name") 
volume_name = dbutils.widgets.get("volume_name")

print(f"Catalog: {catalog_name}")
print(f"Schema: {schema_name}")
print(f"Volume: {volume_name}")

# COMMAND ----------

# MAGIC %python
from pyspark.sql.types import *

# Define schema for superstore data
superstore_schema = StructType([
    StructField("Row_ID", IntegerType(), True),
    StructField("Order_ID", StringType(), True),
    StructField("Order_Date", StringType(), True),
    StructField("Ship_Date", StringType(), True),
    StructField("Ship_Mode", StringType(), True),
    StructField("Customer_ID", StringType(), True),
    StructField("Customer_Name", StringType(), True),
    StructField("Segment", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("City", StringType(), True),
    StructField("State", StringType(), True),
    StructField("Postal_Code", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Product_ID", StringType(), True),
    StructField("Category", StringType(), True),
    StructField("Sub_Category", StringType(), True),
    StructField("Product_Name", StringType(), True),
    StructField("Sales", DoubleType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("Discount", DoubleType(), True),
    StructField("Profit", DoubleType(), True)
])

# COMMAND ----------

# MAGIC %python
# Use Autoloader to read CSV files from volume
df = (spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "csv")
      .option("header", "true")
      .schema(superstore_schema)
      .load(f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/"))

# COMMAND ----------

# MAGIC %python
# Write to stage table using autoloader
checkpoint_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/checkpoints/superstore"

(df.writeStream
 .format("delta")
 .option("checkpointLocation", checkpoint_path)
 .option("mergeSchema", "true")
 .trigger(availableNow=True)
 .toTable(f"{catalog_name}.{schema_name}.superstore")
 .awaitTermination())

print("Data loaded successfully to stage.superstore table")