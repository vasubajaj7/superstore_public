import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import get_spark_session, check_table_exists, get_table_count, validate_data_quality

class TestUtils:
    
    @pytest.mark.unit
    def test_get_spark_session(self):
        """Test Spark session creation"""
        spark = get_spark_session()
        assert spark is not None
        assert spark.sparkContext.appName == "SuperstoreETL"
    
    @pytest.mark.unit
    def test_check_table_exists_true(self, spark, sample_superstore_data, superstore_schema):
        """Test table exists check - positive case"""
        # Create test table
        df = spark.createDataFrame(sample_superstore_data, superstore_schema)
        df.createOrReplaceTempView("test_table")
        
        result = check_table_exists(spark, "test_table")
        assert result is True
    
    @pytest.mark.unit
    def test_check_table_exists_false(self, spark):
        """Test table exists check - negative case"""
        result = check_table_exists(spark, "non_existent_table")
        assert result is False
    
    @pytest.mark.unit
    def test_get_table_count(self, spark, sample_superstore_data, superstore_schema):
        """Test getting table row count"""
        # Create test table
        df = spark.createDataFrame(sample_superstore_data, superstore_schema)
        df.createOrReplaceTempView("count_test_table")
        
        count = get_table_count(spark, "count_test_table")
        assert count == 2
    
    @pytest.mark.unit
    def test_get_table_count_non_existent(self, spark):
        """Test getting count for non-existent table"""
        count = get_table_count(spark, "non_existent_table")
        assert count == 0
    
    @pytest.mark.unit
    def test_validate_data_quality(self, spark, sample_superstore_data, superstore_schema):
        """Test data quality validation"""
        # Create test table
        df = spark.createDataFrame(sample_superstore_data, superstore_schema)
        df.createOrReplaceTempView("quality_test_table")
        
        result = validate_data_quality(spark, "quality_test_table")
        
        assert result["exists"] is True
        assert result["total_rows"] == 2
        assert "null_counts" in result
        assert isinstance(result["null_counts"], dict)
    
    @pytest.mark.unit
    def test_validate_data_quality_non_existent(self, spark):
        """Test data quality validation for non-existent table"""
        result = validate_data_quality(spark, "non_existent_table")
        assert result["exists"] is False