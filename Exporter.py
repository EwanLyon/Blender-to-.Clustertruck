import bpy
import math
from mathutils import Vector, Matrix
import json
import os
import datetime
import numpy

# Start timer
startTime = datetime.datetime.now()

# Used for counting and starts list
counter = 1
vertlist = []

# Get object
obj = bpy.context.active_object
mesh = obj.data

# Get object matrix
mat_world = obj.matrix_world
up = Vector((0, 0, 1.5))

# File name and location
directoryloc = "C:/"
levelname = "0ExporterTesting.clustertruck"
fullname = os.path.join(directoryloc, levelname)

# Create file named after filename as a .json
print("Creating: {}" .format(levelname))
with open(fullname, 'w') as a:
    level = {"tiles":[ ] }

print("\n")
print("Starting")
print("--------------")

# Adding a new object in .clustertruck
def newPlane(locx, locy, locz, rotx, roty, rotz, scax, scay):
    global counter

    # Add object
    level['tiles'].append({"x": locx, "y": locy, "z": locz, "scalex": scax, "scaley": scay, "scalez": 0.1, "rotx": rotx, "roty": roty, "rotz": rotz, "type": 8, "waypointType": 0, "wayPointIndex": 0, "id": "Cube", "Index": counter, "objsParams": [], "Behaviours": None, "EventInfo": None})

    counter += 1

# Analyse polygon's properties
for poly in mesh.polygons:

    print("--------------")
    print("Poly:", counter)
    print("--------------")

    print("Calculating polygon")

    # SCALE
    # Get verticies of poly
    for idx in poly.vertices:
        # print(obj.data.vertices[idx].co)
        local_point = obj.data.vertices[idx].co
        world_point = mat_world * local_point
        vertlist.append(world_point)

    # Get needed points
    point1 = vertlist[0]
    point2 = vertlist[1]
    point3 = vertlist[2]

    # Scale X
    distx = numpy.linalg.norm(point1 - point2)
    distxdiv = distx / 2
    scax = round(distxdiv, 8)
    #Scale Y
    disty = numpy.linalg.norm(point2 - point3)
    distydiv = disty / 2
    scay = round(distydiv, 8)

    # Coords for poly
    co = mat_world * Vector(poly.center)

    # Idk what's happening here
    forward = poly.normal.copy()
    forward.rotate(mat_world)
    right = forward.cross(up).normalized()  # Vector.length closer to 1.0
    up = right.cross(forward)

    rot = Matrix((right, up, -forward)).transposed().normalized().to_4x4()
    mat = Matrix.Translation(co) * rot

    # Deconstructing Polygon Matrix
    # Deconstructing Polygon Matrix
    loc, rot, sca = mat.decompose()
    # print(rot)
    rotxyz = rot.to_euler('XYZ')

    # Location
    # Rounding
    print("\tConverting location")
    locx = round(loc.x, 8)
    locy = round(loc.y, 8)
    locz = round(loc.z, 8)

    # Rotation
    # Converting from radians to degrees and rounding
    print("\tConverting rotation")
    radx = rotxyz.x
    rady = rotxyz.y
    radz = rotxyz.z
    rotx = round(math.degrees(radx), 8)
    roty = round(math.degrees(rady), 8)
    rotz = round(math.degrees(radz), 8)

    # Print scale
    print("Scale-X", scax)
    print("Scale-Y", scay)

    # Add object
    bpy.ops.mesh.primitive_plane_add(radius=1, location=co, rotation=(radx, rady, radz))
    bpy.context.object.name = "CT.Block." + str(counter)
    bpy.context.object.scale = ((scax, scay, 1))

    mat2 = bpy.context.object.matrix_world

    # Deconstructing Polygon Matrix
    loc, rot, sca = mat2.decompose()
    # print(rot)
    rotxyz = rot.to_euler('XYZ')

    # Location
    # Rounding
    print("\tConverting location")
    locx = round(loc.x, 8)
    locy = round(loc.y, 8)
    locz = round(loc.z, 8)

    # Rotation
    # Converting from radians to degrees and rounding
    print("\tConverting rotation")
    radx = rotxyz.x
    rady = rotxyz.y
    radz = rotxyz.z
    rotx = round(math.degrees(radx), 8)
    roty = round(math.degrees(rady), 8)
    rotz = round(math.degrees(radz), 8)

    newPlane(locx, locy, locz, rotx, roty, rotz, scax, scay)

    # Delete all verticies from list
    del vertlist[:]

for i in level['tiles']:
    i['objsParams'].append({"Name": "Smoothness", "Value": "0.5"})
    i['objsParams'].append({"Name": "Metallic", "Value": "0"})
    i['objsParams'].append({"Name": "Killable", "Value": "True"})
    i['objsParams'].append({"Name": "Color", "Value": "1F1F1F"})
    i['objsParams'].append({"Name": "Name", "Value": ""})
    i['objsParams'].append({"Name": "EmissionStrength", "Value": "0"})
    i['objsParams'].append({"Name": "Emission", "Value": "1F1F1F"})

with open(fullname, mode='w') as a:
    a.write(json.dumps(level, indent=4))
print("\n")
print('Output to location :: {0.name}'.format(a))

print('Finished at:', datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
print("Took:", datetime.datetime.now() - startTime, "to complete")
