# 01_check_env.py —— 環境檢查。用 Shift+Enter 一格一格跑
# 目的:確認 VS Code 用的是 3.14,而且套件都叫得到

# %% 1. 現在用的是哪個 Python?
import sys
print(sys.version)       # 應該看到 3.14.7
print(sys.executable)    # 應該看到 D:\vs_vs\py314\python.exe

# %% 2. 符號計算:1² + 2² + ... + n² 的公式
from sympy import symbols, summation, simplify, factor
k, n = symbols("k n")
print(factor(summation(k**2, (k, 1, n))))   # n*(n + 1)*(2*n + 1)/6

# %% 3. 打表找規律(CP 用):1..n 裡 a<b 且 (a+b)%3==0 的對數
def brute(n):
    return sum(1 for a in range(1, n + 1)
                 for b in range(a + 1, n + 1)
                 if (a + b) % 3 == 0)

for i in range(1, 13):
    print(i, brute(i))

# %% 4. 畫圖:結果會顯示在互動視窗裡
import matplotlib.pyplot as plt
xs = list(range(1, 31))
plt.plot(xs, [brute(x) for x in xs], marker="o")
plt.title("brute(n)")
plt.show()
