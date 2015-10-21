# -*- coding: utf-8 -*-

from boto3.session import Session
from storage_provisioner.storage import Storage, S3Storage


class StorageProvisioner(object):
    """
        Abstract class. Creates and provisions storage endpoints for arbitrary client data.
    """

    def __init__(self):
        pass

    def provision_storage(self) -> Storage:
        raise NotImplementedError


# region Amazon AWS S3 Provisioner

AWS_S3_POLICY_TEMPLATE = """{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Action":[
            "s3:PutObject",
            "s3:PutObjectAcl",
            "s3:PutObjectAclVersion",
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:DeleteObject",
            "s3:DeleteObjectVersion"
         ],
         "Resource":"arn:aws:s3:::{bucket}/{path}*"
      },
      {
         "Effect":"Allow",
         "Action":[
            "s3:ListBucket",
            "s3:GetBucketLocation",
            "s3:ListAllMyBuckets"
         ],
         "Resource":"arn:aws:s3:::{bucket}/{path}"
      }
   ]
}
"""


class S3StorageProvisioner():
    """
        Creates and provisions AWS S3 storage endpoints for arbitrary client data.
    """

    def __init__(self,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 default_region_name: str=None,
                 default_policy: str=None):

        """
        These are the minimum parameters needed by boto3 in order to provision new S3 buckets and IAM users.

        :param aws_access_key_id:
        :param aws_secret_access_key:
        :param default_region_name:
        :param default_policy:
        :return:
        """

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.default_region_name = default_region_name
        self.default_policy = default_policy

    def provision_storage(self,
                          bucket_name: str,
                          path: str,
                          region_name: str=None,
                          policy: str=None) -> S3Storage:
        """
        This method provisions a new IAM users capable of read/write access to the bucket and path.

        :param bucket_name:
        :param path:
        :param region_name:
        :param policy:
        :return:
        """

# endregion

