# =====================================================================
# 06_stdlib_for_cp.py —— 標準函式庫:對應 C++ STL 的那些東西
# =====================================================================
# 對照表:
#   C++ STL                     Python
#   ------------------------    ------------------------------
#   map<K,int> 計數             collections.Counter
#   map<K,vector> 自動建        collections.defaultdict
#   deque                       collections.deque
#   priority_queue              heapq(⚠ 是「最小」堆)
#   lower_bound / upper_bound   bisect.bisect_left / bisect_right
#   next_permutation            itertools.permutations
#   __gcd / lcm                 math.gcd / math.lcm
#   accumulate(前綴和)         itertools.accumulate
# =====================================================================


# %% 1. Counter —— 計數神器
from collections import Counter

c = Counter("mississippi")
print(c)                    # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
print(c["s"])               # 4
print(c["z"])               # 0  ← 不存在不會報錯
print(c.most_common(2))     # 前兩名

# 判斷兩個字串是不是重組字(anagram)
print(Counter("listen") == Counter("silent"))


# %% 2. defaultdict —— 不存在的 key 自動建預設值
from collections import defaultdict

# 建鄰接串列(圖)
graph = defaultdict(list)       # 不存在的 key 自動給 []
edges = [(1, 2), (1, 3), (2, 4)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
print(dict(graph))


# %% 3. deque —— 雙向佇列,BFS 必備
from collections import deque

# ⚠ 不要用 list.pop(0) 當佇列,那是 O(n)
q = deque([1])
dist = {1: 0}
while q:                        # 非空就繼續
    u = q.popleft()             # O(1)
    for v in graph[u]:
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
print("BFS dist:", dist)


# %% 4. heapq —— 優先佇列
import heapq

# ⚠ Python 的 heap 是「最小堆」,C++ priority_queue 預設是「最大堆」
h = []
for x in [5, 1, 8, 3]:
    heapq.heappush(h, x)
print(heapq.heappop(h))         # 1(最小的)

# 要最大堆:存負數
h = []
for x in [5, 1, 8, 3]:
    heapq.heappush(h, -x)
print(-heapq.heappop(h))        # 8

# 存 tuple:先比第一個,一樣再比第二個(Dijkstra 用)
h = [(3, "c"), (1, "a"), (2, "b")]
heapq.heapify(h)                # 把現成串列變成 heap,O(n)
print(heapq.heappop(h))

print(heapq.nsmallest(2, [5, 1, 8, 3]))     # 前 k 小


# %% 5. bisect —— 二分搜尋
import bisect

a = [1, 3, 3, 3, 7, 9]          # ⚠ 必須已排序
print(bisect.bisect_left(a, 3))     # 1  第一個 >= 3 的位置(lower_bound)
print(bisect.bisect_right(a, 3))    # 4  第一個 >  3 的位置(upper_bound)
print(bisect.bisect_right(a, 3) - bisect.bisect_left(a, 3))   # 3 出現幾次

bisect.insort(a, 5)             # 插入並維持排序(O(n))
print(a)


# %% 6. itertools —— 排列、組合、前綴和
from itertools import permutations, combinations, product, accumulate

print(list(permutations([1, 2, 3])))        # 全排列(3! = 6 種)
print(list(combinations([1, 2, 3, 4], 2)))  # C(4,2) = 6 種
print(list(product([0, 1], repeat=3)))      # 3 位元的所有 0/1 組合

pre = list(accumulate([3, 1, 4, 1, 5], initial=0))
print(pre)                      # [0, 3, 4, 8, 9, 14]  前綴和
l, r = 1, 3                     # 區間 [1, 3] 的和
print(pre[r + 1] - pre[l])      # 1 + 4 + 1 = 6


# %% 7. math
import math

print(math.gcd(12, 18), math.lcm(4, 6))
print(math.comb(10, 3), math.perm(10, 3))   # C(10,3) P(10,3)
print(math.isqrt(10**18 + 5))   # 整數平方根,精確,不會有浮點誤差
print(math.inf, -math.inf)      # 無限大,當初始值用

# 模反元素:pow 第三個參數 = 取模
MOD = 10**9 + 7
print(pow(2, 10**18, MOD))      # 快速冪,內建
print(pow(3, -1, MOD))          # 3 的模反元素(Python 3.8+)


# %% 8. CP 用的快速輸入
# input() 在大量資料時很慢。CP 標準寫法:
#
#   import sys
#   input = sys.stdin.readline              # 換掉 input,快很多
#   n = int(input())
#
#   或一次讀完全部:
#   data = sys.stdin.buffer.read().split()
#
# 輸出很多行時:先收進 list,最後 print("\n".join(map(str, ans)))
ans = [1, 2, 3]
print("\n".join(map(str, ans)))


# =====================================================================
# 練習
#   1. 用 Counter 找出串列裡出現次數 >= 2 的所有元素
#   2. 用 heapq 寫 Dijkstra(圖自己編一個 5 個點的)
#   3. 用 bisect 算:排序後的陣列裡,有幾個數落在 [L, R]
# =====================================================================
# %% 練習區
