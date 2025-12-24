import pytest
from unittest.mock import Mock, patch, MagicMock
from pyspark.sql.functions import *
from pyspark.sql.types import *
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestDataPipeline:
    
    @pytest.mark.integration
    def test_stage_data_transformation(self, spark, sample_superstore_data, superstore_schema):
        """Test data transformation from raw to stage"""
        # Create source dataframe
        df = spark.createDataFrame(sample_superstore_data, superstore_schema)
        
        # Apply transformations similar to stage processing
        transformed_df = df.withColumn("ingestion_timestamp", current_timestamp())
        
        # Assertions
        assert transformed_df.count() == 2
        assert "ingestion_timestamp" in transformed_df.columns
        
        # Check data types
        sales_col = [field for field in transformed_df.schema.fields if field.name == "Sales"][0]
        assert sales_col.dataType == DoubleType()
    
    @pytest.mark.integration
    def test_processed_data_transformation(self, spark, sample_superstore_data, superstore_schema):
        """Test data transformation from stage to processed"""
        # Create source dataframe
        df = spark.createDataFrame(sample_superstore_data, superstore_schema)
        
        # Apply transformations similar to processed layer
        processed_df = (df
                       .withColumn("Order_Date", to_date(col("Order_Date"), "M/d/yyyy"))
                       .withColumn("Ship_Date", to_date(col("Ship_Date"), "M/d/yyyy"))
                       .withColumn("Profit_Margin", col("Profit") / col("Sales"))
                       .withColumn("processing_timestamp", current_timestamp()))
        
        # Assertions
        assert processed_df.count() == 2
        assert "Profit_Margin" in processed_df.columns
        assert "processing_timestamp" in processed_df.columns
        
        # Check profit margin calculation
        profit_margins = processed_df.select("Profit_Margin").collect()
        expected_margin_1 = 41.9136 / 261.96
        assert abs(profit_margins[0]["Profit_Margin"] - expected_margin_1) < 0.001
    
    @pytest.mark.integration
    def test_data_quality_checks(self, spark, sample_superstore_data, superstore_schema):
        """Test data quality expectations"""
        # Create dataframe with some invalid data
        invalid_data = [
            (3, "CA-2016-152157", "11/8/2016", "11/11/2016", "Second Class", 
             "CG-12521", "Test Customer", "Consumer", "United States", "Test City", 
             "Test State", "12345", "South", "TEST-PROD", "Furniture", 
             "Tables", "Test Product", -100.0, 0, 0.0, -50.0),  # Invalid: negative sales, zero quantity
        ]
        
        all_data = sample_superstore_data + invalid_data
        df = spark.createDataFrame(all_data, superstore_schema)
        
        # Apply quality checks
        valid_sales_df = df.filter(col("Sales") > 0)
        valid_quantity_df = df.filter(col("Quantity") > 0)
        
        # Assertions
        assert df.count() == 3  # Total records
        assert valid_sales_df.count() == 2  # Only valid sales
        assert valid_quantity_df.count() == 2  # Only valid quantities
    
    @pytest.mark.integration
    def test_aggregation_logic(self, spark, sample_superstore_data, superstore_schema):
        """Test gold layer aggregation logic"""
        df = spark.createDataFrame(sample_superstore_data, superstore_schema)
        
        # Apply aggregation similar to gold layer
        agg_df = (df
                 .groupBy("Category", "Region", "Segment")
                 .agg(
                     sum("Sales").alias("Total_Sales"),
                     sum("Profit").alias("Total_Profit"),
                     avg(col("Profit") / col("Sales")).alias("Avg_Profit_Margin"),
                     count("*").alias("Order_Count")
                 ))
        
        # Assertions
        assert agg_df.count() == 1  # Both records have same Category, Region, Segment
        
        result = agg_df.collect()[0]
        expected_total_sales = 261.96 + 731.94
        expected_total_profit = 41.9136 + 219.582
        
        assert abs(result["Total_Sales"] - expected_total_sales) < 0.01
        assert abs(result["Total_Profit"] - expected_total_profit) < 0.01
        assert result["Order_Count"] == 2