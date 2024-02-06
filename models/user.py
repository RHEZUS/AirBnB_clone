#!/usr/bin/python3

from models.base_model import BaseModel

"""
Contains the module user
"""

class User(BaseModel):
    """The user Model"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
    