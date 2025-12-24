# Databricks notebook source
# MAGIC %md
# MAGIC # Setup Catalog, Schemas, and Volume

# COMMAND ----------

# MAGIC %python
# Get parameters
catalog_name = dbutils.widgets.get("catalog_name")
schema_stage = dbutils.widgets.get("schema_stage")
schema_processed = dbutils.widgets.get("schema_processed")
volume_name = dbutils.widgets.get("volume_name")

print(f"Setting up:")
print(f"Catalog: {catalog_name}")
print(f"Stage Schema: {schema_stage}")
print(f"Processed Schema: {schema_processed}")
print(f"Volume: {volume_name}")

# COMMAND ----------

# MAGIC %python
# Create catalog
try:
    spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog_name}")
    print(f"✓ Catalog {catalog_name} created/exists")
except Exception as e:
    print(f"Error creating catalog: {e}")

# COMMAND ----------

# MAGIC %python
# Create schemas
try:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_stage}")
    print(f"✓ Schema {catalog_name}.{schema_stage} created/exists")
    
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_processed}")
    print(f"✓ Schema {catalog_name}.{schema_processed} created/exists")
except Exception as e:
    print(f"Error creating schemas: {e}")

# COMMAND ----------

# MAGIC %python
# Create volume
try:
    spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog_name}.{schema_stage}.{volume_name}")
    print(f"✓ Volume {catalog_name}.{schema_stage}.{volume_name} created/exists")
except Exception as e:
    print(f"Error creating volume: {e}")

# COMMAND ----------

# MAGIC %python
print("Setup completed successfully!")