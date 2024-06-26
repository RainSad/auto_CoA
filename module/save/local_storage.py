import json
import os
import sys
from typing import Any
from module.utils.path_utils import PathUtils


class LocalStorage:
    """
    本地存储对象
    """

    def __init__(self, name: str):
        self.__json_file = name + ".json"
        self.__json_file = os.path.join(PathUtils.get_base_dir(), self.__json_file)
        try:
            with open(self.__json_file, "r") as json_file:
                self.__dict = json.load(json_file)
        except FileNotFoundError:
            try:
                sys_default = os.path.join(PathUtils.get_base_dir(), "sys_default.json")
                print("--------------")
                print(sys_default)
                with open(sys_default, "r", encoding='utf-8') as json_file:
                    self.__dict = json.load(json_file)
            except FileNotFoundError:
                self.__dict = {}

    def set_item(self, key: str, value: Any):
        """
        存储数据
        """
        self.__dict[key] = value
        self._save()

    def get_item(self, key: str, default=None):
        """
        读取数据
        """
        return self.__dict.get(key, default)

    def remove_item(self, key: str):
        """
        移除键值对
        """
        if key in self.__dict:
            del self.__dict[key]
            self._save()

    def clear(self):
        """
        清空数据
        """
        self.__dict = {}
        self._save()

    def _save(self):
        """
        保存
        """
        with open(self.__json_file, "w") as json_file:
            json.dump(self.__dict, json_file, indent=4)


sys.path.append("..\\..\\auto_CoA")
from module.base.singleton import Singleton


class LocalStorageMgr(Singleton):
    """
    本地存储管理器
    """

    def __init__(self):
        self.__storage_dict = {}

    def getLocalStorage(self, name='user_default') -> LocalStorage:
        """
        获取本地存储对象
        """
        if name not in self.__storage_dict:
            self.__storage_dict[name] = LocalStorage(name)
        return self.__storage_dict[name]
