# =====================================================================
# 03_control_flow.py —— if / for / while / 推導式
# =====================================================================
# ★ 核心觀念:Python 沒有 C 式的 for(int i=0; i<n; i++)
#   Python 的 for 永遠是「對一串東西逐一處理」(像 C++ 的 range-for)
# =====================================================================


# %% 1. if / elif / else
# C++ :  if (x > 0) { ... } else if (x == 0) { ... } else { ... }
# Python:冒號 + 縮排。else if 寫成 elif
x = 0
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# 邏輯運算子用英文單字
# C++ :  &&   ||   !
# Python: and  or   not
a, b = 3, 7
if a > 0 and b > 0:
    print("both positive")
if not (a > b):
    print("a <= b")

# ★ 連續比較,C++ 沒有
if 0 < a < 10:          # 等於 0 < a and a < 10
    print("a in (0, 10)")


# %% 2. 三元運算子
# C++ :  int m = (a > b) ? a : b;
# Python:順序不一樣,條件放中間
m = a if a > b else b
print(m)


# %% 3. for + range —— 取代 C 式迴圈
# range(n)         = 0, 1, ..., n-1         for(i=0; i<n; i++)
# range(a, b)      = a, a+1, ..., b-1       for(i=a; i<b; i++)
# range(a, b, s)   = a, a+s, ...            for(i=a; i<b; i+=s)
for i in range(5):
    print(i, end=" ")
print()

for i in range(10, 0, -2):     # 倒著數:10 8 6 4 2
    print(i, end=" ")
print()

# ⚠ range 的右端「不包含」,跟 C++ 的 i < b 一樣


# %% 4. 直接走訪容器
fruits = ["apple", "banana", "cherry"]

# C++ :  for (auto& f : fruits)
for f in fruits:
    print(f)

# 需要索引的時候:enumerate
# C++ :  for (int i = 0; i < n; i++) cout << i << fruits[i];
for i, f in enumerate(fruits):
    print(i, f)

# 兩個串列一起走:zip
prices = [30, 10, 50]
for f, p in zip(fruits, prices):
    print(f"{f}: {p}")


# %% 5. while / break / continue —— 跟 C++ 一樣
n = 27
steps = 0
while n != 1:                   # 考拉茲猜想:偶數除 2,奇數 3n+1
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps += 1                  # ⚠ Python 沒有 ++ 和 --,要寫 += 1
print("steps:", steps)

for i in range(10):
    if i % 2 == 0:
        continue
    if i > 7:
        break
    print(i, end=" ")
print()


# %% 6. for ... else —— C++ 沒有的東西
# else 在「迴圈沒有被 break 打斷」時才執行
# 用途:找東西,找不到時要處理
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            break               # 找到因數
    else:
        return True             # 整個迴圈跑完都沒 break = 質數
    return False

print([p for p in range(30) if is_prime(p)])


# %% 7. ★ 推導式(comprehension)—— Python 最有特色的寫法
# 「把一個迴圈壓成一行,直接產生串列」
#
# C++ :
#   vector<int> sq;
#   for (int i = 0; i < 10; i++) sq.push_back(i * i);
# Python:
sq = [i * i for i in range(10)]
print(sq)

# 加條件(過濾)
evens = [i for i in range(20) if i % 2 == 0]
print(evens)

# 雙層迴圈(先寫外層,再寫內層,順序跟一般 for 一樣)
pairs = [(a, b) for a in range(1, 4) for b in range(a, 4)]
print(pairs)

# 二維陣列:C++ 的 vector<vector<int>> g(3, vector<int>(4, 0))
g = [[0] * 4 for _ in range(3)]     # _ = 「這個變數我不會用到」
g[0][0] = 9
print(g)

# ⚠⚠ 經典大坑:不要寫成 [[0] * 4] * 3
bad = [[0] * 4] * 3
bad[0][0] = 9
print(bad)      # 三列全變 9!因為三列是「同一個」串列的三個參照


# %% 8. match(Python 3.10+)—— 類似 switch
cmd = "go"
match cmd:
    case "stop":
        print("stopping")
    case "go" | "run":          # | = 多個情況
        print("moving")
    case _:                     # _ = default
        print("unknown")


# =====================================================================
# 練習
#   1. 用一行推導式,列出 1..100 裡所有 3 的倍數或 5 的倍數
#   2. 用 for-else 寫:找出串列裡第一個負數,沒有就印 "none"
#   3. 印出 9x9 乘法表(兩層 for + f-string 對齊)
# =====================================================================
# %% 練習區
