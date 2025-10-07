import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import getDataScene
import logger

def exportActorsMarkersSeparatly(file_path=None):
    scene_data = getDataScene.ShogunPostSceneData()
    file_name_path = scene_data.getFileName()
    file_name = file_name_path.split("/")[-1].split(".")[0]
    if file_path is None:
        file_path = scene_data.getCurrentDirectory()
        # Usually folder is ../shogun_post from the filepath
        if "shogun_live" in file_path:
            file_path = file_path.replace("shogun_live", "shogun_post")
            scene_data.printInHSL(f"Exporting to folder: {file_path}")
        else:
            file_path = "D:/PostExports/CSV/BufferFolder/"

    log_folder = file_path.replace("shogun_post", "metadata")
    scene_data.printInHSL(f"Looking for log files in folder: {log_folder}")
    log_file = logger.fetch_first_log_file_from_folder(log_folder, file_name)
    scene_data.printInHSL(f"Using log file: {log_file if log_file != '' else 'None found...'}")
    log = logger.Logger(log_file if log_file != "" else None)

    file_paths = scene_data.processAndExportAllMarkers(output_dir=file_path)
    scene_data.printInHSL(f"Done processing marker csv's")

    for path in file_paths:
        log.append_log(f"assets.mocap_marker_csv", path)

if __name__ == "__main__":
    exportActorsMarkersSeparatly()
