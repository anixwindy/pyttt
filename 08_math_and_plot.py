# =====================================================================
# 08_math_and_plot.py —— sympy 符號數學 + matplotlib 畫圖 + 打表找規律
# =====================================================================
# sympy      = 會「推導」的數學:解方程、因式分解、微積分、求和公式
# matplotlib = 畫圖
# 最後一段把兩者合起來:CP 的「打表找規律」
# =====================================================================

import sympy as sp
import matplotlib.pyplot as plt


# %% 1. 符號 —— 告訴 sympy 哪些是未知數
x, y, n, k = sp.symbols("x y n k")

expr = (x + 1) ** 3
print(sp.expand(expr))          # 展開
print(sp.factor(x**2 - 5*x + 6))   # 因式分解 (x - 2)*(x - 3)
print(sp.simplify((x**2 - 1) / (x - 1)))   # 化簡 x + 1


# %% 2. 解方程
print(sp.solve(x**2 - 5*x + 6, x))                  # [2, 3]
print(sp.solve([x + y - 10, x - y - 2], [x, y]))    # 聯立:{x: 6, y: 4}
print(sp.solve(x**2 + 1, x))                        # 複數解 [-I, I]


# %% 3. ★ 求和公式 —— CP 最實用的功能
print(sp.factor(sp.summation(k, (k, 1, n))))        # n(n+1)/2
print(sp.factor(sp.summation(k**2, (k, 1, n))))     # n(n+1)(2n+1)/6
print(sp.factor(sp.summation(k**3, (k, 1, n))))     # [n(n+1)/2]²
print(sp.summation(2**k, (k, 0, n)))                # 2^(n+1) - 1


# %% 4. 微積分
f = x**3 - 3*x
print(sp.diff(f, x))                    # 微分 3x² - 3
print(sp.integrate(f, x))               # 不定積分
print(sp.integrate(f, (x, 0, 2)))       # 定積分 = -2
print(sp.limit(sp.sin(x) / x, x, 0))    # 極限 = 1


# %% 5. 數論
print(sp.isprime(10**9 + 7))            # True
print(sp.factorint(360))                # {2: 3, 3: 2, 5: 1}  質因數分解
print(sp.divisors(36))                  # 所有因數
print(sp.totient(36))                   # 歐拉函數 φ(36) = 12


# %% 6. 精確值 vs 浮點數
print(sp.Rational(1, 3) + sp.Rational(1, 6))    # 1/2,精確分數
print(sp.sqrt(8))                               # 2*sqrt(2),不會變成 2.828...
print(sp.N(sp.pi, 50))                          # π 到 50 位


# %% 7. matplotlib 基本圖
import numpy as np

xs = np.linspace(-3, 3, 200)
plt.figure(figsize=(6, 4))
plt.plot(xs, xs**3 - 3*xs, label="x³ - 3x")
plt.plot(xs, 3*xs**2 - 3, label="derivative", linestyle="--")
plt.axhline(0, color="gray", linewidth=0.5)     # 畫 y=0 的線
plt.legend()
plt.grid(True, alpha=0.3)
plt.title("function and its derivative")
plt.show()


# %% 8. ★ 打表找規律 —— 把 CP 的「想不到」變成「看得到」
# 流程:
#   (1) 寫暴力解(慢沒關係)
#   (2) 對小的 n 全部跑出來
#   (3) 看數字、畫圖,猜規律
#   (4) 用 sympy 或更大的 n 驗證猜測
#   (5) 把公式寫回 C++ 送出

# (1) 題目:1..n 裡,有幾對 a<b 使得 gcd(a, b) == 1
from math import gcd

def brute(n):
    return sum(1 for a in range(1, n + 1)
                 for b in range(a + 1, n + 1)
                 if gcd(a, b) == 1)

# (2) 打表
table = [brute(i) for i in range(1, 16)]
print(table)

# (3) 看差分:相鄰兩項相減
diff = [table[i] - table[i - 1] for i in range(1, len(table))]
print(diff)
# 差分 = [1, 2, 2, 4, 2, 6, 4, 6, 4, 10, ...]
# 這正是 φ(n)(歐拉函數)!所以答案 = φ(2) + φ(3) + ... + φ(n)

# (4) 驗證
guess = [sum(sp.totient(i) for i in range(2, m + 1)) for m in range(1, 16)]
print(guess == table)


# %% 9. 把打表結果畫出來 —— 看成長速度
ns = list(range(1, 60))
vals = [brute(i) for i in ns]
plt.figure(figsize=(6, 4))
plt.plot(ns, vals, "o-", markersize=3, label="brute(n)")
plt.plot(ns, [3 / np.pi**2 * i * i for i in ns], label="3n²/π²")
plt.legend()
plt.title("coprime pairs grow like 3n²/π²")
plt.show()
# 看得出來:答案大約是 n² 的 0.3 倍。這種「看到形狀」的直覺,只靠腦袋很難有


# =====================================================================
# 練習
#   1. 用 sympy 求 1·2 + 2·3 + ... + n(n+1) 的公式
#   2. 打表:n 的因數個數 d(n),n = 1..30,畫成長條圖(plt.bar)
#   3. 拿一題你卡住的 CF 題,寫暴力打表,看看有沒有規律
# =====================================================================
# %% 練習區
