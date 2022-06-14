from odd_ge_adapter.domain import S3Uri

FOLDER_PATH = "s3://bucket/folder"
NESTED_FOLDER_PATH = "s3://bucket/folder1/folder2"

# TODO: check if passed file,because now s3-adapter only works with folders
FILE_PATH = "s3://bucket/folder/file.parquet"


def test_s3_folder_path():
    s3_uri = S3Uri(FOLDER_PATH)

    assert s3_uri.schema == "s3"
    assert s3_uri.bucket == "bucket"
    assert s3_uri.path == "folder"


def test_s3_nested_folder_path():
    s3_uri = S3Uri(NESTED_FOLDER_PATH)

    assert s3_uri.schema == "s3"
    assert s3_uri.bucket == "bucket"
    assert s3_uri.path == "folder1:folder2"
