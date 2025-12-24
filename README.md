# Superstore Data Pipeline

A comprehensive Databricks project for processing superstore dataset using modern data engineering practices.

## Architecture

```
Raw Volume → Stage Schema → Processed Schema
     ↓            ↓              ↓
   CSV Files → Autoloader → DLT Pipeline
```

## Project Structure

```
├── databricks.yml          # Bundle configuration
├── resources/              # Resource definitions
│   ├── catalog.yml         # Catalog, schemas, volumes
│   └── jobs.yml           # Jobs and DLT pipelines
├── src/                   # Source code
│   ├── load_raw_to_stage.py  # Autoloader notebook
│   ├── dlt_pipeline.py       # DLT transformations
│   └── utils.py             # Utility functions
├── tests/                 # Test suite
│   ├── conftest.py        # Test fixtures
│   ├── test_utils.py      # Unit tests
│   └── test_pipeline.py   # Integration tests
├── data/                  # Sample data
└── .github/workflows/     # CI/CD pipeline
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Databricks CLI**
   ```bash
   databricks configure --token
   ```

3. **Deploy to Development**
   ```bash
   databricks bundle deploy --target dev
   ```

## Data Pipeline

### 1. Catalog Setup
- **Catalog**: `superstore`
- **Schemas**: `stage`, `processed`
- **Volume**: `raw` (in stage schema)

### 2. Data Flow
1. **Raw → Stage**: Autoloader reads CSV files from volume
2. **Stage → Processed**: DLT pipeline with bronze/silver/gold layers

### 3. Data Quality
- Sales > 0 validation
- Quantity > 0 validation
- Profit margin calculations
- Aggregated metrics by category/region/segment

## Testing

```bash
# Run all tests
pytest

# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration
```

## CI/CD

GitHub Actions workflow:
- **Test**: Run pytest on push/PR
- **Deploy Dev**: Auto-deploy to dev on develop branch
- **Deploy Prod**: Manual approval for production deployment

## Usage

1. Upload sample data to raw volume
2. Run autoloader job to load data to stage
3. Execute DLT pipeline for processed data
4. Query gold tables for analytics

## Environment Variables

Set these in GitHub Secrets:
- `DATABRICKS_HOST`: Your Databricks workspace URL
- `DATABRICKS_TOKEN`: Personal access token