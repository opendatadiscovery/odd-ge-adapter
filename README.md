## ODD Great Expectations adapter

ODD Great Expectations adapter is used for extracting data quality test and data quality test run info and metadata from Great Expectations. This adapter is implemetation of push model (see more https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#discovery-models). After installation, your GE will push new data QT on every suite save, and data QT runs on every validations run.

#### Data entities:
| Entity type | Entity source |
|:----------------:|:---------:|
|Data quality test|DAG|
|Data quality test run|DAG's runs|

For more information about data entities see https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#data-model-specification

## Quickstart
#### Installation
```
pip3 install odd-ge
```
#### Usage
```Python
from odd_ge import DataContext

context = DataContext(os.path.join(BASE_DIR, 'great_expectations'))
suite = context.get_expectation_suite("suite_name")
suite.expectations = []                                                                                                                                           
batch_kwargs = {
  'data_asset_name': 'titanic_pivot', 
  'datasource': 'PandasDatasource',                                                                                                                               
  'path': os.path.join(BASE_DIR, 'data/titanic_pivot.parquet')
}
batch = context.get_batch(batch_kwargs, suite)                                                                                                                       
batch.head() 

# Add your expectations

batch.save_expectation_suite(discard_failed_expectations=False) # Add quality tests to platform
results = context.run_validation_operator("action_list_operator", assets_to_validate=[batch]) # Add quality tests runs to platform
```


## Advanced configuration
All configuration must be inside settings.py
```Python
CATALOG_URL = os.getenv("CATALOG_URL", None)

CLOUD_TYPE = os.getenv("CLOUD_TYPE", "aws")
CLOUD_REGION = os.getenv("CLOUD_REGION", "region_id")
CLOUD_ACCOUNT = os.getenv("CLOUD_ACCOUNT", "account_id")

CLOUD = {
    "type": CLOUD_TYPE,
    "region": CLOUD_REGION,
    "account": CLOUD_ACCOUNT
}
```

## Requirements
- Python 3.8
- Great Expectations  >= 0.13.28
