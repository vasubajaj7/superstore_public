# Superstore Data Pipeline

A minimal Databricks project for processing superstore dataset using Asset Bundles.

## Architecture

```
Raw Volume → Stage Schema → Processed Schema
     ↓            ↓              ↓
   CSV Files → Autoloader → Manual Processing
```

## Project Structure

```
├── databricks.yml          # Bundle configuration
├── resources/              # Resource definitions
│   ├── catalog.yml         # Empty (infrastructure via notebook)
│   ├── jobs.yml           # Jobs configuration
│   └── src/               # Notebooks
│       ├── setup_catalog.py    # Infrastructure setup
│       └── load_raw_to_stage.py # Data loading
├── data/                  # Sample data
└── .github/workflows/     # CI/CD pipeline
```

## Setup

1. **Configure Databricks CLI**
   ```bash
   databricks configure --token
   ```

2. **Deploy to Development**
   ```bash
   databricks bundle deploy --target dev
   ```

## Data Pipeline

### 1. Infrastructure Setup
- **Catalog**: `superstore_dev` (dev) / `superstore` (prod)
- **Schemas**: `stage`, `processed`
- **Volume**: `raw` (in stage schema)

### 2. Data Flow
1. **Setup**: Run "Setup Infrastructure" job to create catalog/schemas/volume
2. **Ingestion**: Run "Superstore Data Ingestion" job to load CSV to stage table

## CI/CD

GitHub Actions workflow:
- **Deploy**: Auto-deploy bundle on push to dev/main
- **Execute**: Run setup and ingestion jobs automatically

## Environment Variables

Set these in GitHub Secrets:
- `DATABRICKS_HOST`: Your Databricks workspace URL
- `DATABRICKS_TOKEN`: Personal access token