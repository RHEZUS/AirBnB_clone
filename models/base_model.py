#!/usr/bin/python3

import uuid
from datetime import datetime
from models import storage


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
