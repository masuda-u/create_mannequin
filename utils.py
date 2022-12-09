from libs import scipy as sp
import numpy as np

def calc_ellipse_short_radius(L,a):
  """
  楕円の周の長さと長半径から、短半径を求める
  L:周の長さ
  a:長半径
  """
  k = 0.7 # 離心率初期値
  dk = 0.001  # 簡易微分用
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
  
