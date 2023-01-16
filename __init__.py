bl_info = {
  'name':'create_mannequin',
  'author':'masuda-u',
  'version':(1,0),
  'blender':(3,0,1),
  'location':'3D View Port > Object',
  'description':'create mannequin from body measurements',
  'warning':'',
  'support':'COMMUNITY',
  'doc_url':'',
  'tracker_url':'',
  'category':'Object'
}

# 翻訳辞書
translation_dict = {
  'en_US':{
    ('*','Create Mannequin'):'Create Mannequin',
    ('*','Mannequin'):'Mannequin',
    ('*','Add'):'Add',
    ('*','Unit (m)'):'Unit (m)',
    ('*','(L1) height'):'(L1) height',
    ('*','(C1) bust'):'(C1) bust',
    ('*','(C2) waist'):'(C2) waist',
    ('*','(C3) hip'):'(C3) hip',
    ('*','(C4) upper arm circumference'):'(C4) upper arm circumference',
    ('*','(L2) shoulder width'):'(L2) shoulder width',
    ('*','(L3) sleeve length'):'(L3) sleeve length',
    ('*','(L4) inseam_height'):'(L4) inseam_height',
    ('*','(C5) thign circumference'):'(C5) thign circumference',
    ('*','(L5) foot length'):'(L5) foot length',
  },
  'ja_JP':{
    ('*','Create Mannequin'):'マネキン生成',
    ('*','Mannequin'):'マネキン',
    ('*','Add'):'追加',
    ('*','Unit (m)'):'単位 (m)',
    ('*','(L1) height'):'(L1) 身長',
    ('*','(C1) bust'):'(C1) バスト',
    ('*','(C2) waist'):'(C2) ウエスト',
    ('*','(C3) hip'):'(C3) ヒップ',
    ('*','(C4) upper arm circumference'):'(C4) 上腕周囲',
    ('*','(L2) shoulder width'):'(L2) 肩幅',
    ('*','(L3) sleeve length'):'(L3) そで丈',
    ('*','(L4) inseam_height'):'(L4) 股下高',
    ('*','(C5) thign circumference'):'(C5) 太もも周囲',
    ('*','(L5) foot length'):'(L5) 足底長さ',
  }
}
import os
import sys
if not os.path.join(os.path.dirname(__file__),'.') in sys.path:
  sys.path.append(os.path.join(os.path.dirname(__file__),'.'))
  sys.path.append(os.path.join(os.path.dirname(__file__),'libs'))


if 'bpy' in locals():
  import importlib
  importlib.reload(create_mannequin)
  importlib.reload(utils)
else:
  from . import create_mannequin
  from . import utils

import bpy

# アドオン有効化時の処理
def register():
  create_mannequin.register()
  # 翻訳辞書の登録
  bpy.app.translations.register(__name__,translation_dict)
  
# アドオン無効化時の処理
def unregister():
  bpy.app.translations.unregister(__name__)
  create_mannequin.unregister()

# メイン処理
if __name__ == '__main__':
  register()
