#!/usr/bin/python3
import cmd
import shlex
from models.base_model import BaseModel
import json
import re
from models import storage
class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "

    def precmd(self, line):
        split_lne = shlex.shlex(line , posix=True)
        split_lne.whitespace = ['.', '(', ')']
        split_lne.whitespace_split = True
        result = list(split_lne)
        if len(result) < 2:
            return line
        class_name = result[0]
        method_name = result[1]
        if len(list(result)) == 2:
            line = "{} {}".format(method_name, class_name)
            return line
        args = result[2].split(',', 1)
        uid = args[0]
        if len(args) == 1:
            line = line = "{} {} {}".format(method_name, class_name, uid)
            return line

        if method_name == 'update' and '{' in args[1]:
            #print(args[1])
            args[1].replace('{', '{"')
            dic_arg =  args[1].replace('{', '{"').replace(', ', '":"').replace('}', '"}')
            #print(dic_arg)
            self.update_dict(class_name, uid, str(dic_arg))
            return ""
        elif method_name == 'update' and '{' not in args[1]:
            parts = args[1].split(', ')
            attr = parts[0] if parts[0] else ""
            val = parts[1] if parts[1] else ""

            # Format the parts with double quotes
            line  = '{} {} {}{} "{}"'.format(method_name, class_name, uid, attr,  val)
            #print(line)
            return line

        return ""


    def update_dict(self, class_name, uid, attr_dict):    
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
            return
        else:
            args = arg.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
                return
            elif len(args) < 2:
                print("** instance id missing **")
                return
            else:
                key = "{}.{}".format(args[0], args[1])

                if key not in storage.all():
                    print("** no instance found **")
                    return
                else:
                    print(storage.all()[key])
    
    def do_destroy(self, arg):
        """Destroy an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        else:
            args = arg.split(' ')
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
                return
            elif len(args) < 2:
                print("** instance id missing **")
                return
            else:
                key = "{}.{}".format(args[0], args[1])
                if key not in storage.all():
                    print("** no instance found **")
                    return
                else:
                    del storage.all()[key]
                    storage.save()


    def do_all(self, arg):
        """Prints all string representation of instances based on the class name."""
    
        if arg:
            args = arg.split(' ')
            if args[0] not in storage.classes():  # Add more class names as needed
                print("** class doesn't exist **")
                return
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
        elif not classname:
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
