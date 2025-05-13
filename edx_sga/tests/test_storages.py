
"""
Unit tests for django-storages
"""

from unittest import TestCase

from django.conf import settings
from django.test.utils import override_settings
from storages.backends.s3boto3 import \
    S3Boto3Storage  # pylint: disable=wrong-import-order

from edx_sga.utils import get_default_storage


class S3Boto3TestCase(TestCase):
    """Unit tests for verifying the S3Boto3 storage backend selection logic"""

    def setUp(self):
        self.storage = S3Boto3Storage()

    def test_default_backend(self):
        storage = get_default_storage()
        storage_class = storage.__class__

        self.assertIn(
            f"{storage_class.__module__}.{storage_class.__name__}",
            [
                'django.core.files.storage.FileSystemStorage',
                'django.core.files.storage.filesystem.FileSystemStorage',
            ]
        )

    @override_settings(SGA_STORAGE_SETTINGS={
        'STORAGE_CLASS': 'storages.backends.s3boto3.S3Boto3Storage',
        'STORAGE_KWARGS': {
            'bucket_name': 'test',
            'default_acl': 'public',
            'location': 'abc/def'
        }
    })
    def test_backend_with_params(self):
        storage = get_default_storage()
        self.assertIsInstance(storage, S3Boto3Storage)
        self.assertEqual(storage.bucket_name, "test")
        self.assertEqual(storage.default_acl, 'public')
        self.assertEqual(storage.location, "abc/def")
