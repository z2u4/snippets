import pytest
import os
import json
import tempfile
from masscodepp.utils import JsonProperty

class TestJson:
    def __init__(self, json_path):
        self.__JSON_PATH__ = json_path
        self.__JSON_CONTENT__ = None
    
    name = JsonProperty("name")
    age = JsonProperty("age")

@pytest.fixture
def json_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tf:
        test_data = {"name": "John", "age": 30}
        json.dump(test_data, tf)
        temp_path = tf.name
    
    yield temp_path
    os.unlink(temp_path)

def test_read_property(json_file):
    test_obj = TestJson(json_file)
    assert test_obj.name == "John"
    assert test_obj.age == 30

def test_write_property(json_file):
    test_obj = TestJson(json_file)
    test_obj.name = "Jane"
    
    with open(json_file, 'r') as f:
        content = json.load(f)
        assert content == {"name": "Jane", "age": 30}

def test_file_modification_detection(json_file):
    test_obj = TestJson(json_file)
    
    # Modify file externally
    with open(json_file, 'w') as f:
        json.dump({"name": "Bob", "age": 25}, f)
        
    assert test_obj.name == "Bob"
    assert test_obj.age == 25

def test_missing_key(json_file):
    with open(json_file, 'w') as f:
        json.dump({"other_key": "value"}, f)
    
    test_obj = TestJson(json_file)
    assert test_obj.name is None
    assert test_obj.age is None

class CustomJson:
    def __init__(self, json_path):
        self.__JSON_PATH__ = json_path
        self.__JSON_CONTENT__ = None
        
    def __JSON_LOAD_METHOD__(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            return {"prefix_" + k: v for k, v in data.items()}
            
    def __JSON_SAVE_METHOD__(self, path, value):
        cleaned = {k.replace("prefix_", ""): v for k, v in value.items()}
        with open(path, 'w') as f:
            json.dump(cleaned, f)
            
    name = JsonProperty("prefix_name")

def test_custom_load_method(json_file):
    test_obj = CustomJson(json_file)
    assert test_obj.name == "John"  # Should load with prefix

def test_custom_save_method(json_file):
    test_obj = CustomJson(json_file)
    test_obj.name = "Modified"
    
    with open(json_file, 'r') as f:
        saved_data = json.load(f)
        assert saved_data == {"name": "Modified", "age": 30}  # Should save without prefix 