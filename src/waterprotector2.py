"""Faucet Protector"""

import bpy
from mathutils import Matrix

bpy.context.scene.unit_settings.scale_length = 0.001
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS' 

def make_cube(loc, size):
    bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
    obj = bpy.context.active_object
    _size = (size[0]/2, size[1]/2, size[2]/2)
    S = Matrix.Diagonal(_size).to_4x4()
    obj.data.transform(S)
    obj.data.update()
    obj.location.x = loc[0] + _size[0]
    obj.location.y = loc[1] + _size[1]
    obj.location.z = loc[2] + _size[2]
    bpy.context.scene.cursor.location=(0, 0, 0)
    return obj

def make_cylinder(loc, radius, depth):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=radius, depth=depth)
    bpy.context.scene.cursor.location=(0, 0, 0)
    obj = bpy.context.active_object
    obj.location.x = loc[0]
    obj.location.y = loc[1]
    obj.location.z = loc[2] + depth / 2
    bpy.context.scene.cursor.location=(0, 0, 0)
    return obj

def clear():
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
        
def set_active(obj):
    bpy.context.view_layer.objects.active = obj
    
def delete_obj(obj, new_active_obj=None):
    set_active(obj)
    bpy.ops.object.delete()
    if new_active_obj:
        set_active(new_active_obj)
    
def chop(obj, chopper):
    bm = obj.modifiers.new("Chop", 'BOOLEAN')
    bm.object = chopper
    bm.operation = 'DIFFERENCE'
    set_active(obj)
    bpy.ops.object.modifier_apply(modifier=bm.name)
        
def chop_all(objs, chopper, delete=True):
    for obj in objs:
        chop(obj, chopper)
    if delete:
        delete_obj(chopper, objs[0])
        
def join_all(obj):
    set_active(obj)
    bpy.ops.object.select_all()
    bpy.ops.object.join()
            
def water_protecter2():    
    
    width = 150
    depth = 124
#    height_1 = 30
#    height_2 = 90
    height_1 = 10
    height_2 = 50
    height_3  = 3
    pipe_height_1 = 8
    pipe_radius_1 = 56 / 2
    pipe_radius_2 = 30 / 2
    thickness = 2
    front_depth = 30.5
    
    
    z_0 = height_1 + thickness
    x_0 = width / 2
    y_0 = thickness + front_depth + pipe_radius_1
    print(y_0) 
    
    objs = []

    objs.append(make_cube(loc=(0, 0, 0), size=(width, thickness, height_1)))
    objs.append(make_cube(loc=(0, 0, height_1), size=(width, depth,  thickness)))
    objs.append(make_cube(loc=(0, depth, height_1), size=(width,   2, height_2 + thickness)))
    objs.append(make_cube(loc=(x_0 - pipe_radius_2 - thickness, y_0, z_0), 
        size=((pipe_radius_2 + thickness) * 2,  depth - y_0, height_2)))
    objs.append(make_cube(loc=(x_0 - pipe_radius_1 - thickness, y_0, z_0), 
        size=((pipe_radius_1 + thickness) * 2,  depth - y_0,  pipe_height_1)))
    objs.append(make_cube(loc=(0, 0, z_0), size=(thickness, depth, height_3)))
    objs.append(make_cube(loc=(0, -height_3, 0), 
        size=(thickness, height_3, height_1 + height_3 + thickness)))
    objs.append(make_cube(loc=(width - thickness, 0, z_0), size=(thickness, depth, height_3)))
    objs.append(make_cube(loc=(width - thickness, -height_3, 0), 
        size=(thickness, height_3, height_1 + height_3 + thickness)))
    
    objs.append(make_cylinder(loc=(x_0, y_0, z_0), radius=pipe_radius_1 + thickness, depth=pipe_height_1))
    objs.append(make_cylinder(loc=(x_0, y_0, z_0), radius=pipe_radius_2 + thickness, depth=height_2))
    
    chop_all(objs, make_cylinder(loc=(x_0, y_0, height_1), radius=pipe_radius_1, 
        depth=pipe_height_1))
    chop_all(objs, make_cylinder(loc=(x_0, y_0, height_1), radius=pipe_radius_2, 
        depth=height_2 + thickness))
    chop_all(objs, make_cube(loc=(x_0 - pipe_radius_2, y_0, height_1), 
        size=(pipe_radius_2 * 2, depth - y_0 + thickness, height_2 + thickness)))
    chop_all(objs, make_cube(loc=(x_0 - pipe_radius_1, y_0, height_1), 
        size=(pipe_radius_1 * 2, depth - y_0 + thickness, pipe_height_1)))
        
    join_all(objs[0])
    
       
clear()
water_protecter2()
