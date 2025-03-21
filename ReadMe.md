# Shogun Post Scene Data Exporter

## Introduction

I created this project because I dislike dealing with functions, keeping track of variables, and the documentation of the Blade scripting language in Shogun Post. To simplify my workflow, I developed a way to handle these tasks using Python. Directly returning data from Blade to Python was not possible, so I opted to use a temporary file to facilitate the process.

## Overview

This project consists of two main Python scripts:

1. `getDataScene.py`: This script handles the extraction of actor and marker data from Shogun Post and exports it to CSV files.
2. `shogunPostHSLExecutor.py`: This script provides a wrapper to execute HSL (Human Script Language) commands in Shogun Post using a temporary file to capture the output.

## Files

### `getDataScene.py`

This script defines the `ShogunPostSceneData` class, which includes methods to:

- Add actors and markers.
- Retrieve actors and markers from Shogun Post.
- Export marker data to CSV files.

### `shogunPostHSLExecutor.py`

This script defines the `ShogunPostHSLExec` class, which includes methods to:

- Connect to the Shogun Post application.
- Execute HSL commands and capture the output using a temporary file.

## Usage

To use this project, follow these steps:

1. Ensure you have Shogun Post installed and the SDK available.
2. Update the `sys.path.append` line in `shogunPostHSLExecutor.py` to point to your Shogun Post SDK directory.
3. Run the `getDataScene.py` script to process and export actor marker data to CSV files.

```bash
python getDataScene.py
```

This will connect to Shogun Post, retrieve actor and marker data, and export the data to CSV files in the `output` directory.

## Example

```python
if __name__ == '__main__':
    print("Running ShogunPostSceneData example...")
    scene_data = ShogunPostSceneData()
    scene_data.processAndExportAll()
```

This example demonstrates how to create an instance of the `ShogunPostSceneData` class and process all actors and markers, exporting the data to CSV files.

## Conclusion

This project simplifies the process of extracting and exporting actor and marker data from Shogun Post using Python, avoiding the complexities of Blade scripting and variable management.
