"""
Utility functions for Superstore data pipeline
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

def get_spark_session():
    """Get or create Spark session"""
    return SparkSession.builder.appName("SuperstoreETL").getOrCreate()

def upload_sample_data_to_volume(spark, catalog_name, schema_name, volume_name, local_file_path):
    """Upload sample data to volume"""
    volume_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}/"
    
    # Read local CSV and write to volume
    df = spark.read.option("header", "true").csv(local_file_path)
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(volume_path)
    
    return volume_path

def check_table_exists(spark, table_name):
    """Check if table exists"""
    try:
        spark.sql(f"DESCRIBE TABLE {table_name}")
        return True
    except:
        return False

def get_table_count(spark, table_name):
    """Get row count from table"""
    if check_table_exists(spark, table_name):
        return spark.sql(f"SELECT COUNT(*) as count FROM {table_name}").collect()[0]['count']
    return 0

def validate_data_quality(spark, table_name):
    """Basic data quality checks"""
    if not check_table_exists(spark, table_name):
        return {"exists": False}
    
    df = spark.table(table_name)
    total_rows = df.count()
    null_counts = {}
    
    for col_name in df.columns:
        null_count = df.filter(col(col_name).isNull()).count()
        null_counts[col_name] = null_count
    
    return {
        "exists": True,
        "total_rows": total_rows,
        "null_counts": null_counts
    }