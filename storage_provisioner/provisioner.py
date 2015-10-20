# -*- coding: utf-8 -*-

import boto3
from storage_provisioner import storage

class StorageProvisioner(object):
    """
        Creates and provisions storage endpoints for arbitrary client data.
    """

    def __init__(self):
        pass

    def provision_storage(self):
        pass

class S3StorageProvisioner():
    """
        Creates and provisions AWS S3 storage endpoints for arbitrary client data.
    """

    def __init__(self, aws_access_key, aws_access_secret, default_policy):
        # TODO
        pass

    def provision_storage(self, policy=None, aws_region=None, bucket_path='/', bucket_name=None):
        """
            Provision a storage entity, returning Storage
        """
