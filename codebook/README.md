# codebook —— Python 模板庫

> **這裡刻意從空的開始。** C++ 那邊有 23 支(`D:\2D_RIEE\codebook\`),Python 不照搬。
> **規則:某一題真的需要、而且 AC 了,才把那段抽出來放進來。**
> 理由:「擴充 codebook 但沒在解題」= 頭號死因(見 `CLAUDE.md` 紅色警報)。

---

## §0 目前有什麼

| 資料夾 | 檔案 | 等級 | 一句話 | 驗證 |
|---|---|---|---|---|
| (空) | | | | |

資料夾照 C++ 那邊的編號開:`01_basic` `02_ds` `03_graph` `04_dp` `05_string` `06_math`,**要放第一支時才建**。
格式看 `_FORMAT.md`。

---

## §1 ★ C++ STL → Python 對照(800 分夠用的部分)

> 800 題大部分**不需要 codebook**,需要的是「C++ 那個東西,Python 叫什麼」。

| C++ | Python | ⚠ 坑 |
|---|---|---|
| `vector<int> a(n)` | `a = [0] * n` | |
| `vector<vector<int>> g(n, vector<int>(m))` | `g = [[0] * m for _ in range(n)]` | ★ **不要寫 `[[0] * m] * n`** —— n 列會是同一個 list,改一格全部跟著變 |
| `sort(all(a))` | `a.sort()` | `sorted(a)` 會回傳新的,`a.sort()` 回傳 `None` |
| `sort` 由大到小 | `a.sort(reverse=True)` | |
| 自訂排序 | `a.sort(key=lambda p: (p[1], -p[0]))` | 沒有 `cmp`,用 `key` 回傳 tuple |
| `map<int,int> cnt; cnt[x]++` | `cnt = Counter(a)` 或 `defaultdict(int)` | 普通 `dict` 讀不存在的 key 會噴 `KeyError` |
| `map` 依 key 排序走訪 | `for k in sorted(cnt):` | Python 的 dict **不會自動排序**(只記插入順序) |
| `set<int>` 有序 | ⚠ **沒有內建** | 只要「有沒有出現過」用 `set()`;要排序/找前後一個 → 先跟我說 |
| `lower_bound` / `upper_bound` | `bisect_left(a, x)` / `bisect_right(a, x)` | a 必須先排好序 |
| `priority_queue<int>`(大的先出) | `heappush(h, -x)`,`-heappop(h)` | ★ Python 的 heap **只有小的先出**,要大的先出就存負數 |
| `queue` / `deque` | `deque()`,`popleft()` / `append()` | ⛔ 不要用 `list.pop(0)`,那是 O(n) |
| `pair<int,int>` | `(a, b)` tuple | tuple 比大小 = 先比第一個再比第二個,跟 pair 一樣 |
| `long long` | `int` | ★ **Python 的 int 不會溢位**。C++ 要 ll 的地方這裡不用管 |
| `a / b`(整數除法) | `a // b` | ★ `/` 會變小數。負數:C++ 往 0 取,Python 往下取(`-7 // 2 == -4`) |
| `a % b` 負數 | `a % b` | Python 的結果永遠跟 b 同號(`-7 % 3 == 2`),C++ 是 `-1` |
| `__gcd(a, b)` | `gcd(a, b)` | |
| `sqrt` 取整 | `isqrt(n)` | ⛔ 不要 `int(n ** 0.5)`,大數會差 1 |
| 前綴和 | `pre = [0] + list(accumulate(a))` | `pre[r+1] - pre[l]` = `a[l..r]` 的和 |
| `string s; s[i] = 'x'` | `s = list(s)`,改完 `''.join(s)` | ★ Python 的字串**不能改**,要先轉 list |
| 遞迴 DFS | 改成用 stack 的迴圈 | Python 遞迴預設只有 1000 層,深一點就 RE |

更完整的 stdlib 範例:`learn/06_stdlib_for_cp.py`。

---

## §2 ★ 規則:沒驗證過的模板不准信(跟 C++ 那邊同一條)

| 狀態 | 意思 |
|---|---|
| `[  ]` | 寫好、跑過示範,但**還沒用它 AC 過任何一題** |
| `[OK] 2026-10-20 CF1234D` | **用它 AC 過了,這時候才能信它** |
