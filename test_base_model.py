    def precmd(self, line):
        split_line = shlex.shlex(line , posix=True)
        split_line.whitespace = ['.', '(', ')']
        split_line.whitespace_split = True

        result = list(split_line)
        print(result)
        if len(result) < 2:
            return super().precmd(line)
        class_name = result[0]
        method_name = result[1]
        if len(list(result)) == 2:
            line = "{} {}".format(method_name, class_name)
            return super().precmd(line)
        args = result[2].split(',', 1)
        uid = args[0]
        if len(args) == 1:
            line = line = "{} {} {}".format(method_name, class_name, uid)
            return super().precmd(line)

        if method_name == 'update' and '{' in args[1]:
            #print(args[1])
            dic_arg = {}
            if len(args) > 1:
                try:
                    dic_arg = eval(args[1])
                    print(dic_arg)
                except Exception as e:
                    print(args[1])
                    print(f"Error: {e}")
                    return ""
            else:
                print("No arguments provided.")
            #dic_arg = eval(args[1])
            #print(dic_arg)
            print(uid)
            self.update_dict(class_name, uid, str(dic_arg))
            return ""
        elif method_name == 'update' and '{' not in args[1]:
            parts = args[1].split(', ')
            attr = parts[0] if parts[0] else ""
            val = parts[1] if parts[1] else ""

            # Format the parts with double quotes
            line  = '{} {} {}{} "{}"'.format(method_name, class_name, uid, attr,  val)
            #print(line)
            return super().precmd(line)

        return ""
    








    
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

