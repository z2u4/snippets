import os
from .utils import JsonProperty, JsonObj2
from .app import preferences

class _Db(JsonObj2):
    __JSON_PATH__ = os.path.join(preferences.storagePath, "db.json")

db = _Db()

