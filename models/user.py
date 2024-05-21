#!/usr/bin/python3
"""
Module: user.py

Defines a `User` class that inherits from `BaseModel`.
"""
from models.base_model import BaseModel


class User(BaseModel):
    """Creates a new User"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
