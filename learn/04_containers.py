# =====================================================================
# 04_containers.py —— list / tuple / dict / set
# =====================================================================
# 對照表:
#   Python list   ≈ C++ vector
#   Python tuple  ≈ C++ 不能改的 pair / tuple
#   Python dict   ≈ C++ unordered_map(但會記住插入順序)
#   Python set    ≈ C++ unordered_set
#   ⚠ Python 內建沒有 map / set 的「有序」版本(紅黑樹)
# =====================================================================


# %% 1. list —— 最常用
a = [3, 1, 4, 1, 5]
a.append(9)             # push_back
a.insert(0, 100)        # 插在位置 0(O(n),慢)
last = a.pop()          # pop_back,而且會回傳那個值
print(a, last)
print(len(a), max(a), min(a), sum(a))
print(4 in a)           # 有沒有 4?O(n) 線性搜尋
print(a.index(4))       # 4 在哪?找不到會報錯
print(a.count(1))       # 1 出現幾次


# %% 2. ★ 切片(slicing)—— a[開始:結束:步長]
a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(a[2:5])       # [2, 3, 4]       右端不含
print(a[:3])        # [0, 1, 2]       開頭省略 = 從 0
print(a[7:])        # [7, 8, 9]       結尾省略 = 到底
print(a[-3:])       # [7, 8, 9]       最後三個
print(a[::2])       # [0, 2, 4, 6, 8] 每隔一個
print(a[::-1])      # 反轉!C++ 要 reverse(a.begin(), a.end())
b = a[:]            # 複製一份(淺拷貝)


# %% 3. 排序
a = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(a))                    # 回傳新的,原本不動
print(sorted(a, reverse=True))      # 由大到小
a.sort()                            # 原地排序,回傳 None
print(a)

# ★ key = 「用什麼來比」,取代 C++ 的比較函式
words = ["banana", "kiwi", "apple", "fig"]
print(sorted(words, key=len))                   # 按長度
print(sorted(words, key=lambda w: (len(w), w))) # 先長度,同長再字典序

# 二維:按第二欄排
pts = [(1, 5), (3, 2), (2, 8)]
print(sorted(pts, key=lambda p: p[1]))


# %% 4. ⚠ 參照 vs 複製 —— C++ 寫久的人最容易錯
a = [1, 2, 3]
b = a           # ⚠ 不是複製!b 和 a 是「同一個」串列
b.append(4)
print(a)        # [1, 2, 3, 4]  a 也變了

c = a.copy()    # 這樣才是複製(或 a[:]、list(a))
c.append(5)
print(a, c)

# 規則:Python 的變數全部都是「參照」(像 C++ 的指標)
#       int / str / tuple 不能改,所以感覺不出來
#       list / dict / set 可以改,所以會互相影響


# %% 5. tuple —— 不能改的 list
p = (3, 4)
x, y = p                # 拆包(unpacking),C++17 的 auto [x, y] = p
print(x, y)

a, b = 1, 2
a, b = b, a             # ★ 交換。不需要 swap()
print(a, b)

first, *rest = [1, 2, 3, 4]   # * 收集剩下的
print(first, rest)


# %% 6. dict —— 鍵值對
age = {"alice": 30, "bob": 25}
age["carol"] = 35               # 新增
age["bob"] += 1                 # 修改
print(age)
print(age["alice"])
print("dave" in age)            # 有沒有這個 key?O(1)

# ⚠ 讀不存在的 key 會報錯(C++ 的 map[] 會自動建 0)
# print(age["dave"])            # KeyError
print(age.get("dave", 0))       # 安全讀法:沒有就回傳預設值

for name, a in age.items():     # 走訪鍵和值
    print(name, a)

# 計數的經典寫法
text = "mississippi"
cnt = {}
for ch in text:
    cnt[ch] = cnt.get(ch, 0) + 1
print(cnt)

# dict 推導式
sq = {i: i * i for i in range(5)}
print(sq)


# %% 7. set —— 不重複的集合
s = {3, 1, 4, 1, 5}
print(s)                # {1, 3, 4, 5} 重複的自動去掉
s.add(9)
s.discard(100)          # 刪除,不存在也不報錯
print(4 in s)           # O(1)

a = {1, 2, 3, 4}
b = {3, 4, 5}
print(a & b)            # 交集 {3, 4}
print(a | b)            # 聯集
print(a - b)            # 差集 {1, 2}

# 去重複的一行寫法
print(len(set([1, 1, 2, 3, 3, 3])))   # 3

# ⚠ 空的 set 要寫 set(),寫 {} 會變成空 dict
empty = set()


# =====================================================================
# 練習
#   1. 給一個字串,找出出現最多次的字母(用 dict 計數,再用 max + key)
#   2. 兩個串列,找出共同元素並排序
#   3. 把 [(名字, 分數), ...] 依分數由高到低排,同分照名字
# =====================================================================
# %% 練習區
