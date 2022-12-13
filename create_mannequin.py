import bpy
from bpy.props import *
from bpy_extras import object_utils
import bmesh,mathutils

import math
import numpy as np
from .utils import get_ellipse_another_radius

class CREATEMANNEQUIN_OT_CreateMannequinObject(bpy.types.Operator):

  bl_idname = 'object.create_mannequin_object'
  bl_label = 'mannequin'
  bl_description = 'create mannequin object'
  bl_options = {'REGISTER','UNDO'}

  # メニューを実行したときに呼ばれる関数
  def execute(self, context):
    scene = context.scene
    # パラメータ計算
    height = scene.mannequin_height # 身長
    shoulder_height = 0.91149783*height-0.1065205432 # 肩高さ
    shoulder_width = scene.mannequin_shoulder_width # 肩幅
    sleeve_length = scene.mannequin_sleeve_length # 袖丈
    upper_arm_circumference = scene.mannequin_upper_arm_circumference # 上腕周
    bust_height = 0.77281065*height-0.04232847491 # バスト高さ
    bust = scene.mannequin_bust # バスト周
    bust_width = 0.30120742*bust+0.02519265802  # バスト幅
    bust_depth = 2*get_ellipse_another_radius(bust,bust_width/2)  # バスト深さ
    waist_height = 0.49162933*height+0.12117322816 # ウエスト高さ
    waist = scene.mannequin_waist # ウエスト周
    waist_width = 0.31858435*waist+0.03487671899  # ウエスト幅
    waist_depth = 2*get_ellipse_another_radius(waist,waist_width/2) # ウエスト深さ
    hip_height = 0.54274348*height-0.084138702  # ヒップ高さ
    hip = scene.mannequin_hip # ヒップ周
    hip_width = 0.28534994*hip+0.06717028451  # ヒップ幅
    hip_depth = 2*get_ellipse_another_radius(hip,hip_width/2) # ヒップ深さ
    inseam_height = scene.mannequin_inseam_height # 股下高さ
    thigh_circumference = scene.mannequin_thigh_circumference # 太もも周
    thigh_width = 0.28402614*thigh_circumference+0.01431139685  # 太もも幅
    thigh_depth = 2*get_ellipse_another_radius(thigh_circumference,thigh_width/2) # 太もも深さ
    knee_height = 0.57452881*inseam_height+0.01251392592  # ひざ高さ
    knee_width = 0.16185342*thigh_circumference+0.02330633407 # ひざ幅
    knee_depth = 0.12118377*thigh_circumference+0.05265503627 # ひざ深さ
    min_leg_width = 1.49153530e-02*height+0.004015048447414766  # 足首幅
    min_leg_depth = 0.0339574*height+0.01877687228  # 足首深さ
    foot_length = scene.mannequin_foot_length # 足長さ

    mannequin_part_objects = []
    # 頭部
    bpy.ops.mesh.primitive_cylinder_add(
      radius=.6/(2*math.pi), # 頭部周は60cmとする
      depth=.24,  # 頭部高さは24cmとする
      location=(0,0,height-.24/2)
    )
    mannequin_part_objects.append(context.object)
    mirror_object = context.object  # 頭部をミラーオブジェクトとする
    # 胴体
    # 空のメッシュとオブジェクト生成
    me = bpy.data.meshes.new('torso')
    torso_obj = bpy.data.objects.new('mannequin_torso',me)
    # オブジェクト追加
    scene = context.scene
    scene.collection.objects.link(torso_obj)
    # Bmesh生成
    bm = bmesh.new()
    # Bmesh編集
    ret = bmesh.ops.create_circle(
      bm,
      radius=.5, # 直径１とする
      segments=32,
      matrix=mathutils.Matrix.Translation((0,0,shoulder_height))
    )
    ret = bm.faces.new(ret['verts'])  # 肩
    shoulder_verts = ret.verts
    ret = bmesh.ops.extrude_face_region(bm,geom=[ret])  # バスト
    bust_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(0,0,bust_height-shoulder_height),verts=bust_verts)
    ret = [f for f in ret['geom'] if isinstance(f,bmesh.types.BMFace)]
    ret = bmesh.ops.extrude_face_region(bm,geom=ret)  # ウエスト
    waist_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(0,0,waist_height-bust_height),verts=waist_verts)
    ret = [f for f in ret['geom'] if isinstance(f,bmesh.types.BMFace)]
    ret = bmesh.ops.extrude_face_region(bm,geom=ret)  # ヒップ
    hip_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(0,0,hip_height-waist_height),verts=hip_verts)
    ret = [f for f in ret['geom'] if isinstance(f,bmesh.types.BMFace)]
    ret = bmesh.ops.extrude_face_region(bm,geom=ret)  # 股下
    inseam_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(0,0,inseam_height-hip_height),verts=inseam_verts)
    bmesh.ops.scale(bm,verts=shoulder_verts,vec=(shoulder_width,.6/math.pi,1))
    bmesh.ops.scale(bm,verts=bust_verts,vec=(bust_width,bust_depth,1))
    bmesh.ops.scale(bm,verts=waist_verts,vec=(waist_width,waist_depth,1))
    bmesh.ops.scale(bm,verts=hip_verts,vec=(hip_width,hip_depth,1))
    bmesh.ops.scale(bm,verts=inseam_verts,vec=(hip_width,hip_depth,1))
    bm.to_mesh(me)
    bm.free()
    mannequin_part_objects.append(torso_obj)
    # 腕
    bpy.ops.mesh.primitive_cylinder_add(
      radius=upper_arm_circumference/(2*math.pi),
      depth=sleeve_length,
      location=((shoulder_width+sleeve_length)/2,0,shoulder_height - upper_arm_circumference/(2*math.pi)),
      rotation=(0,math.pi/2,0)
    )
    mannequin_part_objects.append(context.object)
    mod = context.object.modifiers.new('MyMirror','MIRROR')
    mod.use_axis[0] = True
    mod.mirror_object = mirror_object
    # 脚
    me = bpy.data.meshes.new('leg')
    leg_obj = bpy.data.objects.new('mannequin_leg',me)
    scene = context.scene
    scene.collection.objects.link(leg_obj)
    bm = bmesh.new()
    ret = bmesh.ops.create_circle(
      bm,
      radius=.5, # 直径１とする
      segments=12,
      matrix=mathutils.Matrix.Translation((hip_width/2-thigh_circumference/(2*math.pi),0,inseam_height))
    )
    ret = bm.faces.new(ret['verts'])  # 股関節
    inseam_verts = ret.verts
    ret = bmesh.ops.extrude_face_region(bm,geom=[ret])  # 膝
    knee_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(0,0,knee_height-inseam_height),verts=knee_verts)
    ret = [f for f in ret['geom'] if isinstance(f,bmesh.types.BMFace)]
    ret = bmesh.ops.extrude_face_region(bm,geom=ret)  # 足
    foot_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(0,0,-knee_height),verts=foot_verts)
    T = mathutils.Matrix.Translation((-(hip_width/2-thigh_circumference/(2*math.pi)),0,0))
    bmesh.ops.scale(bm,verts=inseam_verts,vec=(thigh_width,thigh_depth,1),space=T)
    bmesh.ops.scale(bm,verts=knee_verts,vec=(knee_width,knee_depth,1),space=T)
    bmesh.ops.scale(bm,verts=foot_verts,vec=(min_leg_width,min_leg_depth,1),space=T)
    bm.to_mesh(me)
    bm.free()
    mannequin_part_objects.append(leg_obj)
    # bpy.ops.mesh.primitive_cylinder_add(
    #   radius=thigh_circumference/(2*math.pi),
    #   depth=inseam_height,
    #   location=(hip_width/2-thigh_circumference/(2*math.pi),0,inseam_height/2)
    # )
    # mannequin_part_objects.append(context.object)
    # mod = context.object.modifiers.new('MyMirror','MIRROR')
    # mod.use_axis[0] = True
    # mod.mirror_object = mirror_object
    # 足
    bpy.ops.mesh.primitive_cube_add(
      size=0.1,
      location=(hip_width/2-thigh_circumference/(2*math.pi),-foot_length/2,0.05),
      scale=(1,foot_length/0.1,1)
    )
    mannequin_part_objects.append(context.object)
    mod = context.object.modifiers.new('MyMirror','MIRROR')
    mod.use_axis[0] = True
    mod.mirror_object = mirror_object
    # ミラーモディファイヤを適用
    for obj in mannequin_part_objects:
      for mod in obj.modifiers:
        if mod.type=='MIRROR':
          bpy.context.view_layer.objects.active = obj
          bpy.ops.object.modifier_apply(modifier=mod.name)
    # オブジェクトを統合する
    [obj.select_set(False) for obj in bpy.data.objects]
    [obj.select_set(True) for obj in mannequin_part_objects]
    bpy.ops.object.join()
    context.object.name = 'mannequin'

    return {'FINISHED'}


class CREATEMANNEQUIN_PT_CreateMannequinObject(bpy.types.Panel):

  bl_label = 'Create Mannequin'
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = 'Mannequin'
  bl_context = 'objectmode'

  def draw(self,context):
    scene = context.scene
    layout = self.layout
    # プロパティ追加
    layout.prop(scene,'mannequin_height')
    layout.prop(scene,'mannequin_bust')
    layout.prop(scene,'mannequin_waist')
    layout.prop(scene,'mannequin_hip')
    layout.prop(scene,'mannequin_upper_arm_circumference')
    layout.prop(scene,'mannequin_shoulder_width')
    layout.prop(scene,'mannequin_sleeve_length')
    layout.prop(scene,'mannequin_inseam_height')
    layout.prop(scene,'mannequin_thigh_circumference')
    layout.prop(scene,'mannequin_foot_length')
    layout.separator()
    # 生成ボタンを追加
    layout.operator(CREATEMANNEQUIN_OT_CreateMannequinObject.bl_idname,text='追加',icon='OUTLINER_OB_ARMATURE')


def init_props():
  scene = bpy.types.Scene
  scene.mannequin_height = FloatProperty(
    name='height',
    description='',
    default=1.7,
    min=0
  )
  scene.mannequin_bust = FloatProperty(
    name='bust',
    description='',
    default=.9,
    min=0
  )
  scene.mannequin_waist = FloatProperty(
    name='waist',
    description='',
    default=.65,
    min=0
  )
  scene.mannequin_hip = FloatProperty(
    name='hip',
    description='',
    default=.91,
    min=0
  )
  scene.mannequin_upper_arm_circumference = FloatProperty(
    name='upper arm circumference',
    description='',
    default=.26,
    min=0
  )
  scene.mannequin_shoulder_width = FloatProperty(
    name='shoulder width',
    description='',
    default=.40,
    min=0
  )
  scene.mannequin_sleeve_length = FloatProperty(
    name='sleeve length',
    description='',
    default=.60,
    min=0
  )
  scene.mannequin_inseam_height = FloatProperty(
    name='inseam_height',
    description='',
    default=.77,
    min=0
  )
  scene.mannequin_thigh_circumference = FloatProperty(
    name='thign circumference',
    description='',
    default=.51,
    min=0
  )
  scene.mannequin_foot_length = FloatProperty(
    name='foot length',
    description='',
    default=.26,
    min=0
  )

def clear_props():
  scene = bpy.types.Scene
  del scene.mannequin_height
  del scene.mannequin_bust
  del scene.mannequin_waist
  del scene.mannequin_hip
  del scene.mannequin_upper_arm_circumference
  del scene.mannequin_shoulder_width
  del scene.mannequin_sleeve_length
  del scene.mannequin_inseam_height
  del scene.mannequin_thigh_circumference
  del scene.mannequin_foot_length
  
# メニューを構築する関数
def menu_fn(self,context):
  layout = self.layout
  layout.separator()
  layout.operator(CREATEMANNEQUIN_OT_CreateMannequinObject.bl_idname,icon='OUTLINER_OB_ARMATURE')

# Blenderに登録するクラス
classes = [
  CREATEMANNEQUIN_OT_CreateMannequinObject,
  CREATEMANNEQUIN_PT_CreateMannequinObject
]

# アドオン有効化時の処理
def register():
  for c in classes:
    bpy.utils.register_class(c)
  bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
  init_props()

# アドオン無効化時の処理
def unregister():
  clear_props()
  bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
  for c in classes:
    bpy.utils.unregister_class(c)