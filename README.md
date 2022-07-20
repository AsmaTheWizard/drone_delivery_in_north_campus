# Drone Delivery in the North Campus of the University of Michigan

My colleagues -Matthew Liu, Chuan Yuan Lim- and I worked on
implementing RRT and RRT\* Algorithms for Drone Delivery in North Campus of the University of Michigan

The drone’s mission is to fly from defined start and end points in the North Campus of the University of Michigan. The path finding algorithms are implemented in 2D first. For simplicity, the drone dynamics are also not added as constraints to the algorithms.

Unreal Engine is then used to build an environment representing North Campus for a 3D drone flight simulation. After generating paths from both RRT and RRT\* techniques, we will use the AirSim open-source library to have the drone fly on such a predefined path, illustrating and verifying that the established paths are viable.

###Algorithms
Two algorithms were explored for path planning of the simulated quadcopter: Rapid-exploring Random Trees (RRT), and Rapid-exploring Random Trees Star (RRT\*).

Area selected and implemented into PyGame from Open Street Map
![Area selected and implemented into PyGame from Open Street Map](/img/img%201.png)

Blank map
![Blank map](/img/img%202.png)

Result
![Result](/img/img%203.png)

### 3D Environment

To create the 3D simulation, we explored three different methods to demonstrate the results of our search algorithms. The first explored option involved using RenderDoc to capture the 3d buffers from Google Maps, then exporting them to a Blender software program to enhance the image; afterwards, the rendered 3D image was exported for use with Unreal Engine. While this method produced a realistic rendered image for buildings, it lacked propagation and GPS data to facilitate navigation and path-finding.

The second explored method was using an OSM plugin with the Blender program to create a map with one-color building shapes, then exporting the model to the Unreal Engine program, and then import this model and OSM data for the same exact map size. This method indeed gave us GPS data that we could use for navigation, but the resulting GPS coordinates were not accurate to the map that they were supposed to represent.

The third method involved using Cesium for Unreal Engine and adding the simulated drone as a new program. Then, we set the origin coordinate of the drone in the Unreal Engine simulation. The drone would be placed at the same GPS coordinates as the origin selected on the 2d map. Then, we used AirSim Python APIs to control the movement of the drone, allowing it to navigate in our 3D simulation.

![3D drone path](/img/img%204.png)
