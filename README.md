# 0x00. AirBnB clone - The console

## Project Description

- This project is our first step towards building our first full web application: the AirBnB clone
- The console folder contains the code for the interpreter
- The model folder contains the Parent class (BaseModel), the subclasses (USer, Amenity, State, PLace, Review) and the engine folder hosting the Filestorage.
- tests Folder contains all the unittest for the codes

## How to start it

### Interactive Mode
```
$ ./console.py
```

Now you are on interactive mode and you will see the prompt `(hbnb)`
input a command:

```
(hbnb) create User
```
the id of the created model will be visible in the standard output, if you do:

```
(hbnb) show User [id]
```

All the attributes of the created model will be in your screen.

use: 

```
(hbnb) help
```
For a list of usable commands, to exit press Ctrl+D or type the command quit.

### Non-Interactive Mode

The console can also be used in non-interactive mode:

```
$ echo "create User" | ./console.py

$ echo "help" | ./console.py
```

The program will create a file called: `file.json` whenever you create a new model, it'll be store in the top folder.
