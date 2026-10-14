# =====================================================================
# 14_ml_iris.py —— 機器學習:用「決策邊界」看懂分類器
# =====================================================================
# 參考:姜偉生《AI時代Math元年:用Python全精通機器學習》
#   這本書的招牌圖:把平面鋪滿網格(10 號檔的 meshgrid),
#   讓模型對「每一個格點」做預測,再用顏色塗出來 → 決策邊界
#   不同演算法的邊界形狀完全不同,一看就懂它們的「個性」
#
# 這個檔案學什麼:
#   1. sklearn 的固定套路:建立模型 → fit → predict → score
#   2. 訓練集 / 測試集;過擬合 vs 欠擬合
#   3. 六種分類器的決策邊界:KNN、樸素貝氏、LDA、QDA、SVM、決策樹
#   4. 混淆矩陣、交叉驗證
#   5. 無監督學習:K-means 分群、高斯混合模型(GMM)
#
# 為了能「畫出來」,大部分例子只用 2 個特徵:花瓣長、花瓣寬
# =====================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import (LinearDiscriminantAnalysis,
                                           QuadraticDiscriminantAnalysis)
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, adjusted_rand_score
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

iris = load_iris()
X_all, y = iris.data, iris.target       # X_all:4 個特徵
X = X_all[:, 2:4]                       # 只取第 2、3 欄:花瓣長、花瓣寬 → (150, 2)
names = iris.target_names

LIGHT = ListedColormap(["#c6dbef", "#fdd0a2", "#c7e9c0"])   # 背景(區域)用淡色
DARK = ["#2171b5", "#d94801", "#238b45"]                    # 樣本點用深色


# %% 1. 切出訓練集、測試集
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=0)
# test_size=0.3   :30% 拿來考試,模型訓練時「看不到」
# stratify=y      :切的時候保持三種花的比例一樣(各 1/3)
# random_state=0  :固定亂數,每次切法一樣
print(X_tr.shape, X_te.shape)                   # (105, 2) (45, 2)
print(np.bincount(y_tr), np.bincount(y_te))     # [35 35 35] [15 15 15]
# ★ 為什麼要切?模型在「看過的資料」上表現好不稀奇(可能只是背答案),
#   在「沒看過的資料」上表現好,才代表它真的學到規律


# %% 2. sklearn 的固定套路(所有模型都一樣)
knn = KNeighborsClassifier(n_neighbors=5)   # (1) 建立模型,設定超參數
knn.fit(X_tr, y_tr)                         # (2) 訓練
y_pred = knn.predict(X_te)                  # (3) 預測
print("測試準確率 =", accuracy_score(y_te, y_pred))   # (4) 評分,也可以寫 knn.score(X_te, y_te)

new_flower = [[4.8, 1.6]]                   # 一朵新花:花瓣長 4.8、寬 1.6(注意是二維 list)
print("預測品種:", names[knn.predict(new_flower)])
print("各品種機率:", knn.predict_proba(new_flower).round(2))
# KNN = 找最近的 5 個鄰居投票;機率 = 5 票裡各品種占幾票


# %% 3. 畫決策邊界的小工具
def plot_boundary(model, ax, title=""):
    # (1) 在資料範圍外多留 0.5,鋪一張 300×300 的網格
    x0, x1 = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y0, y1 = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    XX, YY = np.meshgrid(np.linspace(x0, x1, 300), np.linspace(y0, y1, 300))
    # (2) 把網格「攤平」成 90000 個樣本,shape (90000, 2),丟給模型預測
    grid = np.column_stack([XX.ravel(), YY.ravel()])
    Z = model.predict(grid).reshape(XX.shape)       # (3) 預測完再摺回 (300, 300)
    # (4) 塗顏色:levels 設在 -0.5、0.5、1.5、2.5,讓 0/1/2 各分到一個顏色
    ax.contourf(XX, YY, Z, levels=[-0.5, 0.5, 1.5, 2.5], cmap=LIGHT)
    for k in range(3):
        ax.scatter(X[y == k, 0], X[y == k, 1], color=DARK[k], s=12,
                   edgecolor="white", linewidth=0.5, label=names[k])
    ax.set_xlabel("petal length"); ax.set_ylabel("petal width")
    ax.set_title(title, fontsize=10)


fig, ax = plt.subplots(figsize=(6, 5))
plot_boundary(knn, ax, "KNN, k = 5")
ax.legend(loc="upper left")
plt.show()


# %% 4. 超參數 k:過擬合 vs 欠擬合
fig, axes = plt.subplots(1, 3, figsize=(15, 4.3))
for ax, k in zip(axes, [1, 15, 80]):
    model = KNeighborsClassifier(n_neighbors=k).fit(X_tr, y_tr)   # fit 會回傳模型自己,可以串起來寫
    plot_boundary(model, ax,
                  f"k = {k}   train {model.score(X_tr, y_tr):.2f}  test {model.score(X_te, y_te):.2f}")
fig.tight_layout()
plt.show()
# k = 1 :邊界彎彎曲曲,為了遷就每一個點 → 過擬合(記住了雜訊)
# k = 80:鄰居多到快把整個訓練集都包進來,邊界被「多數決」拖著走 → 欠擬合
# 中間某個 k 最好 —— 怎麼找?看 §7 交叉驗證


# %% 5. 六種分類器,六種邊界
models = {
    "KNN (k=15)":          KNeighborsClassifier(n_neighbors=15),
    "Gaussian Naive Bayes": GaussianNB(),
    "LDA":                 LinearDiscriminantAnalysis(),
    "QDA":                 QuadraticDiscriminantAnalysis(),
    "SVM (RBF kernel)":    SVC(kernel="rbf", C=1.0),
    "Decision Tree (d=3)": DecisionTreeClassifier(max_depth=3, random_state=0),
}
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for ax, (name, model) in zip(axes.flat, models.items()):
    model.fit(X_tr, y_tr)
    plot_boundary(model, ax, f"{name}   test acc = {model.score(X_te, y_te):.3f}")
fig.tight_layout()
plt.show()
# 每種模型的「個性」(對照 12 號檔的高斯分佈):
#   KNN        :看鄰居投票,邊界不規則
#   樸素貝氏   :每個品種一個高斯,但假設特徵「互相獨立」→ 橢圓不能斜
#   LDA        :每個品種一個高斯,而且「共用同一個 Σ」→ 邊界是直線
#   QDA        :每個品種有「自己的 Σ」→ 邊界是二次曲線(拋物線、雙曲線…)
#   SVM        :找「離兩邊最遠」的邊界;RBF 核讓邊界可以彎
#   決策樹     :每次只看一個特徵切一刀 → 邊界全是水平線、垂直線,像樓梯


# %% 6. 混淆矩陣 —— 錯在哪裡?
qda = QuadraticDiscriminantAnalysis().fit(X_tr, y_tr)
fig, ax = plt.subplots(figsize=(4.5, 4))
ConfusionMatrixDisplay.from_estimator(qda, X_te, y_te, display_labels=names,
                                      cmap="Blues", ax=ax)
plt.show()
# 第 i 列第 j 行 = 「真的是 i,被猜成 j」的數量;對角線 = 猜對
# setosa 從來不會錯;錯誤都發生在 versicolor ↔ virginica 之間(它們在圖上本來就有重疊)


# %% 7. 交叉驗證 —— 用來挑超參數
# 只切一次「訓練 / 測試」,結果會受切法影響(運氣)
# 5-fold 交叉驗證:把資料切 5 份,輪流拿 1 份當測試、4 份訓練,做 5 次取平均
ks = range(1, 51)
cv_acc = [cross_val_score(KNeighborsClassifier(n_neighbors=k), X_all, y, cv=5).mean()
          for k in ks]
train_acc = [KNeighborsClassifier(n_neighbors=k).fit(X_all, y).score(X_all, y) for k in ks]

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(ks, train_acc, label="training accuracy")
ax.plot(ks, cv_acc, label="5-fold CV accuracy")
best = ks[int(np.argmax(cv_acc))]
ax.axvline(best, color="gray", linestyle="--", label=f"best k = {best}")
ax.set_xlabel("k"); ax.set_ylabel("accuracy"); ax.legend()
plt.show()
# 這裡用全部 4 個特徵(X_all)
# 訓練準確率在 k 小時最高(背答案),但交叉驗證準確率才是「真實實力」


# %% 8. 無監督學習:K-means —— 不給答案,自己分群
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X_all)
labels = km.labels_                         # 每朵花被分到第幾群(0/1/2,編號是隨便給的)
print("ARI =", round(adjusted_rand_score(y, labels), 3))
# ARI(調整蘭德指數):1 = 跟真正品種完全一致,0 = 跟亂猜一樣
# 不能直接比 labels == y,因為 K-means 的「第 0 群」不一定是 setosa

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", s=15)
axes[0].set_title("true species")
axes[1].scatter(X[:, 0], X[:, 1], c=labels, cmap="viridis", s=15)
centers = km.cluster_centers_[:, 2:4]       # 群中心是 4 維的,只畫花瓣那 2 維
axes[1].scatter(centers[:, 0], centers[:, 1], marker="X", s=200, color="red")
axes[1].set_title("K-means clusters (no labels used)")
for ax in axes:
    ax.set_xlabel("petal length"); ax.set_ylabel("petal width")
plt.show()

# 手肘法:分幾群最好?
inertias = [KMeans(n_clusters=k, n_init=10, random_state=0).fit(X_all).inertia_
            for k in range(1, 9)]
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(range(1, 9), inertias, "o-")
ax.set_xlabel("number of clusters"); ax.set_ylabel("inertia (within-cluster SSE)")
ax.set_title("elbow method")
plt.show()
# inertia = 每個點到自己群中心的距離平方和;群越多一定越小
# 找「下降突然變慢」的拐點(手肘)。鳶尾花的手肘大概在 2~3 —— 因為 versicolor 跟 virginica 很難分開


# %% 9. 高斯混合模型 GMM —— K-means 的「機率版」
# K-means:每個點「硬性」屬於一群,群的形狀是圓的
# GMM    :每一群是一個高斯分佈(有自己的 μ、Σ),形狀可以是斜的橢圓
gmm = GaussianMixture(n_components=3, covariance_type="full", random_state=0).fit(X)
g_labels = gmm.predict(X)
print("GMM ARI =", round(adjusted_rand_score(y, g_labels), 3))
print("第 0 朵花屬於各群的機率:", gmm.predict_proba(X[:1]).round(3))   # 「軟性」分群

t = np.linspace(0, 2 * np.pi, 200)
circle = np.vstack([np.cos(t), np.sin(t)])
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(X[:, 0], X[:, 1], c=g_labels, cmap="viridis", s=15)
for mu, S in zip(gmm.means_, gmm.covariances_):
    lam, V = np.linalg.eigh(S)
    for k in [1, 2]:
        ell = V @ np.diag(k * np.sqrt(lam)) @ circle + mu[:, None]   # 12 號檔 §4 的同一招
        ax.plot(*ell, color="red", lw=1)
ax.set_xlabel("petal length"); ax.set_ylabel("petal width")
ax.set_title("GMM: each cluster is a Gaussian (1σ, 2σ ellipses)")
plt.show()


# =====================================================================
# 練習
#   1. 把 §5 的六個模型改成用 X_all(4 個特徵)訓練,測試準確率有變高嗎?
#      (這時候就畫不出決策邊界了 —— 這就是為什麼教學都用 2 維)
#   2. SVC 的 C 試試 0.01、1、100,畫決策邊界。C 越大越「不肯犯錯」,會怎樣?
#   3. 用 cross_val_score 比較 DecisionTreeClassifier 的 max_depth = 1..10,
#      畫出跟 §7 一樣的「訓練 vs 交叉驗證」曲線
# =====================================================================
# %% 練習區
