# -*- coding: utf-8 -*-

class AWSCredentialMixin(object):
    """
        Represents the credentials needed for an AWS FederationToken
    """

    def __init__(self, aws_access_key, aws_secret_key, aws_session_token, aws_expiration, policy):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_session_token = aws_session_token
        self.aws_expiration = aws_expiration
        self.policy = policy

    def revoke(self):
        # TODO : Revoke token
        pass


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

    def __init__(self, base_path=None):
        pass

class S3Storage(Storage, AWSCredentialMixin):
    """
        Represents an AWS FederationToken granting access to an S3 data resource
    """

    def __init__(self, watch_url, s3_bucket_name, s3_bucket_region, aws_access_key, aws_secret_key, aws_session_token,
                 aws_expiration):

        self.s3_bucket_name = s3_bucket_name
        self.s3_bucket_region = s3_bucket_region

        AWSCredentialMixin.__init__(self, aws_access_key, aws_secret_key, aws_session_token, aws_expiration)
