from odd_ge_adapter.domain.s3_uri import S3Uri
from oddrn_generator.generators import S3Generator


def s3_uri_to_oddrn(s3_uri: S3Uri, oddrn: S3Generator):
    oddrn.set_oddrn_paths(buckets=s3_uri.bucket, keys=s3_uri.path)
    return oddrn.get_oddrn_by_path("keys")
