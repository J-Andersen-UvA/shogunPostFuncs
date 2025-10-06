import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import getDataScene

if __name__ == "__main__":
    scene_data = getDataScene.ShogunPostSceneData()
    scene_data.printInHSL("Hello World from getDataScene!")
    