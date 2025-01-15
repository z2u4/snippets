from functools import cache
import os
import json
from hashlib import sha256

class JsonProperty:
    @staticmethod    
    def _default_load_method(path):
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod    
    def _default_save_method(path, value):
        with open(path, "w") as f:
            json.dump(value, f, indent=4)
    
        
    def __init__(self, key: str):
        self.key = key

    def __get_real_content__(self, instance):
        path = getattr(instance, "__JSON_PATH__")
        load_method = getattr(instance, "__JSON_LOAD_METHOD__", self._default_load_method)
        return load_method(path)
    
    def __need_refresh__(self, instance):
        path = getattr(instance, "__JSON_PATH__")
        mdate = getattr(instance, "__JSON_MDATE__", None)
        if mdate is None or os.path.getmtime(path) != mdate:
            setattr(instance, "__JSON_MDATE__", os.path.getmtime(path))
            return True
        
        sha256_hash = getattr(instance, "__JSON_SHA256_HASH__", None)
        
        s = sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                s.update(chunk)
        
        if sha256_hash is None or s.hexdigest() != sha256_hash:
            setattr(instance, "__JSON_SHA256_HASH__", s.hexdigest())
            return True
        return False

    def __fetch_content__(self, instance):
        content = getattr(instance, "__JSON_CONTENT__", None)
        if content is not None and not self.__need_refresh__(instance):
            return content

        content = self.__get_real_content__(instance)
        setattr(instance, "__JSON_CONTENT__", content)
        return content

    def __get__(self, instance, owner):
        if not instance:
            return
        
        content = self.__fetch_content__(instance)
        return content.get(self.key)

    def __set__(self, instance, value):
        path = getattr(instance, "__JSON_PATH__")
        content = self.__fetch_content__(instance)
        content[self.key] = value
        getattr(instance, "__JSON_SAVE_METHOD__", self._default_save_method)(path, content)
        setattr(instance, "__JSON_CONTENT__", content)

class JsonObj1:
    __JSON_PATH__ : str

    def __getattr__(self, key : str):
        if key.startswith("_"):
            return super().__getattribute__(key)
        
        setattr(self, key, JsonProperty(key))

        return getattr(self, key).__get__(self, type(self))


class JsonObj2:
    __JSON_PATH__ : str

    @cache
    def __getitem__(self, key : str):
        return JsonProperty(key).__get__(self, type(self))