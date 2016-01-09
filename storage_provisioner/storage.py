# -*- coding: utf-8 -*-
from enum import Enum


class Storage(object):
    """
        Represents the credentials needed to access storage.
    """

    def __init__(self):
        pass


class LocalFileStorage(Storage):
    """
        Represents the credentials needed to access storage on the local filesystem.
    """

    def __init__(self, base_path: str=None):
        self.base_path = base_path
        Storage.__init__(self)
        pass


# region Amazon AWS

class AWSS3Region(Enum):
    USEast1 = 'us-east-1'
    USWest1 = 'us-west-1'
    USWest2 = 'us-west-2'

    EUWest1 = 'eu-west-1'
    EUCentral1 = 'eu-central-1'

    APSouthEast1 = 'ap-southeast-1'
    APSouthEast2 = 'ap-southeast-2'
    APNorthEast1 = 'ap-northeast-1'

    SouthAmerica1 = 'sa-east-1'


class AWSFederatedUserMixin(object):
    """
        Represents an AWS Federated User obtained by sts.get_federation_token(..)
    """

    def __init__(self,
                 aws_federated_user_id: str,
                 aws_arn: str,
                 aws_policy: str):

        self.aws_federated_user_id = aws_federated_user_id
        self.aws_arn = aws_arn
        self.aws_policy = aws_policy


class AWSCredentialMixin(object):
    """
        Represents the credentials needed for an AWS FederationToken
    """

    def __init__(self,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 aws_session_token: str,
                 aws_expiration: int):

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        self.aws_expiration = aws_expiration


class S3Storage(Storage, AWSCredentialMixin, AWSFederatedUserMixin):
    """
        Represents an AWS FederationToken granting access to an S3 data resource

        {
            'Credentials': {
                'AccessKeyId': 'string',
                'SecretAccessKey': 'string',
                'SessionToken': 'string',
                'Expiration': datetime(2015, 1, 1)
            },
            'FederatedUser': {
                'FederatedUserId': 'string',
                'Arn': 'string'
            },
            'PackedPolicySize': 123
        }
    """

    def __init__(self,
                 s3_bucket_name: str,
                 s3_bucket_region: AWSS3Region,
                 s3_bucket_path: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 aws_session_token: str,
                 aws_expiration: int,
                 aws_federated_user_id: str,
                 aws_arn: str,
                 aws_policy: str):

        self.s3_bucket_name = s3_bucket_name
        self.s3_bucket_region = s3_bucket_region
        self.s3_bucket_path = s3_bucket_path

        AWSCredentialMixin.__init__(self,
                                    aws_access_key_id,
                                    aws_secret_access_key,
                                    aws_session_token,
                                    aws_expiration)

        AWSFederatedUserMixin.__init__(self,
                                       aws_federated_user_id,
                                       aws_arn,
                                       aws_policy)

    def get_url_for_key(self, key: str) -> str:
        """
        Return a string representing the URL where the specified key would reside
        :param key: A key describing a file location, leading slash omitted. e.g: "some_folder/myfile.txt"
        :return: a fully-qualified url representing the key. e.g: "https://bucket.s3.amazonaws.com/some_folder/myfile.txt"
        """
        return "https://{}.s3.amazonaws.com/{}".format(self.s3_bucket_name, key)

# endregion
