import bpy
from bpy.props import *
from bpy_extras import object_utils

import math
import numpy as np
from .libs.scipy import integrate

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
    bust_height = 0.77281065*height-0.04232847491 # バスト高さ
    waist_height = 0.49162933*height+0.12117322816 # ウエスト高さ
    hip_height = 0.54274348*height-0.084138702  # ヒップ高さ
    inseam_height = scene.mannequin_inseam_height # 股下高さ
    knee_height = 0.57452881*inseam_height+0.01251392592  # ひざ高さ
    shoulder_width = scene.mannequin_shoulder_width # 肩幅
    sleeve_length = scene.mannequin_sleeve_length # 袖丈
    foot_length = scene.mannequin_foot_length # 足長さ
    bust = scene.mannequin_bust # バスト周
    waist = scene.mannequin_waist # ウエスト周
    hip = scene.mannequin_hip # ヒップ周
    hip_width = 0.28534994*hip+0.06717028451
    upper_arm_circumference = scene.mannequin_upper_arm_circumference # 上腕周
    thigh_circumference = scene.mannequin_thigh_circumference # 太もも周

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
    bpy.ops.mesh.primitive_cylinder_add(
      radius=bust/(2*math.pi),
      depth=shoulder_height-inseam_height,
      location=(0,0,inseam_height+(shoulder_height-inseam_height)/2)
    )
    # ループカット
    bpy.ops.object.editmode_toggle()
    override = {}
    for area in bpy.context.window.screen.areas:
      if area.type == 'VIEW_3D':
        view_3d = area.spaces[0]
        for region in area.regions:
          if region.type == 'WINDOW':
            override = {
              'scene':bpy.context.scene,
              'region':region,
              'area':area,
              'space':view_3d
            }
            break
    bpy.ops.mesh.loopcut_slide(
      override,
      MESH_OT_loopcut = {
          "number_cuts"           : 2,
          "smoothness"            : 0,     
          "falloff"               : 'SMOOTH',  # Was 'INVERSE_SQUARE' that does not exist
          "object_index"          : 0,
          "edge_index"            : 2,
          "mesh_select_mode_init" : (True, False, False)
      },
      TRANSFORM_OT_edge_slide = {
          "value"           : 0,
          "mirror"          : False, 
          "snap"            : False,
          "snap_target"     : 'CLOSEST',
          "snap_point"      : (0, 0, 0),
          "snap_align"      : False,
          "snap_normal"     : (0, 0, 0),
          "correct_uv"      : False,
          "release_confirm" : False
      }
    )
    bpy.ops.object.editmode_toggle()
    mannequin_part_objects.append(context.object)
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
    bpy.ops.mesh.primitive_cylinder_add(
      radius=thigh_circumference/(2*math.pi),
      depth=inseam_height,
      location=(hip_width/2-thigh_circumference/(2*math.pi),0,inseam_height/2)
    )
    mannequin_part_objects.append(context.object)
    mod = context.object.modifiers.new('MyMirror','MIRROR')
    mod.use_axis[0] = True
    mod.mirror_object = mirror_object
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