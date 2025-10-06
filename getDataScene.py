import shogunPostHSLExecutor
import fileManager
import csv
import os

class ShogunPostSceneData():
    def __init__(self):
        self.actors = []
        self.markers = {}
        self.hsl_exec = shogunPostHSLExecutor.ShogunPostHSLExec()
        if not os.path.exists("config.yaml"):
            print(f"Error: The YAML file 'config.yaml' does not exist.\tSkipping.")
            self.fm = None
        else:
            self.fm = fileManager.FileManager("config.yaml")
    
        pass

    def addActor(self, actor):
        self.actors.append(actor)

    def addMarkersActor(self, actor, markers):
        self.markers[actor] = markers

    def getActors(self):
        get_actors_hsl = """
            string $Actors[];
            selectByType Character;
            $Actors = `getModules -selected -nameOnly`;

            // Create a returnable string (comma-separated)
            string $result = ""; // Initialize an empty result string, this will be used to store the result
            int $i;
            for ($i = 0; $i < `getCount $Actors`; $i += 1) {
                if ($i > 0) {
                    $result += ",";  // Add a comma separator
                }
                $result += $Actors[$i];
            }
        """
        result = self.hsl_exec.ExecuteHSL(get_actors_hsl)

        # Convert comma-separated string to a Python list
        self.actors = result.strip().split(",") if result else []
        self.unSelect()

        return self.actors
    
    def getAllMarkerForActor(self, actor):
        self.unSelect()
        self.selectCurrentSubject(actor)
        get_markers_hsl = f"""
            select "{actor}";
            string $result = "";
            string $AllChildren[];

            // Get all children of the actor
            $AllChildren = `getChildren {actor}`;

            // Filter only Marker type modules
            int $i;
            for ($i = 0; $i < `getCount $AllChildren`; $i += 1) {{
                string $parent = `getParent $AllChildren[$i]`;
                if (`getModuleType $parent` != "LabelingCluster") {{
                    if (`getModuleType $AllChildren[$i]` == "Marker") {{
                        $result += $AllChildren[$i];
                        $result += ",";
                    }}
                }}
            }}
        """
        result = self.hsl_exec.ExecuteHSL(get_markers_hsl)
        markers = result.strip().split(",") if result else []
        markers = self.filterMarkers(markers)

        self.markers[actor] = markers

        self.unSelectCurrentSubject()
        self.unSelect()

        return markers
    
    def selectAllFingerMarkers(self, actor):
        self.unSelect()
        self.selectCurrentSubject(actor)
        markers = '"LIWR" "LOWR" "RIWR" "ROWR" "LIHAND" "LOHAND" "RIHAND" "ROHAND" "LTHM3" "LTHM6" "LIDX3" "LIDX6" "LMID0" "LMID6" "LRNG3" "LRNG6" "LPNK3" "LPNK6" "RTHM3" "RTHM6" "RIDX3" "RIDX6" "RMID0" "RMID6" "RRNG3" "RRNG6" "RPNK3" "RPNK6"'
        get_markers_hsl = f"""
            selectByName {markers};
            string $result = "";
        """
        self.markers[actor] = markers.split('"')[1::2]
        self.markers[actor] = [marker for marker in self.markers[actor] if marker != ""]
        self.hsl_exec.ExecuteHSL(get_markers_hsl)
        pass

    def filterMarkers(self, markers):
        # remove the last empty string if it exists
        if markers[-1] == "":
            markers = markers[:-1]

        # If a marker name contains the string "LabelingCluster", it is filtered out.
        markers = [marker for marker in markers if "LabelingCluster" not in marker]

        return markers
        
    def selectByName(self, name):
        select_by_name_hsl = f"""
            string $result = "";
            select "{name}";
        """
        self.hsl_exec.ExecuteHSL(select_by_name_hsl)
        pass

    def selectByNames(self, names):
        select_by_name_hsl = """
            string $result = "";
        """
        for name in names:
            select_by_name_hsl += f"""
                select "{name}" -a;\n
            """
        self.hsl_exec.ExecuteHSL(select_by_name_hsl)
        pass

    def selectCurrentSubject(self, actor):
        select_current_subject_hsl = f"""
            string $result = "";
            setCurrentSubject "{actor}";
        """
        self.hsl_exec.ExecuteHSL(select_current_subject_hsl)
        pass

    def unSelectCurrentSubject(self):
        unselect_current_subject_hsl = """
            string $result = "";
            setCurrentSubject All;
        """
        self.hsl_exec.ExecuteHSL(unselect_current_subject_hsl)
        pass

    def unSelect(self):
        unselect_hsl = """
            string $result = "";
            select ;
        """
        self.hsl_exec.ExecuteHSL(unselect_hsl)
        pass

    def getFileName(self):
        get_file_name_hsl = """
            string $result = "";
            string $fileNameExtension = `GetPathToExportTo` + ".mcp";
            $result = `getFileTitle $fileNameExtension`;
        """
        result = self.hsl_exec.ExecuteHSL(get_file_name_hsl)
        return result.strip()

    def getCurrentFilePath(self):
        get_file_path_hsl = """
            string $result = "";
            $result = `GetPathToExportTo` + ".mcp";
        """
        result = self.hsl_exec.ExecuteHSL(get_file_path_hsl)
        return result
    
    def getCurrentDirectory(self):
        get_current_directory_hsl = """
            string $filePath = `GetPathToExportTo`;
            string $result = `getFileLocation $filePath`;
        """
        result = self.hsl_exec.ExecuteHSL(get_current_directory_hsl)
        return result

    def printInHSL(self, message):
        print_in_hsl = f"""
            string $result = "";
            print "{message}";
        """
        self.hsl_exec.ExecuteHSL(print_in_hsl)
        pass

    def _exportActorMarkersToCSV(self, actor, output_dir=None):
        if actor not in self.markers:
            if self.fm is not None:
                self.fm.write_error(f"No marker data available for actor: {actor} in file: {self.getFileName()}")
            print(f"No marker data available for actor: {actor}")
            return
        
        markers = self.markers[actor]
        if not markers:
            if self.fm is not None:
                self.fm.write_error(f"No markers found for actor: {actor} in file: {self.getFileName()}")
            print(f"No markers found for actor: {actor}")
            return

        if output_dir:
            if self.fm is not None:
                self.fm.set_csv_out(output_dir)

        file_name = self.getFileName() + f"_actor_{actor}_markers.csv"
        if self.fm is not None:
            file_path = self.fm.get_file_path_from_output_dir(file_name)
        elif output_dir:
            file_path = f"{output_dir}/{file_name}"
        else:
            file_path = f"D:/PostExports/CSV/BufferFolder/{file_name}"

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["Frame"] + [f"{marker}<T-X>" for marker in markers] + \
                     [f"{marker}<T-Y>" for marker in markers] + \
                     [f"{marker}<T-Z>" for marker in markers]
            writer.writerow(header)

            self.selectCurrentSubject(actor)
            self.selectByNames(markers)

            get_translation_hsl = f"""
                string $Markers[];
                string $result = "";
                $Markers = `getModules -selected -nameOnly -type Marker`;

                int $Start = `getPlayStart`;
                int $End = `getPlayEnd`;
                int $CurTime;

                for ($CurTime = $Start; $CurTime <= $End; $CurTime += 1) {{
                    setTime $CurTime;
                    string $line = string($CurTime) + ",";

                    int $n;
                    for ($n = 0; $n < `getCount $Markers`; $n += 1) {{
                        select $Markers[$n] -priorityOnly;
                        if (`hasKey $Markers[$n] "TranslationX"`) {{
                            float $x = `getProperty $Markers[$n] "TranslationX"`;
                            float $y = `getProperty $Markers[$n] "TranslationY"`;
                            float $z = `getProperty $Markers[$n] "TranslationZ"`;
                            $line = $line + string($x) + "," + string($y) + "," + string($z) + ",";
                        }} else {{
                            $line = $line + ",,,";
                        }}
                    }}

                    $result += $line + "\\n";
                }}
            """
            result = self.hsl_exec.ExecuteHSL(get_translation_hsl)
            for line in result.strip().split("\n"):
                writer.writerow(line.split(","))

        self.unSelectCurrentSubject()
        self.unSelect()
        # return the filepath for logging purposes
        return file_path

    def processAndExportAllMarkers(self, output_dir=None):
        self.getActors()
        file_paths = []
        for i, actor in enumerate(self.actors):
            self.getAllMarkerForActor(actor)
            file_paths.append(self._exportActorMarkersToCSV(actor, output_dir=output_dir))

        return file_paths

    def processAndExportAllFingerMarkers(self, output_dir=None):
        self.getActors()
        for i, actor in enumerate(self.actors):
            self.selectAllFingerMarkers(actor)
            self._exportActorMarkersToCSV(actor, output_dir=output_dir)

    def exportActorFBX(self, actor_name, path):
        export_fbx_hsl = f"""
            string $result = "";
            setCurrentSubject {actor_name};
            labelOptions -curChar "{actor_name}";
            select "{actor_name}" -a;
            SelectChildren_Add_All;
            saveFile -s "{path}";
            select ;
            setCurrentSubject All;
        """
        self.printInHSL(f"Exporting actor '{actor_name}' to FBX at path: {path}")
        if actor_name not in self.actors:
            if self.fm is not None:
                self.fm.write_error(f"Actor '{actor_name}' not found in the scene data.")
            self.printInHSL(f"Actor '{actor_name}' not found in the scene data.")
            return

        result = self.hsl_exec.ExecuteHSL(export_fbx_hsl)

# example usage
# if __name__ == '__main__':
    # print("Running ShogunPostSceneData example...")
    # scene_data = ShogunPostSceneData()
    # scene_data.processAndExportAllMarkers()
    # scene_data.processAndExportAllFingerMarkers()

    # actors = scene_data.getActors()

    # for actor in actors:
    #     markers = scene_data.getMarkersFromActor(actor)
    #     print(f"Markers for actor '{actor}': {markers}")

    # all_markers = scene_data.getAllMarkers()
    # print(f"All markers: {all_markers}")