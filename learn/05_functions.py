# =====================================================================
# 05_functions.py —— 函式、lambda、遞迴、記憶化
# =====================================================================


# %% 1. 定義函式
# C++ :  int add(int a, int b) { return a + b; }
# Python:def + 冒號,不寫型別
def add(a, b):
    return a + b

print(add(2, 3))
print(add("ab", "cd"))      # 型別不檢查,字串也能加


# %% 2. 型別提示(type hints)—— 寫了不會強制,但 VS Code 會幫你檢查
def mul(a: int, b: int) -> int:
    return a * b

print(mul(3, 4))
# 寫給「人」和「編輯器」看的。Pylance 會在你傳錯型別時畫底線


# %% 3. 預設參數與關鍵字參數
def greet(name, greeting="Hello", punct="!"):
    return f"{greeting}, {name}{punct}"

print(greet("Ann"))
print(greet("Ann", "Hi"))
print(greet("Ann", punct="?"))      # 跳過中間的,用名字指定

# ⚠ 預設值不要用可變物件(list / dict)
def bad(x, lst=[]):     # 這個 [] 只會建一次,所有呼叫共用!
    lst.append(x)
    return lst
print(bad(1), bad(2))   # [1, 2] [1, 2] ← 不是你要的

def good(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst
print(good(1), good(2))


# %% 4. 回傳多個值(其實是回傳一個 tuple)
def min_max(arr):
    return min(arr), max(arr)

lo, hi = min_max([3, 1, 4, 1, 5])
print(lo, hi)


# %% 5. lambda —— 一行的匿名函式
# C++ :  auto sq = [](int x) { return x * x; };
sq = lambda x: x * x
print(sq(5))

# 主要用在 sorted / max / min 的 key
words = ["pear", "fig", "banana"]
print(max(words, key=len))


# %% 6. 函式是一般的值,可以傳來傳去
def apply_twice(f, x):
    return f(f(x))

print(apply_twice(sq, 3))           # (3²)² = 81
print(list(map(sq, [1, 2, 3])))     # 對每個元素套用 sq


# %% 7. 遞迴
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)

print(fact(20))

# ⚠ Python 預設遞迴深度上限約 1000 層,超過會 RecursionError
import sys
print(sys.getrecursionlimit())
# 要深一點可以 sys.setrecursionlimit(10**6),但太深還是會讓程式崩潰
# CP 上這是 Python 很大的弱點:DFS 深度 1e5 通常要改成迴圈 + 手動 stack


# %% 8. ★ 記憶化 —— 一行把遞迴變 DP
from functools import cache

@cache                  # 「裝飾器」:自動記住每個參數的回傳值
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(200))         # 沒有 @cache 要跑到宇宙毀滅;有的話瞬間完成
# 這等於 C++ 裡自己開 memo 陣列 + 檢查有沒有算過,Python 一行搞定


# %% 9. global / nonlocal —— 在函式裡改外面的變數
counter = 0

def inc():
    global counter      # 沒有這行,下一行會報錯
    counter += 1

inc(); inc()
print(counter)

# 規則:「讀」外面的變數不用宣告;「改(重新賦值)」才要


# =====================================================================
# 練習
#   1. 寫 gcd(a, b) 遞迴版,跟 math.gcd 比對 100 組隨機數
#   2. 用 @cache 寫:走樓梯一次 1 或 2 階,走 n 階有幾種走法
#   3. 寫一個函式 compose(f, g),回傳「先 g 再 f」的新函式
# =====================================================================
# %% 練習區
