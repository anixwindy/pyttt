import sys
import os
from collections import Counter, defaultdict, deque
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from itertools import accumulate, combinations, permutations
from math import gcd, inf, isqrt

try:
    _HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _HERE = os.getcwd()
_IN = os.path.join(_HERE, "in.txt")
LOCAL = os.path.exists(_IN)
if LOCAL:
    sys.stdin = open(_IN, encoding="utf-8")

input = sys.stdin.readline

def ii(): return int(input())
def mi(): return map(int, input().split())
def li(): return list(map(int, input().split()))
def si(): return input().strip()

def dbg(*x):
    if LOCAL:
        print(*x, file=sys.stderr)

MOD = 10**9 + 7


def solve():


    pass

T = 1
# T = ii()
for _ in range(T):
    solve()
