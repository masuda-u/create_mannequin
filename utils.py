from libs import scipy as sp
import numpy as np

def get_ellipse_another_radius(L,r):
  """
  楕円の周長と半径rから残されたほうの半径を求める
  L:周の長さ
  r:長半径または短半径
  """
  k = 0.9 # 離心率初期値
  dk = 0.001  # デルタk
  # rが長半径か短半径か判定する
  if 2*np.pi*r > L:
    # rが長半径の場合
    a = r
    # 楕円の周の長さの公式
    def F(k):return 4*a*sp.special.ellipe(k**2)-L 
    # F(k)の微分
    def F_diff(k):return (F(k+dk)-F(k-dk))/(2*dk)
    # ニュートン・ラプソン法で離心率を求める
    for i in range(10):
      k = k - F(k)/F_diff(k)
    # 離心率の式から短半径を求める
    b = np.lib.scimath.sqrt(a**2*(1-k**2))
    return b
  else:
    # rが短半径の場合
    b = r
    # 楕円の周の長さの公式
    def F(k):return 4*np.lib.scimath.sqrt(b**2/(1-k**2))*sp.special.ellipe(k**2)-L 
    # F(k)の微分
    def F_diff(k):return (F(k+dk)-F(k-dk))/(2*dk)
    # ニュートン・ラプソン法で離心率を求める
    for i in range(10):
      k = k - F(k)/F_diff(k)
    # 離心率の式から短半径を求める
    a = np.lib.scimath.sqrt(b**2/(1-k**2))
    return a
  
