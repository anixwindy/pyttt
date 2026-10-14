# 16_pycharm_plot_cells.py
# 目的:測試 PyCharm 的兩件事
#   1. 畫圖(plt.show() 會不會出圖)
#   2. #%% 分格執行(一格一格跑,變數會留著)
# 直譯器:D:\vs_vs\py314\python.exe(numpy / matplotlib / ipykernel 都已裝)

#%% 第 1 格:環境檢查 —— 先確認 PyCharm 用的是哪一支 Python
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

print("Python   :", sys.version.split()[0])
print("執行檔   :", sys.executable)          # 應該是 D:\vs_vs\py314\python.exe
print("numpy    :", np.__version__)
print("matplotlib:", matplotlib.__version__)
print("backend  :", matplotlib.get_backend())  # PyCharm 內會是 interagg 之類的

#%% 第 2 格:準備資料 —— 這一格跑完,x 會留在記憶體裡給後面的格子用
x = np.linspace(0, 2 * np.pi, 100)   # 0 到 2π 切 100 個點
print("x 有幾個點:", len(x))
print("前 3 個:", x[:3])

#%% 第 3 格:折線圖 —— 用上一格的 x(單獨跑這格之前要先跑第 2 格)
plt.figure()
plt.plot(x, np.sin(x), label="sin")
plt.plot(x, np.cos(x), label="cos")
plt.title("sin / cos")
plt.legend()
plt.grid(True)
plt.show()

#%% 第 4 格:散佈圖 + 直方圖,一張圖放兩個子圖
rng = np.random.default_rng(0)       # 固定種子,每次跑結果一樣
pts = rng.normal(size=(200, 2))      # 200 個點,每個點 (x, y)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
ax1.scatter(pts[:, 0], pts[:, 1], s=10)
ax1.set_title("scatter")
ax2.hist(pts[:, 0], bins=20)
ax2.set_title("histogram")
fig.tight_layout()
plt.show()

#%% 第 5 格:改一個數字再跑這一格 —— 體會「只重跑這格」的好處
k = 3                                 # 改成 1、2、5 試試看
plt.figure()
plt.plot(x, np.sin(k * x))
plt.title(f"sin({k}x)")
plt.show()

#%% 第 6 格:出不了圖時的退路 —— 存成 png
plt.figure()
plt.plot(x, x ** 2)
plt.title("x^2")
plt.savefig("16_test_plot.png")       # 存在「工作目錄」底下
print("已存檔:16_test_plot.png")
plt.close()
