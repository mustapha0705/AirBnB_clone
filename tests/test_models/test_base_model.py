"""Module: test_base_model.py"""
import unittest
from datetime import datetime
import models
import uuid
from models.base_model import BaseModel
from unittest.mock import patch, MagicMock


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        """Set up test methods."""
        self.model = BaseModel()

    def test_empty_init(self):
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertNotEqual(self.model.id, '')
        try:
            uuid_obj = uuid.UUID(self.model.id, version=4)
        except ValueError:
            self.fail("id is not a valid UUID.")

    def test_init_with_kwargs(self):
        kwargs = {
            'id': '123456',
            'created_at': '2023-01-01T12:00:00.000000',
            'updated_at': '2023-01-01T12:00:00.000000'
        }
        model = BaseModel(**kwargs)
        self.assertEqual(self.model.id, '123456')
        self.assertEqual(self.model.created_at, datetime(2023, 1, 1, 12, 0, 0))
        self.assertEqual(self.model.created_at, datetime(2023, 1, 1, 12, 0, 0))

    def test_init_ignore_class(self):
        kwargs = {'__class__': 'SomeClass'}
        model = BaseModel(**kwargs)
        self.assertFalse(hasattr(model, '__class__'))

    def test_init_invalid_date_format(self):
        kwargs = {'created_at': '2023-01-01 12:00:00'}
        with self.assertRaises(ValueError):
            BaseModel(**kwargs)

    def test_init_with_complex_data_types(self):
        kwargs = {
            'dict_attr': {'key': 'value'},
            'list_attr': [1, 2, 3]
        }
        model = BaseModel(**kwargs)
        self.assertEqual(self.model.dict_attr, {'key': 'value'})
        self.assertEqual(self.model.list_attr, [1, 2, 3])

    def test_str_representation(self):
        string = str(self.model)
        expected = "[BaseModel] ({}) {}".format(
            self.model.id, self.model.__dict__)
        self.assertEqual(string, expected)

    @patch('models.storage')
    def test_save(self, mock_storage):
        original_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, original_updated_at)
        self.assertTrue(mock_storage.save.called)

    def test_to_dict(self):
        dict = self.model.to_dict()
        self.assertEqual(dict["__class__"], "BaseModel")
        self.assertEqual(dict["id"], self.model.id)
        self.assertEqual(dict["created_at"], self.model.created_at.isoformat())
        self.assertEqual(dict["updated_at"], self.model.updated_at.isoformat())

    if __name__ == '__main__':
        unittest.main()
