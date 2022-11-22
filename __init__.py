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

# アドオン有効化時の処理
def register():
  create_mannequin.register()
  
# アドオン無効化時の処理
def unregister():
  create_mannequin.unregister()

# メイン処理
if __name__ == '__main__':
  register()