import bpy
from bpy.props import *
from bpy_extras import object_utils

class CREATEMANNEQUIN_OT_CreateMannequinObject(bpy.types.Operator):

  bl_idname = 'object.create_mannequin_object'
  bl_label = 'mannequin'
  bl_description = 'create mannequin object'
  bl_options = {'REGISTER','UNDO'}

  # depth:FloatProperty(
  #   name='深さ(m)',
  #   description='深さを設定',
  #   default=1.7,
  # )
  # radius:FloatProperty(
  #   name='半径(m)',
  #   description='半径を設定',
  #   default=0.2
  # )

  # メニューを実行したときに呼ばれる関数
  def execute(self, context):
    scene = context.scene
    vertsData = [
      (0,0,0),
      (0,0,scene.mannequin_height),
      (0,0,scene.mannequin_torso_length + scene.mannequin_inseam),
      (0,0,scene.mannequin_inseam),
      (scene.mannequin_shoulder_width/2,0,scene.mannequin_torso_length + scene.mannequin_inseam),
      (-scene.mannequin_shoulder_width/2,0,scene.mannequin_torso_length + scene.mannequin_inseam),
      (-scene.mannequin_shoulder_width/2-scene.mannequin_sleeve_length,0,scene.mannequin_torso_length + scene.mannequin_inseam),
      (scene.mannequin_shoulder_width/2+scene.mannequin_sleeve_length,0,scene.mannequin_torso_length + scene.mannequin_inseam),
    ]
    # edgesData = [(0,1),(1,2),(2,0)]
    # facesData = [(0,1,2)]
    # メッシュ生成
    mesh = bpy.data.meshes.new('Mannequin')
    mesh.from_pydata(vertsData,[],[])
    
    mesh.update()

    # オブジェクト生成
    object_utils.object_data_add(context,mesh,operator=None)
    
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
    layout.prop(scene,'mannequin_torso_length')
    layout.prop(scene,'mannequin_upper_arm_circumference')
    layout.prop(scene,'mannequin_head_height')
    layout.prop(scene,'mannequin_head_circumference')
    layout.prop(scene,'mannequin_shoulder_width')
    layout.prop(scene,'mannequin_back_shoulder_width')
    layout.prop(scene,'mannequin_sleeve_length')
    layout.prop(scene,'mannequin_inseam')
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
  scene.mannequin_torso_length = FloatProperty(
    name='torso_length',
    description='',
    default=.55,
    min=0
  )
  scene.mannequin_upper_arm_circumference = FloatProperty(
    name='upper arm circumference',
    description='',
    default=.26,
    min=0
  )
  scene.mannequin_head_height = FloatProperty(
    name='head height',
    description='',
    default=.24,
    min=0
  )
  scene.mannequin_head_circumference = FloatProperty(
    name='head circumference',
    description='',
    default=.60,
    min=0
  )  
  scene.mannequin_shoulder_width = FloatProperty(
    name='shoulder width',
    description='',
    default=.40,
    min=0
  )
  scene.mannequin_back_shoulder_width = FloatProperty(
    name='back shoulder width',
    description='',
    default=.43,
    min=0
  )
  scene.mannequin_sleeve_length = FloatProperty(
    name='sleeve length',
    description='',
    default=.60,
    min=0
  )
  scene.mannequin_inseam = FloatProperty(
    name='inseam',
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
  del scene.mannequin_head_circumference
  del scene.mannequin_shoulder_width
  del scene.mannequin_back_shoulder_width
  del scene.mannequin_sleeve_length
  del scene.mannequin_inseam
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