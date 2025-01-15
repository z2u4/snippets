import os

from .utils import JsonObj1

preferences_path = os.path.join(
    os.getenv("APPDATA"), "masscode", "v2", "preferences.json"
)

class _Preferences(JsonObj1):
    __JSON_PATH__ = preferences_path

    storagePath : str

preferences = _Preferences()