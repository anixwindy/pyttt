# ══════════════════════════════════════════════════════════════
#  CF1341B  Nastya and Door              rating 1200    AC 2026-09-10
#  https://codeforces.com/problemset/problem/1341/B
#  tag : prefix-sum        用時 35min        結果 : WA2 -> AC
# ──────────────────────────────────────────────────────────────
#  題目一句話 : 找出所有「峰」,再挑一段長度 k 的區間讓峰最多
#  卡在哪     : ★ 每次重掃區間數峰 O(nk) TLE,卡 15 分才想到峰的位置是固定的
#  關鍵想法   : 先算 0/1「是不是峰」陣列 -> 前綴和 -> 每個區間 O(1)
#  線索       : ★★「所有長度 k 的區間 + 數區間內某物數量」= 前綴和 / 滑動視窗
#  codebook   : (沒用到)
#  犯的錯     : 峰要「嚴格大於」寫成 >= ; 端點不算峰忘了排除
# ══════════════════════════════════════════════════════════════
# ⚠ 這份是「檔頭該寫什麼」的範例。檔頭以下就是 AC 那天的 solve.py 原樣貼上
#   (範例為了短,把模板的 import / 縮寫砍到只剩用到的)
import sys

input = sys.stdin.readline


def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    # peak[i] = 1 代表 a[i] 是峰(端點 0 和 n-1 不可能是峰)
    peak = [0] * n
    for i in range(1, n - 1):
        if a[i - 1] < a[i] > a[i + 1]:      # 嚴格大於兩邊
            peak[i] = 1

    # pre[i] = peak[0] + ... + peak[i-1]
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + peak[i]

    best, best_l = -1, 0
    for l in range(n - k + 1):              # 區間 [l, l+k-1],峰只算內部 l+1 .. l+k-2
        cnt = pre[l + k - 1] - pre[l + 1]
        if cnt > best:                      # 用 > 不用 >= → 同分時保留最左邊的 l
            best, best_l = cnt, l
    print(best + 1, best_l + 1)             # 題目要「分成幾塊」= 峰數 + 1;l 轉 1-indexed


T = int(input())
for _ in range(T):
    solve()
