#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
import json
import re
from models import storage
class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def default(self, line):
        """Catch commands if nothing else matches then."""
        self._precmd(line)

    def _precmd(self, line):
        # Split the string to get the class, method and arg
        matches = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not matches:
            return line
        class_name = matches.group(1)
        method_name = matches.group(2)
        args = matches.group(3)
        print("{} {} {}".format(method_name, class_name, args))
        # split the arg to get the id of the instance and the arguments
        uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if uid_and_args:
            uid = uid_and_args.group(1)
            attr_or_dict = uid_and_args.group(2)
        else :
            # if the split fails it means there is only the uid
            uid = args
            attr_or_dict = False
        attr_val = ""
        if method_name == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(class_name, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
            '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_val  = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = "{} {} {} {}".format(method_name, class_name, uid, attr_val) 
        print(command)
        self.onecmd(command)
        return super()._precmd(command)
        #return command
    
    def update_dict(class_name, uid, attr_dict):    
        attr = attr_dict.replace("'", '"')
        my_dict = json.loads(attr)

        if not class_name:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(class_name, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attrs = storage.attributes()[class_name]
                for attr, value in my_dict.items():
                    if attr in attrs:
                        value = attrs[attr](value)
                    setattr(storage.all()[key], attr, value)
                storage.all()[key].save()
        
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
        elif arg not in storage.classes():
            print("** class doesn't exist **")
        else:
            new_model = storage.classes()[arg]()
            new_model.save()
            print(new_model.id)

    def do_show(self, arg):
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])

                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])
    
    def do_destroy(self, arg):
        """Destroy an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()


    def do_all(self, arg):
        """Prints all string representation of instances based on the class name."""
    
        if arg:
            args = arg.split(' ')
            if args[0] not in storage.classes():  # Add more class names as needed
                print("** class doesn't exist **")
            else:
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == args[0]]
                print(nl)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)
            
    
    def do_update(self, arg):
        """Update an instance based on the class name and id"""

        if arg == "" or arg is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, arg)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))






if __name__ == '__main__':
    HBNBCommand().cmdloop()
