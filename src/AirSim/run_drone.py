import setup_path
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time
import json

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)



airsim.wait_key('Press any key to takeoff')
start = time.time()

print("Taking off...")
client.armDisarm(True)
client.takeoffAsync().join()

airsim.wait_key('Press any key to move vehicle')

z= -30

f = open('CoordJsonRRT.json')
data = json.load(f)


for i in data['move_xy']:
    client.moveToPositionAsync(int(i[0]), int(i[1]),   -30, 10).join()


f.close()


time.sleep(5)

end = time.time()
print(f"Runtime of the program is {end - start}")
landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
    print("already landed...")
else:
    print("landing...")
    client.landAsync(10).join()

print(f"Runtime of the program is {end - start}")

client.enableApiControl(False)
