bl_info = {
  'name':'create_mannequin',
  'author':'masuda-u',
  'version':(0,1),
  'blender':(3,0,1),
  'location':'3D View Port > Object',
  'description':'create mannequin from body measurements',
  'warning':'',
  'support':'TESTING',
  'doc_url':'',
  'tracker_url':'',
  'category':'Object'
}

if 'bpy' in locals():
  import importlib
  importlib.reload(create_mannequin)
else:
  from . import create_mannequin
import bpy

# メニューを構築する関数
def menu_fn(self,context):
  layout = self.layout
  layout.separator()
  layout.operator(create_mannequin.CREATEMANNEQUIN_OT_CreateMannequinObject.bl_idname)


# Blenderに登録するクラス
classes = [
  create_mannequin.CREATEMANNEQUIN_OT_CreateMannequinObject
]

# アドオン有効化時の処理
def register():
  for c in classes:
    bpy.utils.register_class(c)
  bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
# アドオン無効化時の処理
def unregister():
  bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
  for c in classes:
    bpy.utils.unregister_class(c)

# メイン処理
if __name__ == '__main__':
  register()