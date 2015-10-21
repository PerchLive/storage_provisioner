# -*- coding: utf-8 -*-

from boto3.session import Session
from storage_provisioner.storage import Storage, S3Storage, AWSS3Region


class StorageProvisioner(object):
    """
        Abstract class. Creates and provisions storage endpoints for arbitrary client data.
    """

    def __init__(self):
        pass

    def provision_storage(self) -> Storage:
        raise NotImplementedError


# region Amazon AWS Constants

DEFAULT_AWS_S3_REGION = AWSS3Region.USWest1

DEFAULT_AWS_S3_POLICY_TEMPLATE = """{
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
# endregion

# region Amazon AWS S3 Provisioner


class S3StorageProvisioner:
    """
        Creates and provisions AWS S3 storage endpoints for arbitrary client data.
    """

    def __init__(self,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 default_region: AWSS3Region = DEFAULT_AWS_S3_REGION,
                 default_policy: str = None):
        """
        These are the minimum parameters needed by boto3 in order to provision new S3 buckets and IAM users.

        :param aws_access_key_id:
        :param aws_secret_access_key:
        :param default_region:
        :param default_policy:
        :return:
        """

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.default_region = default_region
        self.default_policy = default_policy

    def provision_storage(self,
                          user_name: str,
                          bucket_name: str,
                          path: str = None,
                          region: AWSS3Region = None,
                          policy: str = None,
                          duration_sec: int = 129600) -> S3Storage:
        """
        This method provisions a new IAM users capable of read/write access to the S3 bucket and path, creating the
        bucket if necessary.

        This method must be called with one of :param policy OR :param path set.
        If policy is None, a default policy with PUT / GET / DELETE access to :param path within :param bucket_name
        will be used.

        :param user_name: the user name to associate with this credential in AWS. Will be truncated to 32 characters.
        :param bucket_name: the S3 bucket name. A bucket with this name will be created if necessary.
        :param path: a path within the bucket, omitting leading '/', where access is scoped if policy is None.
        :param region: the region where the S3 bucket should be created if necessary. DEFAULT_AWS_S3_REGION if None.
        :param policy: a custom AWS access policy which will be used as-is to scope credentials.
        :param duration_sec: the duration of the returned credentials. If using root AWS credentials, the maximum
        duration is one hour. If an IAM user is used, the maximum duration is 36 hours. If None the maximum available
        duration will be used.
        :return:
        """

        # TODO : Sanitize arguments?

        region_name = (region if region is not None else self.default_region).value

        session = Session(aws_access_key_id=self.aws_access_key_id,
                          aws_secret_access_key=self.aws_secret_access_key,
                          region_name=region_name)

        s3 = session.resource('s3')

        # TODO : Validate region_name. Respond to error e.g: invalid bucket name
        bucket = s3.create_bucket(Bucket=bucket_name,
                                  CreateBucketConfiguration={'LocationConstraint':
                                                             region_name})

        aws_policy = policy if policy is not None else DEFAULT_AWS_S3_POLICY_TEMPLATE.replace('{bucket}', bucket_name)\
                                                                                     .replace('{path}', path)

        sts = session.client('sts')
        token_resp = sts.get_federation_token(Name=user_name[:32],
                                              Policy=aws_policy,
                                              DurationSeconds=duration_sec)

        aws_creds = token_resp.Credentials
        aws_federated_user = token_resp.FederatedUser

        return S3Storage(bucket_name,
                         region_name,
                         self.aws_access_key_id,
                         self.aws_secret_access_key,
                         aws_creds.SessionToken,
                         aws_creds.Expiration,
                         aws_federated_user.FederatedUserId,
                         aws_federated_user.Arn,
                         aws_policy)

# endregion
