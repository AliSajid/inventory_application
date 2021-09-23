import os

from aws_cdk import aws_s3 as s3, core as cdk
from chalice.cdk import Chalice


RUNTIME_SOURCE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.pardir, "runtime"
)


class ChaliceApp(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.s3_bucket = self._create_s3_bucket()
        self.chalice = Chalice(
            self,
            "ChaliceApp",
            source_dir=RUNTIME_SOURCE_DIR,
            stage_config={
                "environment_variables": {
                    "INVENTORY_BUCKET_NAME": self.s3_bucket.bucket_name
                }
            },
        )
        self.s3_bucket.grant_read_write(self.chalice.get_role("DefaultRole"))

    def _create_s3_bucket(self):
        """

        """

        bucket = s3.Bucket(
        self,
        id = "inventory-app.banseljaj.com"
        )
        cdk.CfnOutput(self, "AppBucketName", value=bucket.bucket_name)
        return bucket
