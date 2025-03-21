import yaml
import os

class FileManager:
    def __init__(self, yaml_file_path):
        with open(yaml_file_path, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        self.csv_out = config.get('csv_export_path')

    def set_csv_out(self, path):
        self.csv_out = path

    def get_file_path_from_output_dir(self, file_name):
        return os.path.join(self.csv_out, file_name)

    def write(self, data):
        with open(self.path, 'w') as file:
            yaml.dump(data, file)