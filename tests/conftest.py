import pytest
import os
import sys
from unittest.mock import Mock, MagicMock
from pyspark.sql import SparkSession
from pyspark.sql.types import *

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture(scope="session")
def spark():
    """Create Spark session for testing"""
    spark = (SparkSession.builder
             .appName("SuperstoreTests")
             .master("local[2]")
             .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse")
             .getOrCreate())
    
    yield spark
    spark.stop()

@pytest.fixture
def sample_superstore_data():
    """Sample superstore data for testing"""
    return [
        (1, "CA-2016-152156", "11/8/2016", "11/11/2016", "Second Class", 
         "CG-12520", "Claire Gute", "Consumer", "United States", "Henderson", 
         "Kentucky", "42420", "South", "FUR-BO-10001798", "Furniture", 
         "Bookcases", "Bush Somerset Collection Bookcase", 261.96, 2, 0.0, 41.9136),
        (2, "CA-2016-152156", "11/8/2016", "11/11/2016", "Second Class",
         "CG-12520", "Claire Gute", "Consumer", "United States", "Henderson",
         "Kentucky", "42420", "South", "FUR-CH-10000454", "Furniture",
         "Chairs", "Hon Deluxe Fabric Upholstered Stacking Chairs", 731.94, 3, 0.0, 219.582)
    ]

@pytest.fixture
def superstore_schema():
    """Superstore data schema"""
    return StructType([
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

@pytest.fixture
def mock_dbutils():
    """Mock dbutils for testing"""
    mock = Mock()
    mock.widgets.get.return_value = "test_value"
    return mock