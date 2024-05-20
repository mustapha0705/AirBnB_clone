#!/usr/bin/python3
"""
Module: file_storage.py

Defines a `FileStorage` class.
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity

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
        
        #the obj object is set in __object with key className.id
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
        # Check if the JSON file exists
        if os.path.exists(self.__file_path):
            # Open the JSON file in read mode with utf-8 encoding
            with open(self.__file_path, encoding='utf-8') as file:
                loaded_dictionary = json.load(file)
            # Iterate over each key-value pair in the loaded dictionary
            for key, value in loaded_dictionary.items():
                cls = eval(value["__class__"])
                obj = cls(**value)
                # Recreate the object and store it in __objects dictionary
                self.__objects[key] = obj
        else:
            # If the file does not exist, do nothing
            pass