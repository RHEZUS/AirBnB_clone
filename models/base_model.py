#!/usr/bin/python3
"""
Contains the BaseModel module
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    BaseModel class
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor method
        """

        if args:
            self.id = args[0]
            self.created_at = args[1]
            self.updated_at = args[2]

        elif not args and kwargs:
            self.id = kwargs.get('id', str(uuid.uuid4()))
            self.created_at = datetime.strptime(kwargs.get('created_at', ''), '%Y-%m-%dT%H:%M:%S.%f') or datetime.now()
            self.updated_at = datetime.strptime(kwargs.get('updated_at', ''), '%Y-%m-%dT%H:%M:%S.%f') or datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
    
    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        storage.new(self)
        storage.save()
        self.updated_at = datetime.now()

    def to_dict(self):
        diction = self.__dict__
        diction['created_at'] = datetime.isoformat(diction['created_at'])
        diction['updated_at'] = datetime.isoformat(diction['updated_at'])
        diction ['__class__'] = self.__class__.__name__

        return diction
