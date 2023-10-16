# from executor.executor import Executor
# # from mapping.mapper import Mapper
# # from robot.robot import Robot

def main():
    robot = Robot(time_step=32)
    mapper = Mapper(tile_size=0.12, robot_diameter=robot.diameter, camera_distance_from_center=robot.diameter / 2)
    executor = Executor(mapper, robot)

    executor.run()


## Code for victim's classification using Yolo V8

import requests

def downloadYOLO():
    r = requests.get(IA_DATASETURL, allow_redirects=True)
    open('ia.pt', 'wb').write(r.content)

IA_DATASETURL = "https://raw.githubusercontent.com/GUriburuRomero/test/main/MyYoloTeam.pt"

downloadYOLO()

# main()