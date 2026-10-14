# =====================================================================
# 07_numpy_pandas.py —— 數值計算與資料分析
# =====================================================================
# numpy  = 快速的多維陣列。底層是 C,所以「整批運算」跟 C++ 一樣快
# pandas = 表格(像 Excel),建立在 numpy 上
#
# ★ 核心觀念:「向量化」—— 不要寫 for 迴圈,對整個陣列一次運算
#   Python 的 for 很慢,numpy 的整批運算很快(差 50~100 倍)
# =====================================================================

import numpy as np          # 慣例縮寫,全世界都這樣寫
import pandas as pd


# %% 1. 建立陣列
a = np.array([1, 2, 3, 4, 5])
print(a, a.dtype)           # dtype = 元素型別,這裡是 int64

print(np.zeros(5))          # [0. 0. 0. 0. 0.]
print(np.ones((2, 3)))      # 2x3 全是 1
print(np.arange(0, 10, 2))  # 像 range,但回傳 numpy 陣列
print(np.linspace(0, 1, 5)) # 0 到 1 均分 5 個點(含兩端)


# %% 2. ★ 向量化運算
a = np.array([1, 2, 3, 4, 5])
print(a * 2)                # [ 2  4  6  8 10]  每個都乘 2
print(a ** 2)               # 每個平方
print(a + a)                # 對應位置相加
print(a.sum(), a.mean(), a.std())

# list 做不到這件事:
# [1, 2, 3] * 2  →  [1, 2, 3, 1, 2, 3]  (是重複,不是乘法)


# %% 3. 布林索引 —— 用條件篩選
a = np.array([5, 12, 3, 18, 7, 21])
mask = a > 10
print(mask)                 # [False  True False  True False  True]
print(a[mask])              # [12 18 21]
print(a[a % 2 == 0])        # 偶數
print((a > 10).sum())       # 有幾個 > 10(True 算 1)


# %% 4. 二維陣列(矩陣)
m = np.array([[1, 2, 3],
              [4, 5, 6]])
print(m.shape)              # (2, 3)  2 列 3 行
print(m[1, 2])              # 6       C++ 寫 m[1][2]
print(m[:, 0])              # 第 0 行(整個 column)
print(m.sum(axis=0))        # 每一行加總 [5 7 9]
print(m.sum(axis=1))        # 每一列加總 [6 15]
print(m.T)                  # 轉置

# 矩陣乘法用 @
A = np.array([[1, 1], [1, 0]])
print(np.linalg.matrix_power(A, 10))    # 費氏數列矩陣,[0][1] = F(10) = 55


# %% 5. 速度比較
import time

n = 10**6
t = time.perf_counter()
s = 0
for i in range(n):
    s += i * i
t1 = time.perf_counter() - t

t = time.perf_counter()
x = np.arange(n, dtype=np.int64)
s2 = (x * x).sum()
t2 = time.perf_counter() - t

print(f"for loop: {t1:.3f}s   numpy: {t2:.4f}s   same={s == s2}")


# %% 6. pandas DataFrame —— 表格
df = pd.DataFrame({
    "name":  ["Ann", "Bob", "Cat", "Dan", "Eve", "Fay"],
    "class": ["A",   "B",   "A",   "B",   "A",   "B"],
    "math":  [88,    72,    95,    60,    79,    91],
    "eng":   [75,    85,    70,    90,    88,    65],
})
print(df)


# %% 7. 看資料
print(df.head(3))           # 前 3 列
print(df.describe())        # ★ 一行做完描述統計
print(df["math"].mean())    # 單一欄的平均


# %% 8. 篩選、新增欄位、排序
print(df[df["math"] >= 80])                 # 數學 80 分以上
df["total"] = df["math"] + df["eng"]        # 新增一欄
print(df.sort_values("total", ascending=False))


# %% 9. 分組統計 —— 樞紐分析
print(df.groupby("class")[["math", "eng"]].mean())
print(df.groupby("class")["total"].agg(["mean", "max", "count"]))


# %% 10. 讀寫檔案
# df.to_csv("scores.csv", index=False)      # 存成 CSV
# df2 = pd.read_csv("scores.csv")           # 讀回來
# df2 = pd.read_excel("file.xlsx")          # Excel 也行(要另外 pip install openpyxl)
print(df[["math", "eng"]].corr())           # 相關係數


# =====================================================================
# 練習
#   1. 用 numpy 算 1..10**6 裡所有 3 的倍數的和(不准用 for)
#   2. 產生 1000 個常態分佈隨機數(np.random.normal),算平均和標準差
#   3. 在 df 裡找出「數學比英文高」的人,並算這些人的平均總分
# =====================================================================
# %% 練習區
