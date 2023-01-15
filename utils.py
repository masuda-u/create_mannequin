import numpy as np

def integrate(F,xmin,xmax,n):
  """
  定積分を区分求積法を用いて求める
  F:式
  xmin:区分開始値
  xmax:区分終了値
  n:分割数
  """
  # 短冊の幅dx
  dx = (xmax-xmin)/n
  # 面積の総和
  s = 0
  for i in range(1,n):
    # x,yの値
    x1 = xmin + dx*i
    f1 = F(x1)
    # 面積
    s += dx*f1
  # 面積の総和1(定積分の値)を返す
  return s

def E(k):
  """
  第二種完全楕円積分
  """
  def F(t):return np.sqrt(1-k**2*np.sin(t)**2)
  return integrate(F,0,np.pi/2,2000)

def get_ellipse_another_radius(L,r):
  """
  楕円の周長と半径rから残されたほうの半径を求める
  L:楕円の周長
  r:長半径または短半径
  """
  k = 0.9 # 離心率初期値
  dk = 0.001  # デルタk
  # rが長半径か短半径か判定する
  if 2*np.pi*r > L:
    # rが長半径の場合
    a = r
    # 楕円の周の長さの公式
    def F(k):return 4*a*E(k)-L 
    # F(k)の微分
    def F_diff(k):return (F(k+dk)-F(k-dk))/(2*dk)
    # ニュートン・ラプソン法で離心率を求める
    for i in range(10):
      k = k - F(k)/F_diff(k)
    # 離心率の式から短半径を求める
    b = a*np.lib.scimath.sqrt(1-k**2)
    return b
  else:
    # rが短半径の場合
    b = r
    # 楕円の周の長さの公式
    def F(k):
      return 4*b/np.lib.scimath.sqrt(1-k**2)*E(k)-L 
    # F(k)の微分
    def F_diff(k):return (F(k+dk)-F(k-dk))/(2*dk)
    # ニュートン・ラプソン法で離心率を求める
    for i in range(10):
      k = k - F(k)/F_diff(k)
    # 離心率の式から長半径を求める
    a = b/np.lib.scimath.sqrt(1-k**2)
    return a
  
