# =====================================================================
# 13_numpy_advanced.py —— 寫「數學程式」的四個進階工具
# =====================================================================
# 參考:姜偉生《AI時代Math元年:用Python全精通程式設計》(簡體原名《編程不難》)
#   基本語法 02~08 已經教過了。這裡補的是「用 Python 寫數學」最常用、
#   但初學者最容易卡住的四件事:
#     1. 廣播(broadcasting)—— shape 不同的陣列怎麼一起算
#     2. einsum             —— 用「下標」一行寫完各種矩陣運算
#     3. class              —— 把資料和運算包成一個「物件」
#     4. plotly             —— 可以用滑鼠旋轉、縮放的互動圖
#
# ★ 讀懂這個檔的關鍵:每一行都問自己「現在這個陣列的 shape 是多少?」
# =====================================================================

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.datasets import load_iris

rng = np.random.default_rng(0)


# %% 1. 廣播規則
# 兩個陣列做運算時,numpy 從「最後一個維度」開始往前,一維一維比:
#   長度一樣      → OK
#   其中一個是 1  → 把它「延伸」成跟另一個一樣長(不會真的複製,不佔記憶體)
#   其他情況      → ValueError
a = np.arange(3).reshape(3, 1)      # shape (3, 1):直的一行
b = np.arange(4).reshape(1, 4)      # shape (1, 4):橫的一列
print(a + b)                        # (3, 1) + (1, 4) → (3, 4)
# [[0 1 2 3]
#  [1 2 3 4]
#  [2 3 4 5]]
# 畫成表格想:a 往右延伸成 4 行,b 往下延伸成 3 列,然後逐格相加

# 九九乘法表:一行寫完
n = np.arange(1, 10)
print(n[:, None] * n[None, :])      # None = 在這個位置插入一個長度 1 的維度
# n[:, None] 是 (9, 1),n[None, :] 是 (1, 9) → 結果 (9, 9)


# %% 2. 最常見的錯:(3,) 跟 (3, 1) 不一樣
v = np.array([1, 2, 3])             # shape (3,) —— 一維,沒有「直」或「橫」
M = np.zeros((3, 4))
try:
    print(M + v)                    # (3, 4) vs (3,):最後一維 4 ≠ 3 → 報錯
except ValueError as e:
    print("錯誤:", e)
print(M + v[:, None])               # (3, 4) + (3, 1) → 第 i 列每一格都加 v[i]
# 口訣:想「每一列加不同的數」就要 [:, None];想「每一行加不同的數」就直接加 (4,)


# %% 3. 廣播實戰:一次算出 150 朵花「兩兩之間」的距離
X = load_iris().data                # (150, 4)
diff = X[:, None, :] - X[None, :, :]    # (150, 1, 4) - (1, 150, 4) → (150, 150, 4)
D = np.sqrt((diff ** 2).sum(axis=2))    # 沿最後一維(4 個特徵)加總 → (150, 150)
print(D.shape)
print(D[0, :5].round(3))            # 第 0 朵到第 0~4 朵的距離(第 0 個一定是 0)

fig, ax = plt.subplots(figsize=(5, 4.5))
im = ax.imshow(D, cmap="viridis")   # 把矩陣直接當圖片畫,每一格的顏色 = 數值
fig.colorbar(im, ax=ax)
ax.set_title("pairwise distance matrix")
plt.show()
# 鳶尾花資料是照品種排好的(0~49 setosa、50~99 versicolor、100~149 virginica)
# 所以圖上看得到「方塊」:左上角那塊特別暗 = setosa 彼此很近、跟別人很遠


# %% 4. 迴圈 vs 廣播:速度
t = time.perf_counter()
D_loop = np.zeros((150, 150))
for i in range(150):
    for j in range(150):
        D_loop[i, j] = np.sqrt(((X[i] - X[j]) ** 2).sum())
t_loop = time.perf_counter() - t

t = time.perf_counter()
D_bc = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
t_bc = time.perf_counter() - t

print(f"雙層迴圈 {t_loop:.4f}s   廣播 {t_bc:.5f}s   結果相同 = {np.allclose(D_loop, D_bc)}")
# 實務上直接用 scipy.spatial.distance.cdist(X, X),更快也更省記憶體
# ⚠ 廣播的代價:中間的 diff 是 (150, 150, 4),n 很大時(例如 10 萬筆)記憶體會爆


# %% 5. einsum —— 「愛因斯坦求和」
# 寫法:np.einsum("輸入的下標, 輸入的下標 -> 輸出的下標", 陣列1, 陣列2)
# 規則只有一條:出現在左邊、但「沒出現在箭頭右邊」的下標 → 對它加總
u = rng.random(4)
w = rng.random(4)
A = rng.random((3, 4))
B = rng.random((4, 2))
S = rng.random((4, 4))

print(np.allclose(np.einsum("i,i->", u, w), u @ w))         # 內積   Σ_i u_i w_i
print(np.allclose(np.einsum("ij,jk->ik", A, B), A @ B))     # 矩陣乘 Σ_j A_ij B_jk
print(np.allclose(np.einsum("ij->ji", A), A.T))             # 轉置(沒有加總,只是換位置)
print(np.allclose(np.einsum("i,j->ij", u, w), np.outer(u, w)))  # 外積(沒有加總)
print(np.allclose(np.einsum("ii->", S), np.trace(S)))       # 跡   Σ_i S_ii
print(np.allclose(np.einsum("ii->i", S), np.diag(S)))       # 取對角線
# 好處:公式怎麼寫,程式就怎麼寫 —— 數學課本上的 Σ 可以直接翻譯


# %% 6. einsum 實戰:一次算 150 個二次型(馬氏距離²)
# 12 號檔算馬氏距離是一個點一個點算。如果要算「每一朵花」呢?
#   d²_i = x_iᵀ Σ⁻¹ x_i   (x_i 是第 i 列,已經中心化)
Xc = X - X.mean(axis=0)
S_inv = np.linalg.inv(np.cov(X, rowvar=False))

d2 = np.einsum("ij,jk,ik->i", Xc, S_inv, Xc)    # i 留下來(每朵花一個值),j、k 加總掉
d2_loop = np.array([x @ S_inv @ x for x in Xc]) # 同樣的事用迴圈寫
print(np.allclose(d2, d2_loop))                 # True
print("離中心最遠的 3 朵花:", np.argsort(d2)[-3:][::-1])  # argsort 由小到大,反過來取最大


# %% 7. class —— 把「資料 + 運算」包成一個物件
# 前面的程式都是「一堆變數 + 一堆函式」散在外面。
# 當一組資料(μ、Σ)總是跟同一組運算(pdf、抽樣、畫圖)一起出現,就適合包成 class
class Gaussian2D:
    """二元高斯分佈 N(μ, Σ)"""

    def __init__(self, mu, Sigma):
        # __init__ 是「建構子」:寫 Gaussian2D(...) 的時候會自動執行
        # self = 這個物件自己;self.xxx = 存在物件身上的資料(屬性)
        self.mu = np.asarray(mu, dtype=float)
        self.Sigma = np.asarray(Sigma, dtype=float)
        self._Sigma_inv = np.linalg.inv(self.Sigma)     # 底線開頭 = 慣例上「內部用,外面別碰」
        self._norm = 1 / (2 * np.pi * np.sqrt(np.linalg.det(self.Sigma)))

    def __repr__(self):
        # print(物件) 時顯示的文字;沒寫的話只會顯示一串記憶體位址
        return f"Gaussian2D(mu={self.mu.tolist()}, Sigma={self.Sigma.tolist()})"

    def pdf(self, pts):
        # pts 的最後一維是 2,前面幾維都可以:(n, 2) 或 (200, 200, 2) 都能算
        d = pts - self.mu                                           # 廣播
        q = np.einsum("...i,ij,...j->...", d, self._Sigma_inv, d)   # "..." = 前面任意多維
        return self._norm * np.exp(-0.5 * q)

    def sample(self, n, seed=None):
        return np.random.default_rng(seed).multivariate_normal(self.mu, self.Sigma, size=n)

    def plot(self, ax, lim=3.5):
        xs = np.linspace(-lim, lim, 200)
        XX, YY = np.meshgrid(xs, xs)
        ax.contourf(XX, YY, self.pdf(np.dstack([XX, YY])), levels=12, cmap="Blues")
        pts = self.sample(300, seed=0)
        ax.scatter(pts[:, 0], pts[:, 1], s=3, color="k", alpha=0.4)
        ax.set_aspect("equal")
        ax.set_title(repr(self), fontsize=7)


# %% 8. 使用 class
g = Gaussian2D([0, 0], [[1, 0.8], [0.8, 1]])    # 建立物件 → 自動呼叫 __init__
print(g)                                        # 呼叫 __repr__

# 跟 scipy 比對,確認 pdf 寫對了
pts = rng.normal(size=(5, 2))
print(np.allclose(g.pdf(pts), stats.multivariate_normal(g.mu, g.Sigma).pdf(pts)))

# 建立好幾個物件,每個物件有自己的 μ、Σ,互不干擾
models = [Gaussian2D([0, 0], [[1, 0], [0, 1]]),
          Gaussian2D([1, 0], [[2, 0], [0, 0.5]]),
          Gaussian2D([0, 0], [[1, -0.7], [-0.7, 1]])]
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for ax, m in zip(axes, models):
    m.plot(ax)                                  # 同一個方法,不同的資料
fig.tight_layout()
plt.show()


# %% 9. plotly —— 互動圖
# matplotlib 畫的是「圖片」;plotly 畫的是「網頁」,可以拖曳旋轉、縮放、滑鼠移上去看數值
import plotly.express as px

iris = load_iris(as_frame=True)                 # as_frame=True:直接拿到 pandas 表格
df = iris.frame
df["species"] = iris.target_names[df["target"].to_numpy()]

fig = px.scatter_3d(df, x="petal length (cm)", y="petal width (cm)",
                    z="sepal length (cm)", color="species", opacity=0.8)
fig.update_traces(marker_size=4)
fig.show()
# 在 VS Code 互動視窗(Shift+Enter)裡會直接顯示在右邊
# 用 `py 13_numpy_advanced.py` 整個檔案跑的話,會打開瀏覽器顯示


# =====================================================================
# 練習
#   1. 不用迴圈,用廣播把 X 的每一欄「標準化」:(X - 平均) / 標準差
#      先想好 X.mean(axis=0) 的 shape 是多少,需不需要 [:, None]?
#   2. 用 einsum 寫出「批次矩陣乘法」:As shape (10, 3, 4)、Bs shape (10, 4, 2),
#      算出 10 個 A_k @ B_k,結果 shape (10, 3, 2),跟 As @ Bs 比對
#   3. 幫 Gaussian2D 加一個方法 mahalanobis(self, pts),回傳每個點的馬氏距離
# =====================================================================
# %% 練習區
