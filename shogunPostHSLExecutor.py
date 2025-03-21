import tempfile
import time
import os
import sys
sys.path.append(r"C:\Program Files\Vicon\ShogunPost1.12\SDK\Win64")

try:
    import ViconShogunPostSDK
except ImportError as e:
    print(f"ImportError: {str(e)}")
    sys.exit(1)

class ShogunPostHSLExec():
    def __init__(self, address="localhost", port=805):
        self._Client = ViconShogunPostSDK.Client3.TheClient
        self.Connect(address, port)

    def __del__(self):
        if self._Client.IsConnected():
            self._Client.Disconnect()

    def Connect(self, address, port=803):
        if self._Client.IsConnected():
            self._Client.Disconnect()

        result = self._Client.Connect(address, port)
        if result.Error():  # This line might not be needed if Connect returns a boolean or similar
            raise ConnectionError("Failed to connect to Shogun Post.")

        if not self._Client.IsConnected():
            raise ConnectionError("Unable to connect to ShogunPost application.")
        
        print(f"Connected to ShogunPost at {address}:{port}")

    def ExecuteHSL(self, hsl_script):
        """
        Executes HSL commands by writing them to a temp file,
        executing them in ShogunPost, and capturing the output from another temp file.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", dir=os.getenv("TEMP")) as output_file:
            output_file_path = output_file.name

        try:
            # Ensure paths are correct and passed properly to ShogunPost
            output_file_path = os.path.abspath(output_file_path)
            output_file_path_escaped = output_file_path.replace("\\", "\\\\")

            # Wrap the HSL script to use the output file
            wrapped_script = f"""
            int $fileHandle = `fileOpen "{output_file_path_escaped}" "w"`;

            {hsl_script}  // Execute provided script

            // Write the result to the file
            writeString $fileHandle $result;

            fileClose $fileHandle;
            """

            # Execute HSL script
            self._Client.HSL(wrapped_script)

            # Wait briefly to make sure the file is fully written before reading
            time.sleep(0.2)  # You can adjust the sleep time if needed

            # Read the output from the file
            with open(output_file_path, "r") as file:
                result = file.read().strip()

            return result

        finally:
            # Cleanup temp files from Python
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
