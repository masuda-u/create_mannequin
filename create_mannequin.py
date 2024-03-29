import bpy
from bpy.props import *
import bmesh,mathutils
from bpy.app.translations import pgettext

import math
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
    shoulder_to_elbow = 0.56998292*sleeve_length+0.00114481871  # 肘丈
    upper_arm_circumference = scene.mannequin_upper_arm_circumference # 上腕周
    elbow_circumference =  25.9/36.8*upper_arm_circumference  # ひじ周
    wrist_circumference = 18.1/36.8*upper_arm_circumference # 手首周
    hand_length = 19.5e-2  # 手の長さ
    hand_width = 10e-2 # 手幅
    hand_thick = 3.5e-2  # 手厚さ
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
    foot_width = 10/27.5*foot_length  # 足幅
    foot_thick = 8.5/27.5*foot_length # 足厚

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
    me = bpy.data.meshes.new('arm')
    arm_obj = bpy.data.objects.new('mannequin_arm',me)
    scene = context.scene
    scene.collection.objects.link(arm_obj)
    bm = bmesh.new()
    ret = bmesh.ops.create_circle(
      bm,
      radius=.5, # 直径１とする
      segments=12,
      matrix=mathutils.Matrix.Translation((shoulder_width/2,0,shoulder_height-upper_arm_circumference/(2*math.pi))) @ mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Y')
    )
    ret = bm.faces.new(ret['verts'])  # 肩関節
    shoulder_verts = ret.verts
    ret = bmesh.ops.extrude_face_region(bm,geom=[ret])  # ひじ
    elbow_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(shoulder_to_elbow,0,0),verts=elbow_verts)
    ret = [f for f in ret['geom'] if isinstance(f,bmesh.types.BMFace)]
    ret = bmesh.ops.extrude_face_region(bm,geom=ret)  # 手首
    wrist_verts = [v for v in ret['geom'] if isinstance(v,bmesh.types.BMVert)]
    bmesh.ops.translate(bm,vec=(sleeve_length-shoulder_to_elbow,0,0),verts=wrist_verts)
    T = mathutils.Matrix.Translation((-(shoulder_width/2),0,-(shoulder_height-upper_arm_circumference/(2*math.pi))))
    bmesh.ops.scale(bm,verts=shoulder_verts,vec=(1,upper_arm_circumference/math.pi,upper_arm_circumference/math.pi),space=T)
    bmesh.ops.scale(bm,verts=elbow_verts,vec=(1,elbow_circumference/math.pi,elbow_circumference/math.pi),space=T)
    bmesh.ops.scale(bm,verts=wrist_verts,vec=(1,wrist_circumference/math.pi,wrist_circumference/math.pi),space=T)
    bmesh.ops.mirror(bm,geom=bm.faces,axis='X')
    bm.to_mesh(me)
    bm.free()
    mannequin_part_objects.append(arm_obj)
    # 手
    bpy.ops.mesh.primitive_uv_sphere_add(
      radius=.5,  # 直径１とする
      location=(shoulder_width/2+sleeve_length+hand_length/2-hand_length/10,0,shoulder_height-upper_arm_circumference/(2*math.pi)),
      scale=(hand_length,hand_width,hand_thick)
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
    bmesh.ops.mirror(bm,geom=bm.faces,axis='X')
    bm.to_mesh(me)
    bm.free()
    mannequin_part_objects.append(leg_obj)
    # 足
    bpy.ops.mesh.primitive_uv_sphere_add(
      radius=0.5, # 直径１とする
      location=(hip_width/2-thigh_circumference/(2*math.pi),-(foot_length/4),foot_thick/2),
      scale=(foot_width,foot_length,foot_thick)
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

  bl_label = pgettext('Create Mannequin')
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = pgettext('Mannequin')
  bl_context = 'objectmode'

  def draw(self,context):
    scene = context.scene
    layout = self.layout
    # ラベル
    row = layout.row(align=True)
    row.alignment = 'RIGHT'
    row.label(text=pgettext('Unit (m)'))
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
    layout.operator(CREATEMANNEQUIN_OT_CreateMannequinObject.bl_idname,text=pgettext('Add'),icon='OUTLINER_OB_ARMATURE')

def init_props():
  scene = bpy.types.Scene
  scene.mannequin_height = FloatProperty(
    name=pgettext('(L1) height'),
    description='',
    default=1.7,
    min=0
  )
  scene.mannequin_bust = FloatProperty(
    name=pgettext('(C1) bust'),
    description='',
    default=.9,
    min=0
  )
  scene.mannequin_waist = FloatProperty(
    name=pgettext('(C2) waist'),
    description='',
    default=.65,
    min=0
  )
  scene.mannequin_hip = FloatProperty(
    name=pgettext('(C3) hip'),
    description='',
    default=.91,
    min=0
  )
  scene.mannequin_upper_arm_circumference = FloatProperty(
    name=pgettext('(C4) upper arm circumference'),
    description='',
    default=.26,
    min=0
  )
  scene.mannequin_shoulder_width = FloatProperty(
    name=pgettext('(L2) shoulder width'),
    description='',
    default=.40,
    min=0
  )
  scene.mannequin_sleeve_length = FloatProperty(
    name=pgettext('(L3) sleeve length'),
    description='',
    default=.60,
    min=0
  )
  scene.mannequin_inseam_height = FloatProperty(
    name=pgettext('(L4) inseam_height'),
    description='',
    default=.77,
    min=0
  )
  scene.mannequin_thigh_circumference = FloatProperty(
    name=pgettext('(C5) thign circumference'),
    description='',
    default=.51,
    min=0
  )
  scene.mannequin_foot_length = FloatProperty(
    name=pgettext('(L5) foot length'),
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
  
# # メニューを構築する関数
# def menu_fn(self,context):
#   layout = self.layout
#   layout.separator()
#   layout.operator(CREATEMANNEQUIN_OT_CreateMannequinObject.bl_idname,icon='OUTLINER_OB_ARMATURE')

# Blenderに登録するクラス
classes = [
  CREATEMANNEQUIN_OT_CreateMannequinObject,
  CREATEMANNEQUIN_PT_CreateMannequinObject
]

# アドオン有効化時の処理
def register():
  for c in classes:
    bpy.utils.register_class(c)
  # bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
  init_props()

# アドオン無効化時の処理
def unregister():
  clear_props()
  # bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
  for c in classes:
    bpy.utils.unregister_class(c)