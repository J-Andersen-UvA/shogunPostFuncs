import getDataScene

def exportActorsSeparatly():
    scene_data = getDataScene.ShogunPostSceneData()
    actors = scene_data.getActors()
    file_name_path = scene_data.getFileName()
    file_name = file_name_path.split("/")[-1].split(".")[0]

    for actor in actors:
        scene_data.printInHSL(f"Processing actor: {actor}")
        scene_data.exportActorFBX(actor, f"D:/PostExports/FBX/BufferFolder/{file_name}_{actor}.fbx")
        scene_data.printInHSL(f"Done processing actor: {actor}")

exportActorsSeparatly()
