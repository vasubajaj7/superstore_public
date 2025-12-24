# Databricks notebook source
# MAGIC %md
# MAGIC # DLT Pipeline: Stage to Processed

# COMMAND ----------

import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

@dlt.table(
    name="superstore_bronze",
    comment="Bronze table - raw superstore data from stage"
)
def superstore_bronze():
    return (
        spark.readStream
        .table("stage.superstore")
        .withColumn("ingestion_timestamp", current_timestamp())
    )

# COMMAND ----------

@dlt.table(
    name="superstore_silver",
    comment="Silver table - cleaned superstore data"
)
@dlt.expect_or_drop("valid_sales", "Sales > 0")
@dlt.expect_or_drop("valid_quantity", "Quantity > 0")
def superstore_silver():
    return (
        dlt.read_stream("superstore_bronze")
        .withColumn("Order_Date", to_date(col("Order_Date"), "M/d/yyyy"))
        .withColumn("Ship_Date", to_date(col("Ship_Date"), "M/d/yyyy"))
        .withColumn("Profit_Margin", col("Profit") / col("Sales"))
        .withColumn("processing_timestamp", current_timestamp())
    )

# COMMAND ----------

@dlt.table(
    name="superstore_gold",
    comment="Gold table - aggregated superstore metrics"
)
def superstore_gold():
    return (
        dlt.read_stream("superstore_silver")
        .groupBy("Category", "Region", "Segment")
        .agg(
            sum("Sales").alias("Total_Sales"),
            sum("Profit").alias("Total_Profit"),
            avg("Profit_Margin").alias("Avg_Profit_Margin"),
            count("*").alias("Order_Count")
        )
        .withColumn("aggregation_timestamp", current_timestamp())
    )