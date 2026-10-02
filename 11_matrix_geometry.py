# =====================================================================
# 11_matrix_geometry.py —— 矩陣是「變換」:用圖看懂線性代數
# =====================================================================
# 參考:姜偉生《AI時代Math元年:用Python全精通矩陣及線性代數》(簡體原名《矩陣力量》)
#   這本書最重要的一句話:「矩陣乘法 = 對空間做幾何變換」
#   不要把矩陣當成一堆數字的表格,要看它把「網格」「單位圓」變成什麼樣子
#
# 這個檔案學什麼:
#   1. 向量:長度(範數)、內積、夾角、投影
#   2. 矩陣 A 作用在平面上:旋轉、縮放、剪切、投影
#   3. 行列式 det(A) = 面積的縮放倍率
#   4. 特徵向量:A 作用後「方向不變」的向量
#   5. SVD:任何矩陣 = 旋轉 × 縮放 × 旋轉(單位圓 → 橢圓)
# =====================================================================

import numpy as np
import matplotlib.pyplot as plt


# %% 0. 共用小工具:畫箭頭、畫「網格 + 單位圓」被 A 變換後的樣子
def draw_vec(ax, v, color, label=None):
    # 從原點畫一支箭頭到 v
    ax.quiver(0, 0, v[0], v[1], angles="xy", scale_units="xy", scale=1,
              color=color, label=label)

def setup(ax, lim=3):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axhline(0, color="gray", lw=0.5); ax.axvline(0, color="gray", lw=0.5)
    ax.grid(True, alpha=0.2)

def show_transform(A, title, lim=3):
    # 左圖:原本的網格 + 單位圓;右圖:乘上 A 之後
    t = np.linspace(0, 2 * np.pi, 200)
    circle = np.vstack([np.cos(t), np.sin(t)])          # shape (2, 200):每一「行」是一個點
    lines = np.linspace(-2, 2, 9)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    for ax, M, name in zip(axes, [np.eye(2), A], ["before", "after A"]):
        for c in lines:                                 # 畫網格線(直線經過 A 還是直線)
            seg_v = M @ np.vstack([np.full(50, c), np.linspace(-2, 2, 50)])
            seg_h = M @ np.vstack([np.linspace(-2, 2, 50), np.full(50, c)])
            ax.plot(*seg_v, color="lightsteelblue", lw=0.8)
            ax.plot(*seg_h, color="lightsteelblue", lw=0.8)
        ax.plot(*(M @ circle), color="orange", lw=2)    # 單位圓 → ?
        draw_vec(ax, M[:, 0], "red", "A e1")            # ★ A 的第 1 行 = e1 去的地方
        draw_vec(ax, M[:, 1], "blue", "A e2")           # ★ A 的第 2 行 = e2 去的地方
        setup(ax, lim)
        ax.set_title(name)
    axes[1].legend(loc="upper left")
    fig.suptitle(f"{title}    det = {np.linalg.det(A):.2f}")
    plt.show()
# ★ 關鍵觀念:矩陣 A 的「每一行」就是基底向量 e1=[1,0]、e2=[0,1] 被送去的位置
#   知道 e1、e2 去哪,整張網格去哪就全知道了(因為是線性的)


# %% 1. 向量的基本量
a = np.array([3.0, 1.0])
b = np.array([1.0, 2.0])

print("‖a‖ =", np.linalg.norm(a))           # 長度 = sqrt(3² + 1²)
print("a·b =", a @ b)                        # 內積 = 3·1 + 1·2 = 5
cos_theta = a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
print("夾角 =", np.degrees(np.arccos(cos_theta)).round(2), "度")

# b 在 a 上的投影:proj = (a·b / a·a) a
proj = (a @ b) / (a @ a) * a
print("b 投影到 a =", proj)

fig, ax = plt.subplots(figsize=(5, 4))
draw_vec(ax, a, "red", "a")
draw_vec(ax, b, "blue", "b")
draw_vec(ax, proj, "green", "proj of b on a")
ax.plot([b[0], proj[0]], [b[1], proj[1]], "k--", lw=1)   # 垂線:b - proj 垂直於 a
setup(ax, 3.5)
ax.legend()
plt.show()
print("(b - proj)·a =", ((b - proj) @ a).round(10))      # = 0,真的垂直
# 投影是「最小平方法」「PCA」的核心:找一條線,讓點到線的距離最短


# %% 2. 旋轉矩陣
theta = np.radians(30)
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
show_transform(R, "rotation 30 deg")
# 單位圓還是單位圓、網格只是轉了 → 長度、角度都不變;det = 1(面積不變)


# %% 3. 縮放矩陣(對角矩陣)
S = np.diag([2.0, 0.5])
show_transform(S, "scaling: x*2, y*0.5")
# 單位圓 → 橢圓;det = 2 × 0.5 = 1(拉長又壓扁,面積剛好不變)


# %% 4. 剪切矩陣
H = np.array([[1.0, 1.0],
              [0.0, 1.0]])
show_transform(H, "shear")
# 正方形 → 平行四邊形,det = 1


# %% 5. 投影矩陣(降維!)
P = np.array([[1.0, 0.0],
              [0.0, 0.0]])
show_transform(P, "projection onto x-axis")
# 整個平面被壓成一條線 → det = 0 → 不可逆(資訊丟掉了,回不去)
# ★ det = 0 ⟺ 矩陣不可逆 ⟺ 某個方向被壓扁成 0


# %% 6. 一般矩陣 + 行列式 = 面積倍率
A = np.array([[1.5, 0.5],
              [0.5, 1.0]])
show_transform(A, "general symmetric matrix")
print("det(A) =", np.linalg.det(A))         # 1.5·1 - 0.5·0.5 = 1.25
# 單位圓面積 π → 變換後橢圓面積 1.25π


# %% 7. 特徵值、特徵向量 —— 「方向不變」的那些向量
# A v = λ v :v 被 A 作用後,只是「伸縮 λ 倍」,方向沒變
lam, V = np.linalg.eigh(A)            # A 對稱 → 用 eigh,保證實數、特徵向量互相垂直(eig 可能回傳 +0.j 的複數)
print("特徵值 λ =", lam.round(4))
print("特徵向量(每一行一個)=\n", V.round(4))
for i in range(2):
    v = V[:, i]
    print(f"A v{i} =", (A @ v).round(4), "  λ v =", (lam[i] * v).round(4))   # 兩者相等

# 畫出來:一堆單位向量 u 和 A u,看誰「沒轉彎」
t = np.linspace(0, 2 * np.pi, 24, endpoint=False)
U = np.vstack([np.cos(t), np.sin(t)])
AU = A @ U
fig, ax = plt.subplots(figsize=(6, 6))
for i in range(U.shape[1]):
    ax.plot([U[0, i], AU[0, i]], [U[1, i], AU[1, i]], color="gray", lw=0.8)
ax.plot(*U, "o", color="steelblue", ms=4, label="u (unit circle)")
ax.plot(*AU, "o", color="orange", ms=4, label="A u")
for i in range(2):
    draw_vec(ax, lam[i] * V[:, i], "red")
    draw_vec(ax, -lam[i] * V[:, i], "red")
setup(ax, 2.2)
ax.legend()
ax.set_title("eigenvectors: A u stays on the same line")
plt.show()
# 灰線是 u → Au 的位移。只有紅色那兩個方向,灰線是「沿著自己」伸長的
# 對稱矩陣的特徵向量「互相垂直」,而且剛好是橢圓的長軸、短軸


# %% 8. 特徵分解:A = V Λ V^T(對稱矩陣才這麼漂亮)
Lam = np.diag(lam)
print(np.allclose(A, V @ Lam @ V.T))        # True
# 幾何意義:A = (轉回來) × (沿座標軸縮放) × (轉到特徵方向)
# 任何對稱矩陣都只是「換個角度看的縮放」


# %% 9. SVD 奇異值分解:任何矩陣都能拆
B = np.array([[1.0, 2.0],
              [0.0, 1.5]])                  # 不對稱
Uu, s, Vt = np.linalg.svd(B)
print("奇異值 s =", s.round(4))
print(np.allclose(B, Uu @ np.diag(s) @ Vt))  # B = U Σ V^T

# 分三步畫:單位圓 → V^T(旋轉)→ Σ(縮放)→ U(旋轉)
t = np.linspace(0, 2 * np.pi, 200)
C = np.vstack([np.cos(t), np.sin(t)])
steps = [("circle", np.eye(2)),
         ("V^T", Vt),
         ("Sigma V^T", np.diag(s) @ Vt),
         ("U Sigma V^T = B", B)]
fig, axes = plt.subplots(1, 4, figsize=(14, 3.8))
for ax, (name, M) in zip(axes, steps):
    pts = M @ C
    ax.plot(*pts, color="orange", lw=2)
    ax.plot(*(M @ np.array([[1], [0]])), "ro")      # 追蹤一個點 (1, 0) 跑去哪
    setup(ax, 3)
    ax.set_title(name)
fig.tight_layout()
plt.show()
# ★ 結論:任何 2×2 矩陣 = 轉一下 → 沿軸拉伸 → 再轉一下
#   單位圓最後一定變成橢圓,長半軸 = s[0]、短半軸 = s[1]


# =====================================================================
# 練習
#   1. 找一個矩陣讓 det < 0,用 show_transform 看看發生什麼事
#      (提示:注意紅藍兩支箭頭的「左右順序」—— 平面被翻面了)
#   2. 旋轉矩陣 R 的特徵值是什麼?為什麼是複數?(用幾何解釋)
#   3. 驗證:B 的奇異值平方 = B^T B 的特徵值
# =====================================================================
# %% 練習區
