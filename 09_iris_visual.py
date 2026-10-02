# =====================================================================
# 09_iris_visual.py —— 鳶尾花資料集:用「看」來認識資料
# =====================================================================
# 參考:姜偉生《資料可視化王者:用Python讓AI活躍在圖表世界中》(簡體原名《可視之美》)
#       《AI時代Math元年:用Python全精通程式設計》(簡體原名《編程不難》)
#   這套書的招牌:從頭到尾都用「鳶尾花資料集」當主角,
#   而且「先畫圖,再算數字」—— 圖是用來培養直覺的,公式是用來確認直覺的
#
# 鳶尾花資料集(Iris,Fisher 1936):
#   150 朵花 × 4 個特徵,3 個品種各 50 朵
#   特徵(單位 cm):
#     sepal length 花萼長、sepal width 花萼寬
#     petal length 花瓣長、petal width 花瓣寬
#   品種:setosa / versicolor / virginica
#
# 這個檔案學什麼:
#   1. 把資料讀成 numpy 矩陣 X(150×4)和 pandas 表格
#   2. 一維:直方圖、箱型圖 —— 看「一個特徵」的分佈
#   3. 二維:散點圖 —— 看「兩個特徵」的關係
#   4. 多維:成對散點圖(pairplot)、熱圖 —— 一眼看完全部
#   5. 用數字確認:均值向量、協方差矩陣、相關係數矩陣
# =====================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris      # sklearn 內建,不用上網下載


# %% 1. 載入資料 —— 資料就是一個矩陣
iris = load_iris()
X = iris.data               # numpy 陣列,shape = (150, 4)
y = iris.target             # 品種編號 0 / 1 / 2,shape = (150,)
feature_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
target_names = iris.target_names            # ['setosa' 'versicolor' 'virginica']

print(X.shape, y.shape)     # (150, 4) (150,)
print(X[:5])                # 前 5 朵花
# ★ 鳶尾花書的核心觀點:
#   「一列(row)= 一個樣本 = 一個點」
#   「一行(column)= 一個特徵 = 一個維度」
#   所以 X 就是「4 維空間裡的 150 個點」,後面所有線代、統計都在處理這些點


# %% 2. 轉成 pandas 表格 —— 方便看、方便分組
df = pd.DataFrame(X, columns=feature_names)
df["species"] = target_names[y]             # 用 y 當索引,把 0/1/2 換成名字
print(df.head())
print(df["species"].value_counts())         # 每個品種各 50 朵
print(df.describe().round(2))               # 描述統計:平均、標準差、四分位數


# %% 3. 一維:直方圖 —— 一個特徵長什麼樣子
fig, axes = plt.subplots(2, 2, figsize=(9, 6))   # 2×2 共 4 張小圖
for ax, name in zip(axes.flat, feature_names):   # axes.flat 把 2×2 攤平成 4 個
    ax.hist(df[name], bins=20, edgecolor="white")
    ax.axvline(df[name].mean(), color="red", linestyle="--", label="mean")
    ax.set_title(name)
    ax.legend()
fig.tight_layout()          # 自動調整間距,避免標題重疊
plt.show()
# 觀察:petal_length 的直方圖有「兩個山峰」(雙峰)
#   → 暗示資料裡混了不同的群體(其實就是 setosa 跟其他兩種)
#   → 只看平均數會錯過這件事!這就是「先畫圖」的價值


# %% 4. 一維 + 分組:依品種畫直方圖
fig, ax = plt.subplots(figsize=(7, 4))
for k, name in enumerate(target_names):
    ax.hist(X[y == k, 2], bins=15, alpha=0.6, label=name)  # 布林索引:只取品種 k 的第 2 欄
ax.set_xlabel("petal_length (cm)")
ax.legend()
plt.show()
# setosa 的花瓣明顯短很多,完全跟其他兩種分開 → 雙峰的真相


# %% 5. 箱型圖 —— 用五個數字概括分佈
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=df, x="species", y="petal_length", ax=ax)
plt.show()
# 箱子:中間線 = 中位數,上下緣 = Q3 / Q1(四分位數)
# 鬚:延伸到 1.5×IQR 以內的最遠點;外面的小點 = 離群值


# %% 6. 二維:散點圖 —— 兩個特徵的關係
fig, ax = plt.subplots(figsize=(6, 5))
for k, name in enumerate(target_names):
    ax.scatter(X[y == k, 2], X[y == k, 3], label=name, alpha=0.7, edgecolor="white")
ax.set_xlabel("petal_length")
ax.set_ylabel("petal_width")
ax.legend()
plt.show()
# 花瓣長和花瓣寬幾乎排成一直線 → 強烈正相關
# 而且三個品種在平面上「各自成團」→ 這就是之後「分類」能做到的原因


# %% 7. 多維:成對散點圖 —— 4 個特徵兩兩配對,一張圖看完
sns.pairplot(df, hue="species", height=1.8, corner=True)   # corner=True 只畫下三角
plt.show()
# 對角線:每個特徵的分佈(依品種上色)
# 非對角線:兩個特徵的散點圖
# 4 維空間畫不出來,但可以看它的 6 個「二維投影」


# %% 8. 用數字確認:均值向量(質心)
mu = X.mean(axis=0)         # axis=0:沿著「列」的方向壓扁 → 每個特徵一個平均
print("整體均值向量 μ =", mu.round(3))
for k, name in enumerate(target_names):
    print(f"{name:>10s} 的質心 =", X[y == k].mean(axis=0).round(3))
# 均值向量 = 這團點的「重心」,是 4 維空間裡的一個點


# %% 9. 協方差矩陣 Σ —— 描述這團點「怎麼散開」
Xc = X - mu                 # 中心化:把重心搬到原點(廣播:每一列都減 mu)
n = X.shape[0]
Sigma = Xc.T @ Xc / (n - 1) # ★ 協方差矩陣的定義:(Xc^T Xc) / (n-1),shape = (4, 4)
print(Sigma.round(3))
print(np.allclose(Sigma, np.cov(X, rowvar=False)))  # 跟 numpy 內建的比對 → True
# 對角線 = 每個特徵的變異數(散多開)
# 非對角線 = 兩個特徵一起變化的程度(正 = 一起變大)
# rowvar=False:告訴 np.cov「每一列是一個樣本」(預設是反過來的,很容易踩坑)


# %% 10. 相關係數矩陣 + 熱圖
corr = df[feature_names].corr()         # 相關係數 = 把協方差標準化到 [-1, 1]
fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1,
            square=True, ax=ax)          # annot=True 把數字寫在格子上
ax.set_title("correlation matrix")
fig.tight_layout()
plt.show()
# petal_length vs petal_width = 0.96:幾乎完全相關 → 兩個特徵「資訊重複」
# → 這就是 12_gaussian_pca.py 要用 PCA 降維的動機


# =====================================================================
# 練習
#   1. 只取 versicolor 的 50 朵花,重算相關係數矩陣。結論跟全部 150 朵一樣嗎?
#      (提示:混在一起的資料可能製造出「假的」相關 —— 辛普森悖論)
#   2. 用 sns.kdeplot 畫 sepal_width 的機率密度曲線,依品種上色
#   3. 不用 np.cov,用 for 迴圈手算 Sigma[0, 1],確認跟矩陣算法一樣
# =====================================================================
# %% 練習區
