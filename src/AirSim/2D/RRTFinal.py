import pygame
import time
import json
import math
from RRTbasePyFinal import RRTGraph
from RRTbasePyFinal import RRTMap

def lat2N(lat_in, refLLH):
    # Note: H is fixed to -30
    radius = 6378137
    flattening = 1/298.257223563
    e = math.sqrt(flattening * (2 - flattening))
    Rm = radius * (1 - e**2)/(1 - e**2 * math.sin(refLLH[0]*math.pi/180)**2)**(3/2)
    posN = (lat_in - refLLH[0]) * math.pi/180 * (Rm + -30)

    return posN

def lon2E(lon_in, refLLH):
    # Note: H is fixed to -30
    radius = 6378137
    flattening = 1/298.257223563
    e = math.sqrt(flattening * (2 - flattening))
    Rn = radius / (1 - e**2 * math.sin(refLLH[0]*math.pi/180)**2)**(1/2)
    posE = (lon_in - refLLH[1]) * math.pi/180 * (Rn + -30) * math.cos(refLLH[0] * math.pi/180)

    return posE

def main():
    lat_top = 42.2949
    lat_btm = 42.2878
    lon_lft = 83.7190
    lon_rht = 83.7047

    lat_del = lat_top - lat_btm
    lon_del = lon_lft - lon_rht

    origin = (42.2949, 83.7190)
    refLLH = [42.2949, 83.7190, -30]

    lat_beg = -lat2N(42.28846, refLLH)
    lon_beg = -lon2E(83.71718, refLLH)

    lat_end = -lat2N(42.29313, refLLH)
    lon_end = -lon2E(83.71166, refLLH)

    dimensions = (789, 1180)
    start = (int(lon_beg),int(lat_beg))
    goal = (int(lon_end),int(lat_end))
    obsdim = 30
    obsnum = 97

    iteration = 0
    t1 = 0
    td = 0

    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)

    # Take smallest/largest number of 4 sides to get width and height of rect
    # 1-38 all buildings and forests within bonisteel boulevard to hayward street, murfin avenue to beal avenue
    RT = [42.29393, 42.29393, 42.29336, 42.29335, 42.29363, 42.29334, 42.29379, 42.29297, 42.29296, 42.29296, 42.29277,
          42.29272, 42.29267, 42.29255, 42.29255, 42.29199, 42.29182, 42.29166, 42.29145, 42.29145, 42.29126, 42.29093,
          42.29071, 42.29058, 42.29139, 42.29136, 42.29087, 42.29157, 42.29129, 42.29129, 42.29158, 42.29131, 42.29114,
          42.29107, 42.29208, 42.29209, 42.29217, 42.29208, 42.29480, 42.29471, 42.29383, 42.29383, 42.29388, 42.29369,
          42.29352, 42.29314, 42.29291, 42.29264, 42.29218, 42.29173, 42.29037, 42.28987, 42.28977, 42.28899, 42.28924,
          42.28924, 42.28923, 42.29001, 42.28999, 42.29000, 42.29000, 42.29011, 42.28985, 42.28981, 42.28941, 42.28944,
          42.28957, 42.28914, 42.29006, 42.28990, 42.28988, 42.28966, 42.28932, 42.29012, 42.28999, 42.28844, 42.28860,
          42.28848, 42.29487, 42.29492, 42.29494, 42.29483, 42.29353, 42.29358, 42.29318, 42.29305, 42.29266, 42.29398,
          42.29543, 42.29273, 42.29246, 42.29225, 42.28996, 42.29068, 42.29049, 42.29311, 42.29226]
    RB = [42.29278, 42.29297, 42.29266, 42.29310, 42.29294, 42.29294, 42.29294, 42.29258, 42.29281, 42.29254, 42.29254,
          42.29254, 42.29254, 42.29214, 42.29178, 42.29178, 42.29163, 42.29142, 42.29132, 42.29125, 42.29091, 42.29069,
          42.29054, 42.29045, 42.29070, 42.29116, 42.29050, 42.29075, 42.29104, 42.29053, 42.29112, 42.29111, 42.29105,
          42.29070, 42.29163, 42.29182, 42.29201, 42.29191, 42.29404, 42.29416, 42.29307, 83.71229, 42.29366, 42.29349,
          42.29312, 42.29290, 42.29279, 42.29218, 42.28988, 42.28988, 42.28988, 42.28943, 42.28913, 42.28820, 42.28846,
          42.28878, 42.28882, 42.28927, 42.28974, 42.28981, 42.28984, 42.28989, 42.28972, 42.28926, 42.28926, 42.28926,
          42.28943, 42.28835, 42.28984, 42.28962, 42.28962, 42.28930, 42.28904, 42.28955, 42.28771, 42.28825, 42.28843,
          42.28843, 42.29427, 42.29431, 42.29439, 42.29459, 42.29326, 42.29326, 42.29299, 42.29290, 42.29237, 42.29275,
          42.29384, 42.29202, 42.29224, 42.29191, 42.28791, 42.28870, 42.28884, 42.29135, 42.28997]
    RL = [83.71857, 83.71883, 83.71769, 83.71510, 83.71478, 83.71413, 83.71327, 83.71361, 83.71404, 83.71473, 83.71455,
          83.71428, 83.71402, 83.71482, 83.71482, 83.71482, 83.71405, 83.71419, 83.71367, 83.71384, 83.71408, 83.71386,
          83.71415, 83.71404, 83.71476, 83.71483, 83.71495, 83.71627, 83.71705, 83.71701, 83.71761, 83.71773, 83.71785,
          83.71798, 83.71818, 83.71772, 83.71706, 83.71630, 83.71890, 83.71218, 83.71229, 83.71148, 83.71120, 83.71097,
          83.71097, 83.71134, 83.71192, 83.71260, 83.71215, 83.70849, 83.71288, 83.71282, 83.71210, 83.71256, 83.71398,
          83.71361, 83.71468, 83.71466, 83.71441, 83.71476, 83.71390, 83.71342, 83.71534, 83.71542, 83.71542, 83.71496,
          83.71509, 83.71539, 83.71811, 83.71759, 83.71688, 83.71785, 83.71818, 83.71658, 83.71169, 83.70826, 83.70791,
          83.70756, 83.70992, 83.70967, 83.70940, 83.70902, 83.70965, 83.70928, 83.70969, 83.70959, 83.70949, 83.70834,
          83.70693, 83.70714, 83.70867, 83.70777, 83.70483, 83.70874, 83.70653, 83.70639, 83.70574]
    RR = [83.71758, 83.71857, 83.71507, 83.71469, 83.71399, 83.71290, 83.71290, 83.71317, 83.71374, 83.71455, 83.71427,
          83.71401, 83.71376, 83.71292, 83.71457, 83.71319, 83.71397, 83.71347, 83.71346, 83.71378, 83.71336, 83.71378,
          83.71323, 83.71393, 83.71454, 83.71472, 83.71474, 83.71517, 83.71624, 83.71644, 83.71699, 83.71758, 83.71744,
          83.71738, 83.71768, 83.71671, 83.71676, 83.71606, 83.71253, 83.71069, 83.71192, 42.29341, 83.71027, 83.71026,
          83.71046, 83.71025, 83.71039, 83.71041, 83.70840, 83.70725, 83.71153, 83.71187, 83.71187, 83.71198, 83.71354,
          83.71321, 83.71420, 83.71433, 83.71419, 83.71461, 83.71337, 83.71323, 83.71492, 83.71521, 83.71493, 83.71493,
          83.71468, 83.71484, 83.71650, 83.71748, 83.71674, 83.71648, 83.71661, 83.71610, 83.70843, 83.70748, 83.70744,
          83.70732, 83.70961, 83.70936, 83.70902, 83.70878, 83.70936, 83.70898, 83.70860, 83.70939, 83.70876, 83.70616,
          83.70499, 83.70658, 83.70743, 83.70744, 83.70408, 83.70653, 83.70607, 83.70564, 83.70436]

    TLy_data = []
    TLx_data = []
    width_data = []
    height_data = []
    for i in range(0, obsnum):
        TLy = -lat2N(RT[i], refLLH)
        TLx = -lon2E(RL[i], refLLH)
        width = lon2E(RL[i], refLLH) - lon2E(RR[i], refLLH)
        height = lat2N(RT[i], refLLH) - lat2N(RB[i], refLLH)

        TLy_data.append(int(TLy / 0.97))
        TLx_data.append(int(TLx * 0.97))
        width_data.append(int(width * 1.05))
        height_data.append(int(height * 1.05))


    obstacles = graph.makeobs(TLy_data,TLx_data,width_data,height_data)
    map.drawMap(obstacles)

    running = True
    rrt_done = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        t1 = time.time()
        td = time.time()
        while (not rrt_done):
            while (not graph.path_to_goal()):
                tt = time.time() - t1
                td = time.time() - t1

                if tt > 600:
                    raise

                if iteration % 10 == 0:
                    X, Y, Parent = graph.bias(goal)
                    pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad + 2, 0)
                    pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)

                else:
                    X, Y, Parent = graph.expand()
                    pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad + 2, 0)
                    pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)

                #while (td < 0.5):
                   #td = time.time() - t1
                    if iteration % 5 == 0: # and td >= 0.5:
                        pygame.display.update()

                td = time.time()

                iteration += 1

            graph.getCosts()

            map.drawPath(graph.getPathCoords())
            pygame.display.update()

            pathout = graph.getPathCoords()
            pathout.reverse()

            xy_start = pathout[0]
            xy_data = []

            for node in pathout:
                x = node[0] - xy_start[0]
                y = node[1] - xy_start[1]

                xy_out = (x, y)

                xy_data.append(xy_out)

            data = {
                'move_xy': xy_data
            }

            json_string = json.dumps(data)

            with open('CoordJsonRRT.json', 'w') as filename:
                json.dump(json_string, filename)

            t1 = time.time()
            for iter in range(0,10000):
                tt = time.time() - t1

                if tt > 600:
                    raise

                if iter % 10 == 0:
                    X, Y, Parent = graph.expandStarIron()
                    pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad+2, 0)
                    pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)

                else:
                    X, Y, Parent = graph.expandStar()
                    pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad+2, 0)
                    pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)

                if iter % 5 == 0:
                    pygame.display.update()

            graph.getCosts()
            print('Loop complete')

            map.drawPathG(graph.getPathCoords())
            pygame.display.update()

            pathout = graph.getPathCoords()
            pathout.reverse()

            xy_start = pathout[0]
            xy_data = []

            for node in pathout:
                x = node[0] - xy_start[0]
                y = node[1] - xy_start[1]

                xy_out = (x, y)

                xy_data.append(xy_out)

            data = {
                'move_xy' : xy_data
            }

            json_string = json.dumps(data)

            with open('CoordJsonRRTstar.json', 'w') as filename:
                json.dump(json_string, filename)

            #file1 = open("PathCoord1.txt", "w")
            #for item in pathout:
            #    file1.writelines(str(item) + "\n")

            #file1.close()
            print('saved complete')

            pygame.event.clear()
            pygame.event.wait(1000)

            rrt_done = True

    print("end function")

if __name__ == '__main__':
    result = False
    while not result:
        try:
            main()
            print("end main")
            result = True
            print("end update")
        except:
            print("except")
            result = False
