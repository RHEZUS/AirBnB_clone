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
        """Serializes __objects to the JSON file (path: __file_path)."""

        serialized_objects = {}
        for key, obj in FileStorage.__objects.items():
            if isinstance(obj, dict):
                serialized_objects[key] = obj
            else:
                serialized_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(serialized_objects, f)

    def reload(self):
        from models.base_model import BaseModel
        """Deserializes the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf8") as f:
                serialized_objects = json.load(f)
                # Convert serialized objects back to instances
                FileStorage.__objects = {key: BaseModel(**value) for key, value in serialized_objects.items()}
        except (FileExistsError, FileNotFoundError, json.JSONDecodeError):
            FileStorage.__objects = {}

