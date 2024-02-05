#!/usr/bin/python3
import uuid
from datetime import datetime


"""
Contains the BaseModel module
"""

class BaseModel:
    """
    BaseModel class
    """

    def __init__(self):
        """
        Constructor method
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.update_at = datetime.now()
    
    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        self.update_at = datetime.now()

    def to_dict(self):
        diction = self.__dict__
        diction ['__class__'] = self.__class__.__name__
        return diction