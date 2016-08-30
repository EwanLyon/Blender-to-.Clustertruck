import bpy
import math
from mathutils import Vector, Matrix
import json
import os
import datetime

#Get object
obj = bpy.context.active_object
mesh = obj.data

mat_world = obj.matrix_world
up = Vector((0,0,1))

print("\n")
print("Starting")
print("--------------")

#levelname = ("What do you want the level to be called: ")+".clustertruck"
directoryloc = "C:/"
levelname = "0ExporterTesting.clustertruck"
counter = 1

fullname = os.path.join(directoryloc, levelname) 

#Open it as a .json
print("Creating: {}" .format(levelname))
with open(fullname, 'w') as a:
    level = {"tiles":[ ] }

#When adding a new object in .clustertruck
def newPlane(locx, locy, locz, rotx, roty, rotz, scax, scay):
    
    global counter
    
    level['tiles'].append({"x": locx, "y": locy, "z": locz, "scalex": scax, "scaley": scay, "scalez": 0.1, "rotx": rotx, "roty": roty, "rotz": rotz, "type": 8, "waypointType": 0, "wayPointIndex": 0, "id": "Cube", "Index": counter, "objsParams": [], "Behaviours": None, "EventInfo": None})
    
    #print('Saved poly', counter)
    counter = counter + 1

#Analyse polygon's propeterties 
for poly in mesh.polygons:
    
    print("--------------")
    print("Poly:", counter)
    print("--------------")
    
    co = mat_world * Vector(poly.center)

    forward = poly.normal.copy()
    forward.rotate(mat_world)
    right = forward.cross(up).normalized() # Vector.length closer to 1.0
    up = right.cross(forward)

    rot = Matrix((right, up, -forward)).transposed().normalized().to_4x4()
    mat = Matrix.Translation(co) * rot
    
    #Deconstructing Polygon Matrix
    print("Calculating polygon")
    loc, rot, sca = mat.decompose()
    print(rot)
    rotxyz = rot.to_euler('XYZ')
    print(rotxyz)
    
    #Rounding
    print("\tConverting location")
    locx = round(loc.x ,8)
    locy = round(loc.y ,8)
    locz = round(loc.z ,8)
    
    #Rounding
    print("\tConverting scale")
    scax = round(sca.x ,8)
    scay = round(sca.y ,8)
    scaz = round(sca.z ,8)
    
    #Converting from radians to degrees and rounding
    print("\tConverting rotation")
    radx = rotxyz.x
    rady = rotxyz.y
    radz = rotxyz.z
    rotx = round(math.degrees(radx) ,8)
    roty = round(math.degrees(rady) ,8)
    rotz = round(math.degrees(radz) ,8)
    
    print(rotx)
    print(roty)
    print(rotz)
    
    #Add object
    newPlane(locx, locy, locz, rotx, roty, rotz, scax, scay)
    
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

print('Done!')
print(fullname)
print(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
