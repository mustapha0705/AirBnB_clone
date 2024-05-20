import unittest
from unittest.mock import patch, mock_open, MagicMock
from models.base_model import BaseModel
from models.file_storage import FileStorage
import json
import os

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        """Set up test methods."""
        self.storage = FileStorage()
        self.model = BaseModel()
        self.model.id = "123456"
        self.model_dict = self.model.to_dict()

    def tearDown(self):
        """Clean up after tests."""
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.storage.new(self.model)
        self.assertEqual(self.storage.all(), {"BaseModel.123456" : self.model})

    def test_new(self):
        self.storage.new(self.model)
        key = "BaseModel.123456"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], self.model)

    @patch('models.file_storage.open', new_callable=mock_open)
    @patch('models.file_storage.json.dump')
    def test_save(self, mock_json_dump, mock_open_file):
        self.storage.new(self.model)
        self.storage.save()
        mock_open_file.assert_called_once_with('file.json', 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with({"BaseModel.123456": self.model_dict}, mock_open_file())

    @patch('models.file_storage.open', new_callable=mock_open, read_data='{"BaseModel.123456": {"__class__": "BaseModel", "id": "123456"}}')
    @patch('os.path.exists', return_value=True)
    def test_reload(self, mock_exists, mock_open_file):
        self.storage.reload()
        self.assertIn("BaseModel.123456", self.storage.all())
        self.assertIsInstance(self.storage.all()["BaseModel.123456"], BaseModel)

    @patch('os.path.exists', return_value=False)
    def test_reload_method_no_file(self, mock_exists):
        self.storage.reload()
        self.assertEqual(self.storage.all(), {})

    if __name__ == '__main__':
        unittest.main()