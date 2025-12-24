# Databricks Project Setup - Errors, Fixes & Learnings

## Overview
This document captures all errors encountered during the Databricks superstore project setup, their root causes, fixes applied, and key learnings.

## Errors and Fixes

### 1. Bundle Command Not Found
**Error**: `No such command 'bundle'`
**Root Cause**: Using legacy Python-based `databricks-cli` package that doesn't support bundle commands
**Fix**: Switched to new Databricks CLI installation via curl script
```bash
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
```

### 2. Workspace Host Interpolation
**Error**: `Variable interpolation is not supported for fields that configure authentication`
**Root Cause**: Using `${workspace.host}` in databricks.yml authentication fields
**Fix**: Removed workspace host config from databricks.yml, rely on DATABRICKS_HOST environment variable

### 3. Unsupported Catalogs Field
**Error**: `unknown field: catalogs`
**Root Cause**: Catalogs are not supported as bundle resources in current Databricks version
**Fix**: Removed catalogs from bundle configuration, created via setup notebook instead

### 4. Circular Variable Reference
**Error**: `cycle detected in field resolution: variables.catalog_name.default -> var.catalog_name`
**Root Cause**: Self-referencing variable definition in targets section
**Fix**: Used direct string values instead of variable interpolation
```yaml
# Before: catalog_name: ${var.catalog_name}_dev
# After: catalog_name: superstore_dev
```

### 5. Missing File Extensions
**Error**: `notebook "resources/src/load_raw_to_stage" not found`
**Root Cause**: Missing .py extension in notebook paths
**Fix**: Added .py extensions to all notebook paths in jobs.yml

### 6. Incorrect Notebook Paths
**Error**: `notebook resources/src/load_raw_to_stage.py not found`
**Root Cause**: Bundle looking for notebooks in resources/src/ but files were in src/
**Fix**: Moved notebooks to resources/src/ directory where bundle expects them

### 7. Missing Catalog Dependencies
**Error**: `Catalog 'superstore_dev' does not exist`
**Root Cause**: Bundle trying to create schemas and volumes before catalog exists
**Fix**: Removed dependent resources from bundle, create all infrastructure via setup notebook

### 8. Job Execution Command Issues
**Error**: `unknown flag: --job-name`
**Root Cause**: New Databricks CLI expects job ID, not job name for run-now command
**Fix**: Used `databricks jobs list` + jq to get job ID by name first

### 9. JSON Structure Mismatch
**Error**: `Cannot index array with string "jobs"`
**Root Cause**: Incorrect jq query assuming JSON has .jobs wrapper
**Fix**: Updated jq query to match actual JSON structure without .jobs wrapper
```bash
# Before: '.jobs[] | select(.settings.name=="Job Name")'
# After: '.[] | select(.settings.name=="Job Name")'
```

### 10. Job Name Prefix Mismatch
**Error**: `Job 'Setup Infrastructure' not found`
**Root Cause**: Bundle adds environment prefixes like `[dev vasu_c_bajaj]` to job names
**Fix**: Used `contains()` instead of exact match in jq query
```bash
# Before: select(.settings.name=="Setup Infrastructure")
# After: select(.settings.name | contains("Setup Infrastructure"))
```

### 11. Serverless Compute Configuration
**Error**: Cluster configurations not compatible with Databricks free edition
**Root Cause**: Using cluster configs instead of serverless compute
**Fix**: Removed all cluster configurations, added `serverless: true` for DLT pipelines

## Key Learnings

### 1. Databricks CLI Evolution
- Legacy Python-based CLI (`databricks-cli` package) vs new Go-based CLI
- Bundle functionality only available in new CLI
- Installation method matters for feature availability

### 2. Bundle Resource Limitations
- Not all Databricks resources can be managed via bundles
- Catalogs must be created manually or via notebooks
- Dependencies between resources require careful ordering

### 3. Naming Conventions
- Bundles automatically add environment prefixes to resource names
- Format: `[target environment_username] Original Name`
- Must account for prefixes when referencing resources programmatically

### 4. Dependency Management
- Resources with dependencies (schemas depend on catalogs) need careful handling
- Hybrid approach: Use bundles for jobs/notebooks, notebooks for infrastructure

### 5. Free Edition Constraints
- Limited to serverless compute only
- No custom cluster configurations allowed
- DLT pipelines must use `serverless: true`

### 6. CI/CD Best Practices
- Always validate job existence before execution
- Use debugging output to troubleshoot deployment issues
- Handle environment-specific naming in automation scripts

### 7. JSON Processing
- Databricks CLI output structure can vary
- Always verify JSON structure before writing jq queries
- Use flexible matching (contains) for dynamic naming

## Final Architecture

The solution uses a hybrid approach:
- **Databricks Bundle**: Manages jobs and notebooks
- **Setup Notebook**: Creates catalog, schemas, and volumes
- **CI/CD Pipeline**: Deploys bundle and executes jobs automatically
- **Serverless Compute**: Compatible with free edition constraints

## Recommendations

1. **Start Simple**: Begin with minimal bundle configuration
2. **Test Incrementally**: Deploy and test each component separately
3. **Use Debugging**: Add verbose output to troubleshoot issues
4. **Handle Dependencies**: Create infrastructure before dependent resources
5. **Account for Naming**: Use flexible matching for auto-generated names
6. **Document Constraints**: Clearly document platform limitations and workarounds