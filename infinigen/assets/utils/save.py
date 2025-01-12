import os
import json

import bpy
import mathutils
from mathutils import Vector

# from infinigen.assets.utils.object import 

def get_global_bounds(obj):
    obj = bpy.context.object  # 获取当前选中的物体

    # 获取物体的 Bounding Box，在局部坐标系下的 8 个角
    local_bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    # 计算 Bounding Box 的中心点
    center = sum(local_bbox_corners, Vector()) / len(local_bbox_corners)

    return tuple(center)

def get_rotation(obj):
    # 提取物体的朝向（可以用物体的世界坐标系下的局部X、Y、Z轴来表示朝向）
    x_axis = obj.matrix_world.to_3x3() @ Vector((1, 0, 0))  # X轴
    y_axis = obj.matrix_world.to_3x3() @ Vector((0, 1, 0))  # Y轴
    z_axis = obj.matrix_world.to_3x3() @ Vector((0, 0, 1))  # Z轴

    return tuple(x_axis), tuple(y_axis), tuple(z_axis)

def get_bounding_box_center_size(obj):
    center = None
    size = None
    # 确保物体是网格类型
    if obj.type == 'MESH':
        # 获取物体的网格数据
        mesh = obj.data
        
        # 获取物体的所有顶点
        world_vertices = [obj.matrix_world @ v.co for v in mesh.vertices]

        # 计算包围盒的最小和最大坐标
        min_corner = Vector((float('inf'), float('inf'), float('inf')))
        max_corner = Vector((float('-inf'), float('-inf'), float('-inf')))
        
        for vert in world_vertices:
            min_corner = Vector((
                min(min_corner.x, vert.x),
                min(min_corner.y, vert.y),
                min(min_corner.z, vert.z)
            ))
            max_corner = Vector((
                max(max_corner.x, vert.x),
                max(max_corner.y, vert.y),
                max(max_corner.z, vert.z)
            ))
        
        # 输出最小包围盒的中心和尺寸
        center = (min_corner + max_corner) / 2
        size = max_corner - min_corner
    else:
        print("Selected object is not a mesh. Return None for both")
    
    return tuple(center), tuple(size)




def save_scene():
    # Obtain collection of the whole scene.
    collection = bpy.context.scene.collection

    if 'unique_assets' in collection.keys():
        unique_assets_collection = collection.children['unique_assets']
    else:
        print("The key 'unique_assets' not in the collection of scene with collection", collection.keys(), "\nAborting save_scene.")
        return None
    
    # TODO: Save whole scene here.
    
    
    # Save each object here, with the bounding box center, size, 
    object_keys = unique_assets_collection.keys()

    for object_name in object_keys:
        obj = unique_assets_collection.objects[object_name]
        
    
