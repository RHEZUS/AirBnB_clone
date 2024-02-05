#!/usr/bin/python3
"""FileStorage that serializes instances to a JSON file
and deserializes JSON file to instances"""

import json

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
        new_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(new_name, obj.id)] = obj.to_dict()

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)
        """
        objects = FileStorage.__objects
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objects, f)

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists
        otherwise, do nothing. If the file doesn’t exist, no exception should be raised)
        """
        try:
            with open(FileStorage.__file_path, "r", encoding="utf8") as f:
                FileStorage.__objects =  json.load(f)
        except FileExistsError:
            FileStorage.__objects = {}
        except FileNotFoundError:
            FileStorage.__objects = {}

