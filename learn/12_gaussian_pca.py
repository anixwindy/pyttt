# =====================================================================
# 12_gaussian_pca.py —— 高斯分佈、協方差橢圓、PCA 降維
# =====================================================================
# 參考:姜偉生《AI時代Math元年:用Python全精通統計及機率》(簡體原名《統計至簡》)
#   把 09(鳶尾花資料)、10(曲面、二次型)、11(特徵分解)三個檔案串起來:
#     協方差矩陣 Σ   ——  一團點的「形狀」
#     Σ 的特徵向量   ——  橢圓的長軸、短軸方向
#     PCA            ——  把資料投影到「最散開」的方向上
#
# 這個檔案學什麼:
#   1. 一元高斯:μ、σ 怎麼改變鐘形曲線;68-95-99.7 法則
#   2. 二元高斯:協方差矩陣 Σ 決定等高線橢圓的形狀
#   3. 馬氏距離:考慮了「形狀」的距離
#   4. PCA:手算(特徵分解)→ 用 sklearn 驗證 → 鳶尾花 4 維降到 2 維
# =====================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

rng = np.random.default_rng(42)     # 新式亂數產生器;固定種子 → 每次結果一樣


# %% 1. 一元高斯分佈 N(μ, σ²)
x = np.linspace(-6, 6, 400)
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for mu in [-2, 0, 2]:
    axes[0].plot(x, stats.norm.pdf(x, loc=mu, scale=1), label=f"mu={mu}")
for sigma in [0.5, 1, 2]:
    axes[1].plot(x, stats.norm.pdf(x, loc=0, scale=sigma), label=f"sigma={sigma}")
axes[0].set_title("change mu: shift"); axes[1].set_title("change sigma: spread")
for ax in axes:
    ax.legend()
plt.show()
# μ 決定「位置」,σ 決定「胖瘦」。曲線下面積永遠 = 1(它是機率密度)


# %% 2. 68-95-99.7 法則 —— 用模擬驗證
samples = rng.normal(loc=0, scale=1, size=100_000)
for k in [1, 2, 3]:
    ratio = np.mean(np.abs(samples) < k)        # True 的比例
    exact = stats.norm.cdf(k) - stats.norm.cdf(-k)
    print(f"|x| < {k}σ :模擬 {ratio:.4f}   理論 {exact:.4f}")


# %% 3. 二元高斯:Σ 決定橢圓
# 密度 f(x) ∝ exp(-½ (x-μ)^T Σ⁻¹ (x-μ))
# 指數裡面就是 10 號檔的「二次型」!所以等高線 = 二次型的等高線 = 橢圓
xs = np.linspace(-3, 3, 200)
XX, YY = np.meshgrid(xs, xs)
grid = np.dstack([XX, YY])          # shape (200, 200, 2):每個格點一個 [x, y]

Sigmas = {
    "independent, equal": [[1, 0], [0, 1]],
    "independent, x wider": [[2, 0], [0, 0.5]],
    "positive corr 0.8": [[1, 0.8], [0.8, 1]],
    "negative corr -0.6": [[1, -0.6], [-0.6, 1]],
}
fig, axes = plt.subplots(1, 4, figsize=(15, 4))
for ax, (name, S) in zip(axes, Sigmas.items()):
    S = np.array(S)
    rv = stats.multivariate_normal(mean=[0, 0], cov=S)
    ax.contourf(XX, YY, rv.pdf(grid), levels=12, cmap="Blues")
    pts = rv.rvs(size=300, random_state=1)          # 抽 300 個點疊上去
    ax.scatter(pts[:, 0], pts[:, 1], s=3, color="k", alpha=0.4)
    # 畫出 Σ 的特徵向量(長度 = sqrt(特徵值) = 該方向的標準差)
    lam, V = np.linalg.eigh(S)
    for i in range(2):
        v = V[:, i] * np.sqrt(lam[i]) * 2
        ax.annotate("", xy=v, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color="red", lw=2))
    ax.set_aspect("equal"); ax.set_title(name, fontsize=10)
fig.tight_layout()
plt.show()
# ★ 紅箭頭 = Σ 的特徵向量 = 橢圓的長短軸
#   特徵值越大 → 那個方向越散開


# %% 4. 從資料估計 Σ,畫出 1σ / 2σ / 3σ 橢圓
true_S = np.array([[3.0, 1.2],
                   [1.2, 1.0]])
data = rng.multivariate_normal(mean=[1, 2], cov=true_S, size=500)

mu_hat = data.mean(axis=0)
S_hat = np.cov(data, rowvar=False)
print("估計的 μ =", mu_hat.round(3))
print("估計的 Σ =\n", S_hat.round(3))      # 跟 true_S 很接近

lam, V = np.linalg.eigh(S_hat)
t = np.linspace(0, 2 * np.pi, 200)
circle = np.vstack([np.cos(t), np.sin(t)])
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(data[:, 0], data[:, 1], s=5, alpha=0.4)
for k in [1, 2, 3]:
    # ★ 單位圓 → 沿軸縮放 sqrt(λ) → 轉到特徵方向 → 平移到 μ
    #   這就是 11 號檔的「矩陣 = 變換」直接拿來用
    ellipse = V @ np.diag(k * np.sqrt(lam)) @ circle + mu_hat[:, None]
    ax.plot(*ellipse, lw=1.5, label=f"{k} sigma")
ax.set_aspect("equal"); ax.legend()
ax.set_title("covariance ellipses")
plt.show()


# %% 5. 馬氏距離 —— 「考慮形狀」的距離
# 歐氏距離 d = sqrt((x-μ)^T (x-μ))
# 馬氏距離 d = sqrt((x-μ)^T Σ⁻¹ (x-μ))   ← 先把橢圓「拉回圓」再量距離
S_inv = np.linalg.inv(S_hat)
p1 = mu_hat + 2.0 * V[:, 1] * np.sqrt(lam[1])   # 沿長軸走 2 個標準差
p2 = mu_hat + 2.0 * V[:, 0] * np.sqrt(lam[0])   # 沿短軸走 2 個標準差

for name, p in [("長軸方向的點", p1), ("短軸方向的點", p2)]:
    d = p - mu_hat
    euc = np.sqrt(d @ d)
    mah = np.sqrt(d @ S_inv @ d)
    print(f"{name}:歐氏 {euc:.3f}   馬氏 {mah:.3f}")
# 歐氏距離差很多,馬氏距離「都是 2」→ 兩個點一樣「不尋常」
# 用途:異常偵測(離群值)、分類(QDA / LDA)


# %% 6. PCA 手算 —— 鳶尾花 4 維 → 2 維
iris = load_iris()
X, y = iris.data, iris.target
names = iris.target_names

Xc = X - X.mean(axis=0)                 # (1) 中心化
S = np.cov(Xc, rowvar=False)            # (2) 協方差矩陣 4×4
lam, V = np.linalg.eigh(S)              # (3) 特徵分解(eigh:對稱矩陣專用,特徵值由小到大)
order = np.argsort(lam)[::-1]           # (4) 改成由大到小
lam, V = lam[order], V[:, order]
Z = Xc @ V[:, :2]                       # (5) 投影到前 2 個主成分 → shape (150, 2)

explained = lam / lam.sum()
print("每個主成分解釋的變異比例 =", explained.round(4))
print("前 2 個加起來 =", explained[:2].sum().round(4))     # 約 97.8%
# ★ 4 維資料丟掉 2 維,只損失約 2% 的資訊


# %% 7. 用 sklearn 驗證
pca = PCA(n_components=2)
Z_sk = pca.fit_transform(X)
print(pca.explained_variance_ratio_.round(4))
# 特徵向量的「正負號」是任意的(v 和 -v 都是特徵向量),所以比絕對值
print(np.allclose(np.abs(Z), np.abs(Z_sk)))     # True


# %% 8. 畫出 PCA 結果 + 碎石圖
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for k, name in enumerate(names):
    axes[0].scatter(Z[y == k, 0], Z[y == k, 1], label=name, alpha=0.7, edgecolor="white")
axes[0].set_xlabel(f"PC1 ({explained[0]:.1%})")
axes[0].set_ylabel(f"PC2 ({explained[1]:.1%})")
axes[0].legend(); axes[0].set_title("iris projected to 2D")

axes[1].bar(range(1, 5), explained, label="each")
axes[1].plot(range(1, 5), np.cumsum(explained), "ro-", label="cumulative")
axes[1].set_xticks(range(1, 5)); axes[1].set_xlabel("component")
axes[1].legend(); axes[1].set_title("scree plot")
fig.tight_layout()
plt.show()
# 左圖:沒有用到品種標籤(PCA 是無監督的),三種花卻自然分開了
# 右圖:碎石圖 —— 看「拐點」決定要留幾個主成分


# %% 9. 主成分在說什麼?看載荷(loadings)
for i in range(2):
    terms = " ".join(f"{V[j, i]:+.2f}·{n}" for j, n in enumerate(iris.feature_names))
    print(f"PC{i+1} = {terms}")
# PC1 幾乎全由「花瓣長、花瓣寬、花萼長」組成 → 可以解讀成「花的大小」
# 這就是 09 號檔熱圖裡那些高相關的特徵 —— PCA 把重複的資訊合併成一個軸


# =====================================================================
# 練習
#   1. 先把 X 標準化(每一欄除以自己的標準差)再做 PCA,
#      explained 比例有什麼變化?為什麼?(提示:np.corrcoef vs np.cov)
#   2. 用 Z(2 維)乘回 V[:, :2].T 再加回平均,重建 4 維資料,
#      算重建誤差 np.mean((X - X_rec)**2)
#   3. 對鳶尾花的每一朵算「到自己品種質心的馬氏距離」,找出最可疑的 3 朵
# =====================================================================
# %% 練習區
