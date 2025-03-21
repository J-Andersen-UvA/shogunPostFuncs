import yaml
import os
import datetime

class FileManager:
    def __init__(self, yaml_file_path):
        # Check if file exists
        if not os.path.exists(yaml_file_path):
            print(f"Error: The YAML file '{yaml_file_path}' does not exist.\tUsing default variables.")
            yaml_file_path = b"C:\Users\VICON\Desktop\Code\shogunPostHomeMadeCode\exportMultipleActorMarkers\config.yaml"

        with open(yaml_file_path, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        self.csv_out = config.get('csv_export_path')
        self.error_log = config.get('error_log_path')

    def set_csv_out(self, path):
        self.csv_out = path

    def get_file_path_from_output_dir(self, file_name):
        return os.path.join(self.csv_out, file_name)

    def write(self, data):
        with open(self.path, 'w') as file:
            yaml.dump(data, file)
    
    def write_error(self, data):
        # Open a file based on the current day
        file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d')}_error_log.txt"
        self.error_log = os.path.join(self.error_log, file_name)
        # Append the error message to the file
        with open(self.error_log, 'a') as file:
            file.write(f"{datetime.datetime.now().strftime('%H:%M:%S')}: {data}\n")