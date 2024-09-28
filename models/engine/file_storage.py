#!/usr/bin/python3
"""
This is the file storage class for AirBnB

This class serializes instances to a JSON file and deserializes JSON file to instances.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """
    This class serializes instances to a JSON file and deserializes JSON file to instances.

    Attributes:
        __file_path (str): path to the JSON file
        __objects (dict): objects will be stored
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of objects.

        Args:
            cls (class, optional): class of objects to return. Defaults to None.

        Returns:
            dict: dictionary of objects
        """
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace('.', ' ')
                partition = shlex.split(partition)
                if partition[0] == cls.__name__:
                    dic[key] = self.__objects[key]
            return dic
        else:
            return self.__objects


    def new(self, obj):
        """
        Sets __object to given obj.

        Args:
            obj (object): given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj


    def save(self):
        """
        Serialize the file path to JSON file path.
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)


    def reload(self):
        """
        Deserialize the file path to JSON file path.
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in json.load(f).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass


    def delete(self, obj=None):
        """
        Delete an existing element.

        Args:
            obj (object, optional): object to delete. Defaults to None.
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]


    def close(self):
        """
        Calls reload().
        """
        self.reload()
