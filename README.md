## ODD GreatExpectation adapter

Library for GreatExpectation schema compatible json files for suites and validation, reads them from s3 storage and ingests to OpenDataDiscovery platform.

Suites must include special metadata about folder with data which will be validated in the future.
Example 
```json
{
  "expectation_suite_name": "notification",
  ...
  "meta": {
    "batch_kwargs": {
      ...
      "odd_metadata": [
        "s3://bucket/folder"
      ]
    }
  }
}
```

Validation results must include metadata about which file was validated.
Example
```json
{
  "meta": {
    "batch_kwargs": {
      ...
      "odd_metadata": [
        "s3://bucket/folder/file.csv"
      ]
    },
    ...
    "validation_time": "20220525T174015.717924Z"
  },
  "results": [...],
  "success": true
}
```

### Library usage
Install package
```bash
pip install odd-ge-adapter
```

Example:
```
from odd_models.api_client import ODDApiClient
from odd_ge_adapter.domain.plugin import S3StoragePlugin
from odd_ge_adapter.adapters.s3.adapter import Adapter

platform = ODDApiClient(<PLATFORM_URL>)

# aws credentials can be omitted and taken from the ENV variables 
config = S3StoragePlugin(
    type="s3",
    name="s3_storage",
    bucket="",
    results_key="",
    suites_key="",
    # aws_region="",
    # aws_access_key_id="",
    # aws_secret_access_key="",
)

adapter = Adapter(config)
platform.post_data_entity_list(data=adapter.get_data_entity_list())
```


### As collector usage
In progress...

