import bpy
from bpy.props import *


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
    bpy.ops.mesh.primitive_cylinder_add(
      depth=scene.create_mannequin_depth,
      radius=scene.create_mannequin_radius
    )
    return {'FINISHED'}


class CREATEMANNEQUIN_PT_CreateMannequinObject(bpy.types.Panel):

  bl_label = 'Create Mannequin'
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = 'Create Mannequin'
  bl_context = 'objectmode'

  def draw(self,context):
    scene = context.scene
    layout = self.layout
    # プロパティ追加
    layout.prop(scene,'create_mannequin_depth')
    layout.prop(scene,'create_mannequin_radius')
    layout.separator()
    # 生成ボタンを追加
    layout.operator(CREATEMANNEQUIN_OT_CreateMannequinObject.bl_idname,text='追加',icon='OUTLINER_OB_ARMATURE')


def init_props():
  scene = bpy.types.Scene
  scene.create_mannequin_depth = FloatProperty(
    name='深さ(m)',
    description='深さを設定',
    default=1.7,
    min=0
  )
  scene.create_mannequin_radius = FloatProperty(
    name='半径(m)',
    description='半径を設定',
    default=0.2,
    min=0
  )

def clear_props():
  scene = bpy.types.Scene
  del scene.create_mannequin_depth
  del scene.create_mannequin_radius

# メニューを構築する関数
def menu_fn(self,context):
  layout = self.layout
  layout.separator()
  layout.operator(CREATEMANNEQUIN_OT_CreateMannequinObject.bl_idname)

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