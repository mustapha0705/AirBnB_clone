#!/usr/bin/python3
"""This module defines the entry point of the command interpreter.

It defines one class, `HBNBCommand()`, which sub-classes the `cmd.Cmd` class.
This module defines abstractions that allows us to manipulate a powerful
storage system (FileStorage / DB). This abstraction will also allow us to
change the type of storage easily without updating all of our codebase.

It allows us to interactively and non-interactively:
    - create a data model
    - manage (create, update, destroy, etc) objects via a console / interpreter
    - store and persist objects to a file (JSON file)

Typical usage example:

    $ ./console
    (hbnb)

    (hbnb) help
    Documented commands (type help <topic>):
    ========================================
    EOF  create  help  quit
    (hbnb)
    (hbnb) quit
    $
"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity

class_names = ["BaseModel", "User", "State",
               "City", "Amenity", "Place", "Review"]


class HBNBCommand(cmd.Cmd):
    """The command interpreter.

    This class represents the command interpreter, and the control center
    of this project. It defines function handlers for all commands inputted
    in the console and calls the appropriate storage engine APIs to manipulate
    application data / models.

    It sub-classes Python's `cmd.Cmd` class which provides a simple framework
    for writing line-oriented command interpreters.
    """
    prompt = "(hbnb) "

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        if len(arg) < 1:
            print("** class name missing **")
            return

        elif arg in class_names:
            print(arg)
            class_instance = globals()[arg]()
            class_instance.save()
            print(class_instance.id)

        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints an instance based on class name and id"""
        args = arg.split()
        if len(arg) < 1:
            print("** class name missing **")
            return

        if args[0] not in class_names:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        obj_intsance = storage.all()

        key = "{}.{}".format(args[0], args[1])
        requested_instance = obj_intsance.get(key)
        if not requested_instance:
            print("** no instance found **")
            return
        print(requested_instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()

        if len(arg) < 1:
            print("** class name missing **")
            return

        if args[0] not in class_names:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        obj_instance = storage.all()
        key = "{}.{}".format(args[0], args[1])

        requested_instance = obj_instance.get(key)
        if not requested_instance:
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of
        all instances based or not on the class name."""
        if arg and arg not in class_names:
            print("** class doesn't exist **")
            return

        obj_instances = storage.all()
        obj_list = []

        if arg:
            for key, obj in obj_instances.items():
                if key.startswith(arg + "."):
                    obj_list.append(str(obj))
        else:
            for obj in obj_instances.values():
                obj_list.append(str(obj))

        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name
        and id by adding or updating attribute."""
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in class_names:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        if len(args) > 4:
            print("** too many arguments **")
            return

        class_name, instance_id, attribute_name, attribute_value = args
        key = "{}.{}".format(class_name, instance_id)
        obj_instances = storage.all()

        if key not in obj_instances:
            print("** no instance found **")
            return

        instance = obj_instances[key]

        if attribute_name in ["id", "created_at", "updated_at"]:
            print("** can't update {} **".format(attribute_name))
            return

        # Cast attribute_value to the correct type
        if hasattr(instance, attribute_name):
            attr_type = type(getattr(instance, attribute_name))
            try:
                if attr_type == int:
                    attribute_value = int(attribute_value)
                elif attr_type == float:
                    attribute_value = float(attribute_value)
                else:
                    attribute_value = str(attribute_value)
            except ValueError:
                print("** value type mismatch **")
                return

        setattr(instance, attribute_name, attribute_value)
        instance.save()

    def do_help(self, arg):
        """To get help on a command, type help <topic>."""
        return super().do_help(arg)

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """Inbuilt EOF command to calmly catch errors."""
        return True

    def emptyline(self):
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
