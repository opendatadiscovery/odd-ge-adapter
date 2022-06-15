"""
    dataset_list: [
        s3://bucket/datasets,
        s3://bucket/datasets/subfolder
    ]
"""
from urllib.parse import urlparse


class S3Uri:
    def __init__(self, path: str, join_key: str = ":"):
        self._parsed = urlparse(path)
        self._join_key = join_key

    @property
    def schema(self):
        return self._parsed.scheme

    @property
    def bucket(self):
        return self._parsed.netloc

    @property
    def path(self):
        """"""
        return self._parsed.path.lstrip("/").replace("/", self._join_key)
