import json
import os

def fetch_first_log_file_from_folder(folder, glossary_name):
    log_file = ""
    # find out if there is a json file in this folder
    for file in os.listdir(folder):
        if file.endswith(".json"):
            file_path = os.path.join(folder, file)
            try:
                with open(file_path, 'r') as f:
                    content = json.load(f)
                    if glossary_name in json.dumps(content):
                        log_file = file_path
                        break
            except Exception:
                continue
    return log_file

class Logger:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.data = {}

        if self.file_path is not None:
            self.load_file(file_path)
        pass

    def load_file(self, file_path):
        self.file_path = file_path
        
        if not os.path.exists(self.file_path):
            print(f"Error: The log file '{self.file_path}' does not exist.\tSkipping.")
            return

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

        pass

    def log(self, key, value):
        if self.file_path is None:
            print("Error: No log file path specified.\tSkipping...")
            return

        keys = key.split(".")  # support nested keys like "user.name.first"
        data_ref = self.data

        for k in keys[:-1]:
            if k not in data_ref or not isinstance(data_ref[k], dict):
                data_ref[k] = {}
            data_ref = data_ref[k]

        data_ref[keys[-1]] = value

        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def append_log(self, key, value):
        if self.file_path is None:
            print("Error: No log file path specified.\tSkipping...")
            return

        keys = key.split(".")  # support nested keys like "user.name.first"
        data_ref = self.data

        for k in keys[:-1]:
            if k not in data_ref or not isinstance(data_ref[k], dict):
                data_ref[k] = {}
            data_ref = data_ref[k]

        if keys[-1] not in data_ref or not isinstance(data_ref[keys[-1]], list):
            data_ref[keys[-1]] = []
        
        data_ref[keys[-1]].append(value)

        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)
