import math
import bpy
import mathutils
# from math import * to get math functions into namespace

class MakeCylinderGridFromFile(bpy.types.Operator):
    print("MakeCylinderGrid built from file")
    bl_idname = "mesh.make_cylinder"
    bl_label = "Add gridded cylinder (from file)"
    
    def invoke(self, context, event):
        print("Starting to make cylinder grid from file...")
        
        #big cylinder
        c = bpy.ops.mesh.primitive_cylinder_add(vertices = 40, radius = 21, depth = 50, end_fill_type='NGON', view_align=False, enter_editmode=False, location = (0.0, 0.0, 0.0), rotation = (0.0, 0.0, 0.0), layers = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        
        #parameter list of little cylinders [[vertices, radius, depth, location(x, y, z), rotation(x,y,z)], ...]
        parList = []
        
        #loading list from file (read mode)
        file = open("CylinderParameters.txt", "r")
        for line in file:
            v, r, d, l1, l2, l3, r1, r2, r3 = line.strip(" ,()").split("\t")
            parList.append([float(v), float(r), float(d), (float(l1), float(l2), float(l3)), (float(r1), float(r2), float(r3))])
        #end
        print(parList)
        
        #iterating over parameter list, building little cylinders & subtracting them from big one
        for arr in parList:
            cyl = bpy.ops.mesh.primitive_cylinder_add(vertices = arr[0], radius = arr[1], depth = arr[2], end_fill_type='NGON', view_align=False, enter_editmode=False, location = arr[3], rotation = arr[4], layers = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            
            objects = bpy.data.objects
            
            target = objects["Cylinder"] #big: c
            cutter = objects["Cylinder.001"] #little: cyl
            
            cutter.select = True
            target.select = False
            
            phi = math.pi/12
            theta = math.pi/8
            
            #bpy.context.scene.cursor_location = (arr[3][0], arr[3][1], 25)
            bpy.context.area.spaces[0].cursor_location = (arr[3][0], arr[3][1], 25)
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            bpy.ops.transform.rotate(value = theta, axis=(0, 1, 0))
            bpy.ops.transform.rotate(value = phi, axis=(0, 0, 1))
            
            bpy.context.scene.objects.active = target
            target.select = True
            
            #b^2 - 4ac
            exists1 = False
            exists2 = False
            
            discriminant1 = (2*math.tan(phi)*arr[3][1] - (2*(math.tan(phi)**2)*arr[3][0])**2 - 4*(1+(math.tan(phi)**2))*((math.tan(phi)**2)*(arr[3][1]**2)+(arr[3][0]**2)-2*math.tan(phi)*arr[3][0]*arr[3][1]-(arr[1]**2)))
            
            #declaring outside scope of conditionals (is it necessary?)
            x1 = 0
            y1 = 0
            x2 = 0
            y2 = 0
            
            if (discriminant1 >= 0):
                x1 = ((-2*math.tan(phi)*arr[3][1]-2*(math.tan(phi)**2)*arr[3][0]) + math.sqrt((2*math.tan(phi)*arr[3][1] - (2*(math.tan(phi)**2)*arr[3][0])**2 - 4*(1+(math.tan(phi)**2))*((math.tan(phi)**2)*(arr[3][1]**2)+(arr[3][0]**2)-2*math.tan(phi)*arr[3][0]*arr[3][1]-(arr[1]**2))))) / (2*(1+(math.tan(phi)**2)))
                
                y1 = math.tan(phi) * (x1 - arr[3][0]) + arr[3][1]
                
                dist1 = math.sqrt((y1 - arr[3][1])**2 + (x1 - arr[3][0])**2)
                exists1 = True
            #end
            
            discriminant2 = (2*math.tan(phi)*arr[3][1] - (2*(math.tan(phi)**2)*arr[3][0])**2 - 4*(1+(math.tan(phi)**2))*((math.tan(phi)**2)*(arr[3][1]**2)+(arr[3][0]**2)-2*math.tan(phi)*arr[3][0]*arr[3][1]-(arr[1]**2)))
            
            if (discriminant2 >= 0):
                x2 = ((-2*math.tan(phi)*arr[3][1]-2*(math.tan(phi)**2)*arr[3][0]) - math.sqrt((2*math.tan(phi)*arr[3][1] - (2*(math.tan(phi)**2)*arr[3][0])**2 - 4*(1+(math.tan(phi)**2))*((math.tan(phi)**2)*(arr[3][1]**2)+(arr[3][0]**2)-2*math.tan(phi)*arr[3][0]*arr[3][1]-(arr[1]**2))))) / (2*(1+(math.tan(phi)**2)))
                
                y2 = math.tan(phi) * (x2 - arr[3][0]) + arr[3][1]
                
                dist2 = math.sqrt((y2 - arr[3][1])**2 + (x2 - arr[3][0])**2)
                exists2 = True
            #end
            
            #points on circumference of big cylinder
            xOnCyl = 0
            yOnCyl = 0
            
            dth = 0
            #d threshold            
            if (exists1 and exists2):
                print("d1: ")
                print(dist1)
                print("d2: ")
                print(dist2)
                dth = min(dist1, dist2)
                
                if (dist1 < dist2):
                    xOnCyl = x1
                    yOnCyl = y1
                else:
                    xOnCyl = x2
                    yOnCyl = y2
                #end
            elif (exists1):
                dth = dist1
                xOnCyl = x1
                yOnCyl = y1
            elif (exists2):
                dth = dist2
                xOnCyl = x2
                yOnCyl = y2
            #end
            
            #d = height cylinder * tan(theta)
            d = 50 * math.tan(theta)
            xend = -d * math.cos(phi) + arr[3][0]
            yend = -d * math.sin(phi) + arr[3][1]
            
            print("x end, y end: ")
            print(xend, yend)
            
            print(d)
            
            if ((xend**2 + yend**2) < (21 - (arr[1] * math.cos(theta) + math.sin(theta)))**2):
            #if (50 * math.tan(theta) > dth):
                print("passed")
                #boolean modifier
                bool_one = target.modifiers.new(type = "BOOLEAN", name = "bool")
                bool_one.object = cutter
                bool_one.operation = 'DIFFERENCE'
                
                #little cylinder-sized cutout from big cylinder
                bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = bool_one.name)
            #end
            
            #deleting little cylinder
            bpy.context.scene.objects[0].select = True
            bpy.data.objects['Cylinder'].select = False
            bpy.ops.object.delete()
        #end loop over parameter list    
        
        bpy.ops.object.mode_set(mode='OBJECT')
        print(list(bpy.data.objects))
        
        return { "FINISHED" }
    #end invoke
#end MakeCylinderGridFromFile
bpy.utils.register_class(MakeCylinderGridFromFile)