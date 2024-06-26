#!/usr/bin/python3
"""
Model: base_model.py
"""
import models
import uuid
from datetime import datetime


class BaseModel:
    """The base class that the other classes inherit from"""
    def __init__(self, *args, **kwargs):
        """Defines public instance attributes"""
        # Create an instance of BaseModel from a dictionary
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                # __class__ should not be added as an attribute
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            # Adds the new object to the __objects dictionary
            # with classname.id as a Key
            models.storage.new(self)

    def __str__(self):
        """Returns class name, the id, and available
        attributes as key-value pairs"""
        return "[{}] ({} {})".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Method to update the time of method instances"""
        self.updated_at = datetime.now()

        # Serializes the object into a JSON file
        models.storage.save()

    def to_dict(self):
        """Method to convert an instaces of the BaseModel
        class to key-value pair dictionaries"""
        dic_copy = self.__dict__.copy()
        dic_copy["__class__"] = self.__class__.__name__
        dic_copy["created_at"] = self.created_at.isoformat()
        dic_copy["updated_at"] = self.updated_at.isoformat()

        # Returns the dictionary
        return dic_copy
