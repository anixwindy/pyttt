# =====================================================================
# 10_meshgrid_surface.py —— 二元函數:網格、等高線、曲面、梯度
# =====================================================================
# 參考:姜偉生《AI時代Math元年:用Python全精通數學要素》(簡體原名《數學要素》)
#       《資料可視化王者:用Python讓AI活躍在圖表世界中》
#   一元函數 y = f(x) 是一條「線」;二元函數 z = f(x, y) 是一張「曲面」
#   要畫曲面,就得先在平面上鋪一張「網格」,在每個格點上算 z
#
# 這個檔案學什麼:
#   1. np.meshgrid —— 鋪網格(這是全部的基礎,一定要懂它的 shape)
#   2. 等高線 contour / contourf —— 從「上面往下看」曲面
#   3. 3D 曲面 plot_surface —— 從「斜上方看」曲面
#   4. 梯度向量 quiver —— 每一點「最陡的上坡方向」,永遠垂直等高線
#   5. 二次型 x^T Q x —— 線性代數和曲面的橋樑(下一個檔案會用到)
# =====================================================================

import numpy as np
import matplotlib.pyplot as plt


# %% 1. meshgrid —— 先用很小的例子看清楚
x = np.array([0, 1, 2])         # x 方向 3 個點
y = np.array([10, 20])          # y 方向 2 個點
XX, YY = np.meshgrid(x, y)
print(XX)
# [[0 1 2]
#  [0 1 2]]      ← 每一列都是 x 複製一次
print(YY)
# [[10 10 10]
#  [20 20 20]]   ← 每一行都是 y 複製一次
print(XX.shape)  # (2, 3) = (len(y), len(x))  ⚠ 注意是 y 在前!
# (XX[i, j], YY[i, j]) 就是第 i 列第 j 行那個格點的座標
# 所以 Z = f(XX, YY) 一行就把「所有格點」的函數值算完(向量化)


# %% 2. 把格點畫出來
x = np.linspace(-2, 2, 9)
y = np.linspace(-2, 2, 9)
XX, YY = np.meshgrid(x, y)
fig, ax = plt.subplots(figsize=(4, 4))
ax.plot(XX, YY, "k.", markersize=4)     # 81 個格點
ax.set_aspect("equal")                  # x、y 等比例,圓才會是圓
ax.set_title("meshgrid: 9 x 9 points")
plt.show()


# %% 3. 定義一個二元函數,算出 Z
def f(x, y):
    # 一個有「山峰」也有「山谷」的函數(MATLAB 經典的 peaks 的簡化版)
    return x * np.exp(-x**2 - y**2)

x = np.linspace(-2, 2, 201)             # 格子要密,圖才平滑
y = np.linspace(-2, 2, 201)
XX, YY = np.meshgrid(x, y)
ZZ = f(XX, YY)                          # shape (201, 201),一次算完 4 萬個點
print(ZZ.shape, ZZ.max().round(4), ZZ.min().round(4))


# %% 4. 等高線 —— 地圖上的等高線就是這個
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

cs = axes[0].contour(XX, YY, ZZ, levels=15, cmap="RdYlBu_r")   # 只畫線
axes[0].clabel(cs, fontsize=7)          # 在線上標出高度
axes[0].set_title("contour")

cf = axes[1].contourf(XX, YY, ZZ, levels=15, cmap="RdYlBu_r")  # 填色
fig.colorbar(cf, ax=axes[1])            # 顏色對照尺
axes[1].set_title("contourf")

for ax in axes:
    ax.set_aspect("equal")
plt.show()
# 一條等高線 = 所有「f(x, y) = 某個常數」的點
# 線越密 → 坡越陡;線越疏 → 越平


# %% 5. 3D 曲面
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection="3d")   # 告訴 matplotlib 這張圖是 3D
ax.plot_surface(XX, YY, ZZ, cmap="RdYlBu_r", linewidth=0, alpha=0.9)
ax.contour(XX, YY, ZZ, levels=15, cmap="RdYlBu_r", offset=ZZ.min() - 0.1)  # 把等高線投影到底部
ax.set_zlim(ZZ.min() - 0.1, ZZ.max())
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.view_init(elev=30, azim=-120)        # 仰角 30°、方位角 -120°
plt.show()
# 小技巧:在 VS Code 互動視窗裡加一行 %matplotlib widget(要裝 ipympl)就能用滑鼠旋轉


# %% 6. 梯度 —— 「最陡的上坡方向」
# ∇f = (∂f/∂x, ∂f/∂y)
# 用 np.gradient 做數值微分(不用自己推公式)
dx = x[1] - x[0]
dZ_dy, dZ_dx = np.gradient(ZZ, dx, dx)  # ⚠ 回傳順序是 (axis 0, axis 1) = (y, x)!

step = 12                               # 箭頭太密看不清,每 12 格取一個
fig, ax = plt.subplots(figsize=(6, 6))
ax.contour(XX, YY, ZZ, levels=15, cmap="RdYlBu_r")
ax.quiver(XX[::step, ::step], YY[::step, ::step],
          dZ_dx[::step, ::step], dZ_dy[::step, ::step])   # quiver = 箭頭場
ax.set_aspect("equal")
ax.set_title("gradient is perpendicular to contours")
plt.show()
# ★ 觀察:箭頭永遠「垂直於等高線」,而且指向山峰
#   機器學習的「梯度下降」就是沿著箭頭的「反方向」一步步走到谷底


# %% 7. 二次型 —— z = x^T Q x
# 把 (x, y) 寫成向量 v = [x, y]^T,Q 是 2×2 對稱矩陣
#   v^T Q v = q11·x² + 2·q12·xy + q22·y²
# Q 的「特徵值正負」決定曲面形狀:
#   兩個都 > 0 → 碗(正定)         兩個都 < 0 → 倒扣的碗(負定)
#   一正一負   → 馬鞍(不定)       有一個 = 0  → 山谷 / 山脊(半正定)
x = np.linspace(-2, 2, 101)
XX, YY = np.meshgrid(x, x)

Qs = {
    "positive definite": np.array([[2, 0.5], [0.5, 1]]),
    "negative definite": np.array([[-2, 0.5], [0.5, -1]]),
    "indefinite (saddle)": np.array([[1, 0], [0, -1]]),
    "semi-definite": np.array([[1, 1], [1, 1]]),
}

fig = plt.figure(figsize=(12, 3.5))
for i, (name, Q) in enumerate(Qs.items(), start=1):
    ZZ = Q[0, 0] * XX**2 + 2 * Q[0, 1] * XX * YY + Q[1, 1] * YY**2
    ax = fig.add_subplot(1, 4, i, projection="3d")
    ax.plot_surface(XX, YY, ZZ, cmap="coolwarm", linewidth=0)
    eig = np.linalg.eigvalsh(Q)         # 對稱矩陣的特徵值(由小到大)
    ax.set_title(f"{name}\neig = {eig.round(2)}", fontsize=9)
fig.tight_layout()
plt.show()
# 這就是「矩陣 ↔ 幾何」的第一座橋:一個 2×2 矩陣決定一張曲面的形狀


# =====================================================================
# 練習
#   1. 畫 f(x, y) = sin(x) * cos(y) 在 [-π, π]² 上的等高線 + 梯度
#   2. 自己推 f(x, y) = x·exp(-x²-y²) 的偏微分公式,
#      跟 np.gradient 的結果比較(np.abs(差).max() 應該很小)
#   3. 寫一個梯度下降:從 (1.5, 1.5) 出發,每步走 -0.1·∇f,
#      走 100 步,把路徑畫在等高線上(提示:要找的是谷底 (-0.707, 0))
# =====================================================================
# %% 練習區
