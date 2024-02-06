#!/usr/bin/python3
"""
Contains the BaseModel module
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """BaseModel class"""
    def __init__(self, *args, **kwargs):
        """Constructor method"""

        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    
    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        self.updated_at = datetime.now()
        storage.save()
        

    def to_dict(self):
        diction = self.__dict__.copy()
        diction ['__class__'] = self.__class__.__name__
        diction['created_at'] = datetime.isoformat(diction['created_at'])
        diction['updated_at'] = datetime.isoformat(diction['updated_at'])
        return diction
