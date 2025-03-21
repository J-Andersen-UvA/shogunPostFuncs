import shogunPostHSLExecutor
import fileManager
import csv
import os

class ShogunPostSceneData():
    def __init__(self):
        self.actors = []
        self.markers = {}
        self.hsl_exec = shogunPostHSLExecutor.ShogunPostHSLExec()
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

            print $result;
        """
        result = self.hsl_exec.ExecuteHSL(get_actors_hsl)

        # Convert comma-separated string to a Python list
        self.actors = result.strip().split(",") if result else []

        print(f"Actors: {self.actors}")
        return self.actors
    
    def getAllMarkerForActor(self, actor):
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

            print $result;
        """
        result = self.hsl_exec.ExecuteHSL(get_markers_hsl)
        markers = result.strip().split(",") if result else []
        markers = self.filterMarkers(markers)

        self.markers[actor] = markers
        print(f"Markers for {actor}: {markers}")

        return markers

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

    def exportActorMarkersToCSV(self, actor, actorID, output_dir=None):
        if actor not in self.markers:
            print(f"No marker data available for actor: {actor}")
            return
        
        markers = self.markers[actor]
        if not markers:
            print(f"No markers found for actor: {actor}")
            return

        if output_dir:
            self.fm.set_csv_out(output_dir)

        file_path = self.fm.get_file_path_from_output_dir(self.getFileName() + f"_actor{actorID}_markers.csv")

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["Frame"] + [f"{marker}<T-X>" for marker in markers] + \
                     [f"{marker}<T-Y>" for marker in markers] + \
                     [f"{marker}<T-Z>" for marker in markers]
            writer.writerow(header)

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

        print(f"Exported markers for {actor} to {file_path}")
        self.unSelect()

    def processAndExportAll(self):
        self.getActors()
        for i, actor in enumerate(self.actors):
            self.getAllMarkerForActor(actor)
            self.exportActorMarkersToCSV(actor, i)


# example usage
if __name__ == '__main__':
    print("Running ShogunPostSceneData example...")
    scene_data = ShogunPostSceneData()
    scene_data.processAndExportAll()

    # actors = scene_data.getActors()

    # for actor in actors:
    #     markers = scene_data.getMarkersFromActor(actor)
    #     print(f"Markers for actor '{actor}': {markers}")

    # all_markers = scene_data.getAllMarkers()
    # print(f"All markers: {all_markers}")