#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
import json
import re
from models import storage
class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "

    def default(self, line):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(line)
        

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