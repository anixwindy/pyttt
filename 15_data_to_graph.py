# =====================================================================
# 15_data_to_graph.py —— 資料處理 → 迴歸預測 → 圖論
# =====================================================================
# 參考:姜偉生《從資料處理到圖論實踐:用Python及AI最強工具預測分析》
#   照書名的路線走三站:
#     A. 資料處理:真實資料一定是髒的 —— 缺失值、離群值、尺度不一
#     B. 預測分析:最小平方法迴歸(= 11 號檔的「投影」)
#     C. 圖論    :把「關係」寫成矩陣,用線性代數分析網路
#
# ★ C 段跟 CP 直接相關:鄰接矩陣、BFS、矩陣快速冪數路徑,都是競程常考的
# =====================================================================

from collections import deque

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import networkx as nx
from sklearn.datasets import load_iris
from sklearn.neighbors import kneighbors_graph

rng = np.random.default_rng(0)

iris = load_iris(as_frame=True)
df = iris.frame.copy()
df.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "target"]
df["species"] = iris.target_names[df["target"].to_numpy()]
df = df.drop(columns="target")
num_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


# =====================================================================
# A. 資料處理
# =====================================================================

# %% A1. 故意把資料弄髒(模擬真實世界)
dirty = df.copy()
idx_nan = rng.choice(len(dirty), size=15, replace=False)
dirty.loc[idx_nan, "sepal_width"] = np.nan      # 15 筆「沒量到」
idx_out = np.sort(rng.choice(len(dirty), size=3, replace=False))
dirty.loc[idx_out, "petal_length"] *= 10        # 3 筆「小數點打錯」
print(dirty.isna().sum())                       # 每一欄有幾個缺失值
print(dirty.describe().round(2))
# 看 petal_length 的 max:正常的花瓣不可能這麼長 → describe() 是抓髒資料的第一步


# %% A2. 缺失值:三種處理方式比一比
print("直接丟掉:", len(df), "→", len(dirty.dropna()), "筆")    # 最簡單,但資料變少

fill_all = dirty["sepal_width"].fillna(dirty["sepal_width"].mean())     # 用整體平均補
fill_group = (dirty.groupby("species")["sepal_width"]                   # 用「同品種」的平均補
                   .transform(lambda s: s.fillna(s.mean())))
# groupby(...).transform:分組計算,但結果「對齊回原本的每一列」(長度還是 150)

truth = df.loc[idx_nan, "sepal_width"]          # 我們偷看真正的值,比較誤差
print("整體平均填補,平均誤差:", (fill_all.loc[idx_nan] - truth).abs().mean().round(3))
print("分組平均填補,平均誤差:", (fill_group.loc[idx_nan] - truth).abs().mean().round(3))
dirty["sepal_width"] = fill_group
# ★ 分組填補比較準,因為不同品種本來就長得不一樣 —— 填補要用「同類」的資訊


# %% A3. 離群值:z-score 法 vs IQR 法
col = dirty["petal_length"]

z = (col - col.mean()) / col.std()
print("z-score 法抓到:", col.index[z.abs() > 3].tolist())

q1, q3 = col.quantile([0.25, 0.75])
iqr = q3 - q1
mask = (col < q1 - 1.5 * iqr) | (col > q3 + 1.5 * iqr)
print("IQR 法抓到:   ", col.index[mask].tolist())
print("真正的離群值:  ", idx_out.tolist())
# 結果:z-score 只抓到 [107, 126],漏了 26;IQR 三個全抓到
# ★ 為什麼?z-score 用的平均和標準差「本身就被離群值拉歪了」:
#   標準差從 1.76 被撐到 6.34,第 26 朵(setosa,1.6 → 16)除以這麼大的標準差,
#   z 只有 1.8 左右,看起來「不夠極端」→ 漏抓(masking 效應)
#   IQR 用四分位數,幾個極端值動不了它 → 比較穩健(robust)

dirty.loc[mask, "petal_length"] = np.nan        # 先標成缺失,再用同品種中位數補
dirty["petal_length"] = (dirty.groupby("species")["petal_length"]
                              .transform(lambda s: s.fillna(s.median())))
clean = dirty
print(clean.describe().round(2))


# %% A4. 標準化 —— 讓不同尺度的特徵可以比較
zscore = (clean[num_cols] - clean[num_cols].mean()) / clean[num_cols].std()   # 平均 0、標準差 1
minmax = (clean[num_cols] - clean[num_cols].min()) / (clean[num_cols].max() - clean[num_cols].min())  # 壓到 [0, 1]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (title, data) in zip(axes, [("raw", clean[num_cols]),
                                    ("z-score", zscore),
                                    ("min-max", minmax)]):
    sns.boxplot(data=data, ax=ax)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=20)
fig.tight_layout()
plt.show()
# KNN、K-means、PCA 都用「距離」,尺度大的特徵會主宰距離 → 用之前通常要標準化


# %% A5. 寬表 ↔ 長表
# 寬表:一列 = 一朵花,4 個特徵各一欄(人好讀)
# 長表:一列 = 一個「(花, 特徵, 數值)」(seaborn 最愛)
long = clean.melt(id_vars="species", value_vars=num_cols,
                  var_name="feature", value_name="cm")
print(long.head())
print(long.shape)                               # (600, 3) = 150 朵 × 4 個特徵

fig, ax = plt.subplots(figsize=(10, 4))
sns.violinplot(data=long, x="feature", y="cm", hue="species", ax=ax, inner="quart")
plt.show()
# 小提琴圖 = 箱型圖 + 機率密度,一張圖比較 4 個特徵 × 3 個品種

print(long.pivot_table(index="species", columns="feature", values="cm",
                       aggfunc="mean").round(2))   # 長表 → 樞紐表(寬)


# =====================================================================
# B. 預測分析:線性迴歸
# =====================================================================

# %% B1. 最小平方法 —— 自己用矩陣解
x = clean["petal_length"].to_numpy()
y = clean["petal_width"].to_numpy()

A = np.column_stack([np.ones_like(x), x])       # 設計矩陣:第一行全是 1(截距),第二行是 x
beta = np.linalg.solve(A.T @ A, A.T @ y)        # ★ 正規方程:(AᵀA) β = Aᵀy
print(f"petal_width ≈ {beta[0]:.3f} + {beta[1]:.3f} × petal_length")

resid = y - A @ beta
print("Aᵀ·殘差 =", (A.T @ resid).round(10))     # ≈ [0, 0]
# ★ 幾何意義(11 號檔 §1 的投影):
#   A @ beta 是 y 在「A 的行空間」上的投影,殘差垂直於 A 的每一行 → Aᵀ·殘差 = 0
#   「最小平方」=「點到平面的最短距離」= 垂直投影


# %% B2. 用 statsmodels:拿到完整的統計報表
model = sm.OLS(y, A).fit()
print(model.params.round(3))                    # 跟 beta 一樣
print("R² =", round(model.rsquared, 4))         # 1 = 完美解釋;0 = 完全沒用
print("p 值 =", model.pvalues.round(6))
# print(model.summary())                        # 想看完整報表就打開這行


# %% B3. 預測 + 區間
x_new = np.linspace(0.5, 7.5, 100)
pred = model.get_prediction(np.column_stack([np.ones_like(x_new), x_new])).summary_frame(alpha=0.05)
print(pred.head(3).round(3))
# mean            :預測值
# mean_ci_*       :「平均」的 95% 信賴區間(很窄 —— 直線本身的不確定性)
# obs_ci_*        :「單一新樣本」的 95% 預測區間(比較寬 —— 還要加上個別差異)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
ax = axes[0]
ax.scatter(x, y, s=12, alpha=0.6)
ax.plot(x_new, pred["mean"], color="red", label="fit")
ax.fill_between(x_new, pred["mean_ci_lower"], pred["mean_ci_upper"],
                color="red", alpha=0.3, label="95% CI of mean")
ax.fill_between(x_new, pred["obs_ci_lower"], pred["obs_ci_upper"],
                color="red", alpha=0.1, label="95% prediction interval")
ax.set_xlabel("petal_length"); ax.set_ylabel("petal_width"); ax.legend()

axes[1].scatter(model.fittedvalues, model.resid, s=12, alpha=0.6)
axes[1].axhline(0, color="red")
axes[1].set_xlabel("fitted"); axes[1].set_ylabel("residual")
axes[1].set_title("residual plot: should look like random noise")
fig.tight_layout()
plt.show()
# 殘差圖如果看得出「形狀」(彎曲、喇叭口),代表直線模型不夠好


# =====================================================================
# C. 圖論:關係 = 矩陣
# =====================================================================

# %% C1. 建一張圖,看它的鄰接矩陣
G = nx.Graph()                                  # 無向圖
G.add_edges_from([(0, 1), (0, 2), (1, 2),       # 三角形 0-1-2
                  (2, 3),                       # 橋
                  (3, 4), (3, 5), (4, 5)])      # 三角形 3-4-5

A = nx.to_numpy_array(G, nodelist=range(6), dtype=int)
print(A)
# A[i, j] = 1 表示 i、j 之間有邊;無向圖 → A 是對稱矩陣
print("度數 =", A.sum(axis=1))                   # 每一列加總 = 有幾個鄰居
print("networkx:", dict(G.degree()))

fig, ax = plt.subplots(figsize=(5, 4))
pos = nx.spring_layout(G, seed=1)               # 自動排版(像彈簧互相推拉);seed 固定排法
nx.draw(G, pos, ax=ax, with_labels=True, node_color="lightsteelblue", node_size=600)
plt.show()


# %% C2. ★ A 的 k 次方 = 長度 k 的走法數
A2 = A @ A
A3 = np.linalg.matrix_power(A, 3)
print("A² =\n", A2)
print("從 0 走 2 步到 3 的走法數 =", A2[0, 3])   # 0→2→3,只有 1 種
print("從 0 走 3 步回到 0 的走法數 =", A3[0, 0]) # 0→1→2→0 和 0→2→1→0,2 種
print("三角形個數 = trace(A³) / 6 =", np.trace(A3) // 6)
print("networkx 數的三角形 =", sum(nx.triangles(G).values()) // 3)
# 為什麼?(A²)[i, j] = Σ_k A[i, k]·A[k, j] = 「i→k→j」對所有中間點 k 加總
# 每個三角形會被 3 個起點 × 2 個方向 = 數 6 次,所以除以 6
# ★ CP:「長度恰為 k 的路徑有幾條,k ≤ 10^18」→ 矩陣快速冪 O(n³ log k)
#   就是 07 號檔用 matrix_power 算費氏數列的同一招


# %% C3. BFS 最短路 —— 自己寫一次,再跟 networkx 對答案
def bfs(adj, s):
    dist = {s: 0}
    q = deque([s])                  # deque 兩端都能 O(1) 進出;list.pop(0) 是 O(n),很慢
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:       # 第一次碰到 = 最短距離(無權圖)
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

adj = {u: list(G.neighbors(u)) for u in G.nodes}    # 鄰接串列,跟 C++ vector<int> adj[N] 一樣
print("自己寫的 BFS:", dict(sorted(bfs(adj, 0).items())))
print("networkx    :", dict(sorted(nx.single_source_shortest_path_length(G, 0).items())))
print("0 到 5 的最短路:", nx.shortest_path(G, 0, 5))


# %% C4. 拉普拉斯矩陣 L = D - A
# D = 度數對角矩陣。L 的特徵值藏著「圖的結構」:
#   L 一定有特徵值 0;特徵值 0 出現幾次 = 圖有幾個連通塊
def laplacian(A):
    return np.diag(A.sum(axis=1)) - A

print("G 的 L 特徵值 =", np.linalg.eigvalsh(laplacian(A)).round(3))

G2 = G.copy()
G2.remove_edge(2, 3)                            # 拆掉橋 → 斷成兩塊
A_2 = nx.to_numpy_array(G2, nodelist=range(6))
print("拆橋後特徵值 =", np.linalg.eigvalsh(laplacian(A_2)).round(3))
print("連通塊數量 =", nx.number_connected_components(G2))
# 拆橋前:0 只出現 1 次,但第二小的特徵值很小 → 「差一點就斷開了」
# 這個第二小的特徵值叫「代數連通度」(Fiedler value),越小越容易切成兩半


# %% C5. 譜分群:用 Fiedler 向量把社群切開
# 空手道俱樂部(Zachary 1977):34 個成員,後來因為吵架分裂成兩派
# 問題:只看「誰跟誰是朋友」,能不能預測分裂後誰跟誰一派?
K = nx.karate_club_graph()
A_k = nx.to_numpy_array(K, nodelist=range(34), weight=None)   # weight=None:只看有沒有邊,不看權重
lam, V = np.linalg.eigh(laplacian(A_k))
fiedler = V[:, 1]                               # 第二小特徵值的特徵向量
pred = (fiedler > 0).astype(int)                # 正的一派、負的一派

truth = np.array([0 if K.nodes[i]["club"] == "Mr. Hi" else 1 for i in range(34)])
acc = max((pred == truth).mean(), (pred != truth).mean())     # 特徵向量正負號任意,兩種都試
print(f"譜分群跟真實分裂的一致率 = {acc:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
pos = nx.spring_layout(K, seed=7)
for ax, c, title in [(axes[0], truth, "real split"), (axes[1], pred, "Fiedler vector sign")]:
    nx.draw(K, pos, ax=ax, node_color=c, cmap="coolwarm", with_labels=True,
            node_size=250, font_size=7, edge_color="lightgray")
    ax.set_title(title)
plt.show()
# 結果約 0.94 = 34 人猜中 32 人。沒有任何「誰支持誰」的資訊,只靠連線結構
# 猜錯的那 2 個人,通常是兩邊都有很多朋友的「中間人」


# %% C6. 終點站:從資料建圖 —— 鳶尾花的 KNN 圖
# 每朵花連到「離它最近的 10 朵花」→ 資料變成一張圖
Xi = clean[num_cols].to_numpy()
W = kneighbors_graph(Xi, n_neighbors=10, include_self=False).toarray()
W = np.maximum(W, W.T)                          # 對稱化:只要有一方把對方當鄰居就連線
Gi = nx.from_numpy_array(W)
print("KNN 圖的連通塊數量 =", nx.number_connected_components(Gi))
lam, V = np.linalg.eigh(laplacian(W))
print("L 最小的 5 個特徵值 =", lam[:5].round(4))

# 用 PCA(12 號檔)把 4 維壓到 2 維,當作畫圖的座標
Xc = Xi - Xi.mean(axis=0)
_, _, Vt = np.linalg.svd(Xc, full_matrices=False)
xy = Xc @ Vt[:2].T
species_code = clean["species"].astype("category").cat.codes.to_numpy()

fig, ax = plt.subplots(figsize=(7, 5))
nx.draw(Gi, pos={i: xy[i] for i in range(len(xy))}, ax=ax,
        node_color=species_code, cmap="viridis", node_size=20,
        edge_color="lightgray", width=0.5)
ax.set_title("iris as a 10-NN graph (layout = PCA)")
plt.show()
# 結果:連通塊 = 2,L 有 2 個特徵值 = 0(印出來的 -0. 是浮點誤差)
#   → setosa 自成一塊,跟另外兩種「完全沒有連線」
#   → versicolor + virginica 連在一起,但第 3 小的特徵值 0.28 偏小 → 「差一點就能切開」
# ★ 把 09 號檔看到的「三團點」,換成圖論的語言重新說了一次:
#   散點圖上的「分得開」= 圖上的「沒有連線」= 拉普拉斯矩陣的「0 特徵值」


# =====================================================================
# 練習
#   1. A3 改用 IQR 法以外的方法:用「同品種」的 z-score 抓離群值,
#      (groupby + transform),抓得到全部 3 個嗎?
#   2. B 段改成用 petal_length、sepal_length 兩個特徵預測 petal_width
#      (設計矩陣多一行),R² 有變高嗎?
#   3. CP 練習:在 C1 的圖上,用 matrix_power 算「從 0 走恰好 20 步到 5」有幾種走法。
#      再自己寫一個 DP(dp[步數][點])驗證答案一樣
# =====================================================================
# %% 練習區
