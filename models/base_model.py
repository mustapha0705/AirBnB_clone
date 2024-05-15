#!/usr/bin/python3
import uuid
from datetime import datetime

class BaseModel:
    """The base class that the other classes inherit from"""
    def __init__(self):
        """Defines public instance attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Prints class name, the id, and available attributes as key-value pairs"""
        return "[{}] ({} {})".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Method to update the time of method instances"""
        self.updated_at = datetime.now()

    def to_dict(self):
        dic_copy = self.__dict__.copy()
        dic_copy["__class__"] = self.__class__.__name__
        dic_copy["created_at"] = self.created_at.isoformat()
        dic_copy["updated_at"] = self.updated_at.isoformat()
        return dic_copy
