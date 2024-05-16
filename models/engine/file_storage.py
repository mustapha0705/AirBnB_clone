#!/usr/bin/python3
"""Models for the FileStorage class"""
from models.base_model import BaseModel
import json
import os

class FileStorage:
    """Class to serialize and Deserialize python objects"""
    __file_path = 'file.json'
    __objects = {}
    
    def all(self):
        """Returns the __objects dictionary"""
        return self.__objects
    
    def new(self, obj):
        """Adds the object to the __objects dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
    
    def save(self):
        """Serializes __objects to JSON file, __file_path"""
        #create new dictionary to store serialized object
        serialized_objects = {}
        
        #iterate over each key-value pair in __objects and convert the object to a dictionary
        for key, value in self.__objects.items():
            serialized_objects[key] = value.to_dict()
        
        #Open the __file_path and serialize the serialized objects to JSON and store in the file
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)
    
    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, encoding='utf-8') as file:
                loaded_dictionary = json.load(file)
            for key, value in loaded_dictionary.items():
                class_name = eval(value["__class__"])
                self.__objects[key] = class_name
        else:
            pass
