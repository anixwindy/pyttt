# ══ Python CP 模板 —— 永遠不動,每題全選複製到 solve.py ══════════
#  交 CF 時語言選 ★ PyPy 3(64bit)★ —— 比 CPython 快 5~10 倍
#  ⚠ CF 的 PyPy 是 3.10:不要用 3.12 之後才有的語法
# ═══════════════════════════════════════════════════════════════
import sys
import os
from collections import Counter, defaultdict, deque
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from itertools import accumulate, combinations, permutations
from math import gcd, inf, isqrt

# ── 本機:自動讀 in.txt。CF 上沒有這個檔 → 自動改讀 stdin,交出去不用改 ──
try:
    _HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:                       # # %% 互動視窗沒有 __file__
    _HERE = os.getcwd()
_IN = os.path.join(_HERE, "in.txt")
LOCAL = os.path.exists(_IN)
if LOCAL:
    sys.stdin = open(_IN, encoding="utf-8")

input = sys.stdin.readline              # 比內建 input() 快很多(⚠ 會留 '\n')

# ── 讀入縮寫 ────────────────────────────────────────
def ii(): return int(input())                     # 一個整數
def mi(): return map(int, input().split())        # 一行拆給多個變數:n, k = mi()
def li(): return list(map(int, input().split()))  # 一行整數 → list
def si(): return input().strip()                  # 一個字串(⚠ 一定要 strip)

# ── debug:只在本機印到 stderr,交出去不用刪 ──────────
#    用法:dbg(f"{a=}")  → 印出 a=[1, 2, 3]
def dbg(*x):
    if LOCAL:
        print(*x, file=sys.stderr)

MOD = 10**9 + 7


def solve():

    pass


T = 1
# T = ii()                # ← 多筆測資的題目,把這行打開
for _ in range(T):
    solve()
