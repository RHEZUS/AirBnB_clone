#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
import json
from models import storage

class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, arg):
        """Exit the program using EOF (Ctrl+D)\n """
        print()
        return True

    def emptyline(self):
        """Do nothing on an empty line\n """
        pass
    
    def do_create(self, arg):
        if not arg:
            print("** class name missing **")
        elif arg != "BaseModel":
            print("** class doesn't exist **")
        else:
            new_base = BaseModel()
            new_base.save()
            print(new_base.id)

    def do_show(self, arg):
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        objects = storage.all()
        key = "{}.{}".format(args[0], args[1])

        if key not in objects:
            print("** no instance found **")
        else:
            print(objects[key])
    
    def do_destroy(self, arg):
        """Destroy an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(args[0], args[1])
            if key not in objects:
                print("** no instance found **")
            else:
                del objects[key]
                storage.save()


    def do_all(self, arg):
        """Prints all string representation of instances based on the class name."""
        args = arg.split()
        objects = storage.all()

        if not args:
            # Print all instances if no class name is provided
            print([str(obj) for obj in objects.values()])
        elif args[0] not in ["BaseModel"]:  # Add more class names as needed
            print("** class doesn't exist **")
        else:
            class_name = args[0]
            filtered_objects = {key: obj for key, obj in objects.items() if class_name in key}
            if not filtered_objects:
                print("** no instance found **")
            else:
                print([str(obj) for obj in filtered_objects.values()])
        
    
    def do_update(self, arg):
        """Update an instance based on the class name and id"""
        
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            instance_id = args[1]
            key = "{}.{}".format(args[0], instance_id)
            storage_objects = storage.all()
            if key not in storage_objects:
                print("** no instance found **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                attribute_name = args[2]
                attribute_value = args[3]
                instance = storage_objects[key]
                if hasattr(instance, attribute_name):
                    attribute_type = type(getattr(instance, attribute_name))
                    setattr(instance, attribute_name, attribute_type(attribute_value))
                    instance.save()
                    print(instance)

        






if __name__ == '__main__':
    HBNBCommand().cmdloop()