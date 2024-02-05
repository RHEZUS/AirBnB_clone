#!/usr/bin/python3
"""FileStorage that serializes instances to a JSON file
and deserializes JSON file to instances"""

import json
from models.base_model import BaseModel

class FileStorage:
    """Represent storage engine."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id
        """
        new_name = obj.__class__.name
        FileStorage.__object["{}.{}".format(new_name, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)
        """
        path_save = FileStorage.__objects
        path_self = {obj: path_save[obj].to_dict() for obj in path_save.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(path_self, f)

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists
        otherwise, do nothing. If the file doesn’t exist, no exception should be raised)
        """

