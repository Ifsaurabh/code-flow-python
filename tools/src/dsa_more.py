from qlib import add
S = 'Data Structures & Algorithms'
NC = 'NeetCode 150 style'; B75 = 'Blind 75 style'; T150 = 'Top Interview 150 style'

# ---------------- Linked List (lists are converted to nodes for you)
H = 'Linked List'
LL = dict(prelude='ds', conv=['ll'], conv_ret='ll')
add('ll-reverse', 'Reverse a linked list', S, H, 'Pointer reversal', 1, [NC, B75, T150],
    'Reverse the singly linked list and return the new head. Nodes have .val and .next. (The app turns your test lists into nodes for you.)',
    'reverse_list',
    'def reverse_list(head):\n    prev = None\n    while head:\n        nxt = head.next\n        head.next = prev\n        prev = head\n        head = nxt\n    return prev',
    ([[1, 2, 3, 4, 5]], [5, 4, 3, 2, 1]), [[[1, 2]], [[]], [[7]]], **LL,
    hints=['Remember the next node before you overwrite head.next.'])
add('ll-merge', 'Merge two sorted linked lists', S, H, 'Dummy head + two pointers', 1, [NC, B75, T150],
    'Merge two sorted linked lists into one sorted list and return its head.',
    'merge_two',
    'def merge_two(a, b):\n    dummy = tail = ListNode()\n    while a and b:\n        if a.val <= b.val:\n            tail.next, a = a, a.next\n        else:\n            tail.next, b = b, b.next\n        tail = tail.next\n    tail.next = a or b\n    return dummy.next',
    ([[1, 2, 4], [1, 3, 4]], [1, 1, 2, 3, 4, 4]), [[[], []], [[], [0]], [[5], [1, 2, 6]]], prelude='ds', conv=['ll', 'll'], conv_ret='ll')
add('ll-cycle', 'Remove the nth node from the end', S, H, 'Fast and slow gap', 2, [NC, B75, T150],
    'Remove the n-th node from the end of the list and return the head.',
    'remove_nth_from_end',
    'def remove_nth_from_end(head, n):\n    dummy = ListNode(0, head)\n    fast = slow = dummy\n    for _ in range(n):\n        fast = fast.next\n    while fast.next:\n        fast = fast.next\n        slow = slow.next\n    slow.next = slow.next.next\n    return dummy.next',
    ([[1, 2, 3, 4, 5], 2], [1, 2, 3, 5]), [[[1], 1], [[1, 2], 1], [[1, 2], 2]], prelude='ds', conv=['ll', None], conv_ret='ll')
add('ll-middle', 'Middle of a linked list', S, H, 'Fast and slow pointers', 1, [],
    'Return the value in the middle node. If there are two middles, return the second one.',
    'middle_value',
    'def middle_value(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow.val',
    ([[1, 2, 3, 4, 5]], 3), [[[1, 2, 3, 4, 5, 6]], [[9]], [[1, 2]]], prelude='ds', conv=['ll'])
add('ll-palin', 'Palindrome linked list', S, H, 'Middle + reverse second half', 2, [],
    'Return True if the values of the list read the same forwards and backwards. Try O(1) extra space.',
    'is_palindrome_ll',
    'def is_palindrome_ll(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    prev = None\n    while slow:\n        nxt = slow.next\n        slow.next = prev\n        prev = slow\n        slow = nxt\n    a, b = head, prev\n    while b:\n        if a.val != b.val:\n            return False\n        a, b = a.next, b.next\n    return True',
    ([[1, 2, 2, 1]], True), [[[1, 2]], [[1]], [[1, 2, 3, 2, 1]]], prelude='ds', conv=['ll'])

# ---------------- Trees (level-order lists are converted to nodes)
H = 'Trees'
TR = dict(prelude='ds', conv=['tree'])
add('tr-depth', 'Maximum depth of a binary tree', S, H, 'DFS recursion', 1, [NC, B75, T150],
    'Return how many nodes are on the longest path from the root down to a leaf. Nodes have .val, .left, .right. Tests give the tree as a level-order list with None for gaps.',
    'max_depth',
    'def max_depth(root):\n    if root is None:\n        return 0\n    return 1 + max(max_depth(root.left), max_depth(root.right))',
    ([[3, 9, 20, None, None, 15, 7]], 3), [[[]], [[1, None, 2]], [[1, 2, 3, 4]]], **TR,
    hints=['The depth of a tree is 1 + the deeper of its two subtrees.'])
add('tr-invert', 'Invert a binary tree', S, H, 'DFS recursion', 1, [NC, B75],
    'Swap the left and right child of every node. Return the root.',
    'invert_tree',
    'def invert_tree(root):\n    if root:\n        root.left, root.right = invert_tree(root.right), invert_tree(root.left)\n    return root',
    ([[4, 2, 7, 1, 3, 6, 9]], [4, 7, 2, 9, 6, 3, 1]), [[[2, 1, 3]], [[]], [[1, 2]]], prelude='ds', conv=['tree'], conv_ret='tree')
add('tr-same', 'Same tree', S, H, 'Parallel DFS', 1, [NC, B75],
    'Return True if the two trees have the same shape and the same values.',
    'is_same_tree',
    'def is_same_tree(p, q):\n    if p is None and q is None:\n        return True\n    if p is None or q is None or p.val != q.val:\n        return False\n    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)',
    ([[1, 2, 3], [1, 2, 3]], True), [[[1, 2], [1, None, 2]], [[1, 2, 1], [1, 1, 2]], [[], []]], prelude='ds', conv=['tree', 'tree'])
add('tr-level', 'Level order traversal', S, H, 'BFS with a queue', 2, [NC, B75, T150],
    'Return the values level by level, left to right, as a list of lists.',
    'level_order',
    'def level_order(root):\n    from collections import deque\n    if root is None:\n        return []\n    out, q = [], deque([root])\n    while q:\n        level = []\n        for _ in range(len(q)):\n            node = q.popleft()\n            level.append(node.val)\n            if node.left:\n                q.append(node.left)\n            if node.right:\n                q.append(node.right)\n        out.append(level)\n    return out',
    ([[3, 9, 20, None, None, 15, 7]], [[3], [9, 20], [15, 7]]), [[[1]], [[]], [[1, 2, 3, 4, 5]]], **TR,
    hints=['Process exactly len(queue) nodes per round: that is one level.'])
add('tr-bst', 'Validate a binary search tree', S, H, 'DFS with allowed range', 2, [NC, B75, T150],
    'Return True if every node is greater than everything in its left subtree and smaller than everything in its right subtree.',
    'is_valid_bst',
    'def is_valid_bst(root):\n    def ok(node, lo, hi):\n        if node is None:\n            return True\n        if not (lo < node.val < hi):\n            return False\n        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)\n    return ok(root, float("-inf"), float("inf"))',
    ([[2, 1, 3]], True), [[[5, 1, 4, None, None, 3, 6]], [[]], [[5, 4, 6, None, None, 3, 7]], [[1, 1]]], **TR)
add('tr-lca', 'Lowest common ancestor of a BST', S, H, 'BST walk', 2, [NC, B75, T150],
    'In a binary search tree, return the value of the lowest node that has both p and q (both exist) as descendants (a node counts as its own descendant).',
    'lca_bst',
    'def lca_bst(root, p, q):\n    node = root\n    while node:\n        if p < node.val and q < node.val:\n            node = node.left\n        elif p > node.val and q > node.val:\n            node = node.right\n        else:\n            return node.val',
    ([[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8], 6), [[[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4], [[2, 1], 2, 1]], prelude='ds', conv=['tree', None, None])
add('tr-diam', 'Diameter of a binary tree', S, H, 'DFS returning height', 2, [NC, B75],
    'Return the length (in edges) of the longest path between any two nodes.',
    'diameter',
    'def diameter(root):\n    best = 0\n    def height(node):\n        nonlocal best\n        if node is None:\n            return 0\n        l, r = height(node.left), height(node.right)\n        best = max(best, l + r)\n        return 1 + max(l, r)\n    height(root)\n    return best',
    ([[1, 2, 3, 4, 5]], 3), [[[1, 2]], [[1]], [[]]], **TR)
add('tr-sym', 'Symmetric tree', S, H, 'Mirror DFS', 1, [],
    'Return True if the tree is a mirror image of itself.',
    'is_symmetric',
    'def is_symmetric(root):\n    def mirror(a, b):\n        if a is None and b is None:\n            return True\n        if a is None or b is None or a.val != b.val:\n            return False\n        return mirror(a.left, b.right) and mirror(a.right, b.left)\n    return root is None or mirror(root.left, root.right)',
    ([[1, 2, 2, 3, 4, 4, 3]], True), [[[1, 2, 2, None, 3, None, 3]], [[1]], [[]]], **TR)
add('tr-pathsum', 'Path sum', S, H, 'DFS carrying remaining sum', 1, [T150],
    'Return True if some root-to-leaf path adds up to target.',
    'has_path_sum',
    'def has_path_sum(root, target):\n    if root is None:\n        return False\n    if root.left is None and root.right is None:\n        return root.val == target\n    return has_path_sum(root.left, target - root.val) or has_path_sum(root.right, target - root.val)',
    ([[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22], True), [[[1, 2, 3], 5], [[1, 2], 0], [[], 0]], prelude='ds', conv=['tree', None])

# ---------------- Backtracking
H = 'Backtracking'
add('bt-subsets', 'Subsets', S, H, 'Include / skip decision tree', 2, [NC, B75],
    'nums has distinct numbers. Return all possible subsets (the power set). Any order.',
    'subsets',
    'def subsets(nums):\n    out = []\n    def go(i, cur):\n        if i == len(nums):\n            out.append(cur[:])\n            return\n        cur.append(nums[i])\n        go(i + 1, cur)\n        cur.pop()\n        go(i + 1, cur)\n    go(0, [])\n    return out',
    ([[1, 2, 3]], [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]), [[[0]], [[]], [[5, 6]]], compare='nested_unordered')
add('bt-perm', 'Permutations', S, H, 'Choose unused element', 2, [NC, B75],
    'Return every ordering of the distinct numbers in nums. Any order.',
    'permutations',
    'def permutations(nums):\n    out = []\n    def go(cur, used):\n        if len(cur) == len(nums):\n            out.append(cur[:])\n            return\n        for i, n in enumerate(nums):\n            if not used[i]:\n                used[i] = True\n                cur.append(n)\n                go(cur, used)\n                cur.pop()\n                used[i] = False\n    go([], [False] * len(nums))\n    return out',
    ([[1, 2, 3]], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), [[[0, 1]], [[1]], [[1, 2, 3, 4]]], compare='unordered')
add('bt-combsum', 'Combination sum', S, H, 'Backtrack with start index', 2, [NC, B75],
    'Using the distinct positive numbers in candidates (each may be reused any number of times), return all unique combinations that add up to target. Each combination in increasing order. Any order of combinations.',
    'combination_sum',
    'def combination_sum(candidates, target):\n    candidates = sorted(candidates)\n    out = []\n    def go(start, cur, left):\n        if left == 0:\n            out.append(cur[:])\n            return\n        for i in range(start, len(candidates)):\n            if candidates[i] > left:\n                break\n            cur.append(candidates[i])\n            go(i, cur, left - candidates[i])\n            cur.pop()\n    go(0, [], target)\n    return out',
    ([[2, 3, 6, 7], 7], [[2, 2, 3], [7]]), [[[2, 3, 5], 8], [[2], 1], [[1], 3]], compare='nested_unordered')
add('bt-parens', 'Generate parentheses', S, H, 'Backtrack with open/close counts', 2, [NC, B75],
    'Return all well-formed strings made of n pairs of parentheses. Any order.',
    'generate_parentheses',
    'def generate_parentheses(n):\n    out = []\n    def go(cur, op, cl):\n        if len(cur) == 2 * n:\n            out.append(cur)\n            return\n        if op < n:\n            go(cur + "(", op + 1, cl)\n        if cl < op:\n            go(cur + ")", op, cl + 1)\n    go("", 0, 0)\n    return out',
    ([3], ['((()))', '(()())', '(())()', '()(())', '()()()']), [[1], [2], [4]], compare='unordered')
add('bt-letters', 'Letter combinations of a phone number', S, H, 'Product of choices', 2, [NC, B75],
    'Digits 2-9 map to letters like a phone keypad (2=abc, 3=def, 4=ghi, 5=jkl, 6=mno, 7=pqrs, 8=tuv, 9=wxyz). Return every letter combination. Any order.',
    'letter_combinations',
    'def letter_combinations(digits):\n    if not digits:\n        return []\n    m = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}\n    out = [""]\n    for d in digits:\n        out = [p + c for p in out for c in m[d]]\n    return out',
    (['23'], ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']), [[''], ['7'], ['79']], compare='unordered')
add('bt-palinpart', 'Palindrome partitioning', S, H, 'Backtrack on cut points', 2, [NC],
    'Cut s into pieces so that every piece is a palindrome. Return all ways. Any order.',
    'partition',
    'def partition(s):\n    out = []\n    def go(i, cur):\n        if i == len(s):\n            out.append(cur[:])\n            return\n        for j in range(i + 1, len(s) + 1):\n            piece = s[i:j]\n            if piece == piece[::-1]:\n                cur.append(piece)\n                go(j, cur)\n                cur.pop()\n    go(0, [])\n    return out',
    (['aab'], [['a', 'a', 'b'], ['aa', 'b']]), [['a'], ['aba'], ['abc']], compare='nested_unordered')
add('bt-wordsearch', 'Word search', S, H, 'Grid DFS with visited', 2, [NC, B75],
    'Return True if word can be spelled by walking up/down/left/right through adjacent cells of the grid without reusing a cell.',
    'exist',
    'def exist(board, word):\n    rows, cols = len(board), len(board[0])\n    def go(r, c, i):\n        if i == len(word):\n            return True\n        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:\n            return False\n        keep = board[r][c]\n        board[r][c] = "#"\n        found = go(r + 1, c, i + 1) or go(r - 1, c, i + 1) or go(r, c + 1, i + 1) or go(r, c - 1, i + 1)\n        board[r][c] = keep\n        return found\n    return any(go(r, c, 0) for r in range(rows) for c in range(cols))',
    ([[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"], True), [[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"], [[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"], [[["A"]], "A"]])
add('bt-nqueens', 'N-Queens (count the solutions)', S, H, 'Backtrack with column/diagonal sets', 3, [NC],
    'Place n queens on an n x n board so none attack each other. Return how many different placements exist.',
    'total_n_queens',
    'def total_n_queens(n):\n    cols, d1, d2 = set(), set(), set()\n    def go(r):\n        if r == n:\n            return 1\n        total = 0\n        for c in range(n):\n            if c in cols or r - c in d1 or r + c in d2:\n                continue\n            cols.add(c); d1.add(r - c); d2.add(r + c)\n            total += go(r + 1)\n            cols.remove(c); d1.remove(r - c); d2.remove(r + c)\n        return total\n    return go(0)',
    ([4], 2), [[1], [5], [6], [2]])

# ---------------- 1-D DP
H = '1-D Dynamic Programming'
add('dp-stairs', 'Climbing stairs', S, H, 'Fibonacci-style recurrence', 1, [NC, B75, T150],
    'You climb n steps, 1 or 2 at a time. In how many distinct ways can you reach the top?',
    'climb_stairs',
    'def climb_stairs(n):\n    a, b = 1, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a',
    ([5], 8), [[1], [2], [10], [30]],
    hints=['ways(n) = ways(n-1) + ways(n-2).'])
add('dp-rob', 'House robber', S, H, 'Take or skip', 2, [NC, B75, T150],
    'You cannot rob two neighbouring houses. nums[i] is the money in house i. Return the most you can take.',
    'rob',
    'def rob(nums):\n    take = skip = 0\n    for n in nums:\n        take, skip = skip + n, max(take, skip)\n    return max(take, skip)',
    ([[2, 7, 9, 3, 1]], 12), [[[1, 2, 3, 1]], [[]], [[5]], [[2, 1, 1, 2]]])
add('dp-rob2', 'House robber II (circular)', S, H, 'Two linear runs', 2, [NC, B75],
    'Same as House robber, but the houses form a circle, so the first and last are neighbours.',
    'rob_circle',
    'def rob_circle(nums):\n    def line(a):\n        take = skip = 0\n        for n in a:\n            take, skip = skip + n, max(take, skip)\n        return max(take, skip)\n    if len(nums) == 1:\n        return nums[0]\n    return max(line(nums[1:]), line(nums[:-1]))',
    ([[2, 3, 2]], 3), [[[1, 2, 3, 1]], [[1]], [[1, 2]], [[5, 1, 1, 5]]])
add('dp-coin', 'Coin change (fewest coins)', S, H, 'Bottom-up table', 2, [NC, B75, T150],
    'Return the fewest coins from coins (unlimited supply) that add up to amount, or -1 if impossible.',
    'coin_change',
    'def coin_change(coins, amount):\n    INF = amount + 1\n    dp = [0] + [INF] * amount\n    for a in range(1, amount + 1):\n        for c in coins:\n            if c <= a:\n                dp[a] = min(dp[a], dp[a - c] + 1)\n    return -1 if dp[amount] >= INF else dp[amount]',
    ([[1, 2, 5], 11], 3), [[[2], 3], [[1], 0], [[186, 419, 83, 408], 6249], [[2, 5, 10, 1], 27]],
    hints=['dp[a] = best way to make amount a. Try every last coin.'])
add('dp-lis', 'Longest increasing subsequence', S, H, 'DP / patience sorting', 2, [NC, B75],
    'Return the length of the longest strictly increasing subsequence (not necessarily contiguous).',
    'length_of_lis',
    'def length_of_lis(nums):\n    import bisect\n    tails = []\n    for n in nums:\n        i = bisect.bisect_left(tails, n)\n        if i == len(tails):\n            tails.append(n)\n        else:\n            tails[i] = n\n    return len(tails)',
    ([[10, 9, 2, 5, 3, 7, 101, 18]], 4), [[[0, 1, 0, 3, 2, 3]], [[7, 7, 7]], [[]], [[1, 3, 6, 7, 9, 4, 10, 5, 6]]])
add('dp-wordbreak', 'Word break', S, H, 'Prefix DP', 2, [NC, B75],
    'Return True if s can be cut into a sequence of words that all appear in the list words (reuse allowed).',
    'word_break',
    'def word_break(s, words):\n    ws = set(words)\n    dp = [True] + [False] * len(s)\n    for i in range(1, len(s) + 1):\n        for j in range(i):\n            if dp[j] and s[j:i] in ws:\n                dp[i] = True\n                break\n    return dp[-1]',
    (['leetcode', ['leet', 'code']], True), [['applepenapple', ['apple', 'pen']], ['catsandog', ['cats', 'dog', 'sand', 'and', 'cat']], ['', ['a']]])
add('dp-decode', 'Decode ways', S, H, 'One or two digits', 2, [NC, B75],
    'A=1, B=2 ... Z=26. A digit string can be decoded into letters in several ways. Return how many.',
    'num_decodings',
    'def num_decodings(s):\n    if not s or s[0] == "0":\n        return 0\n    a, b = 1, 1\n    for i in range(1, len(s)):\n        c = 0\n        if s[i] != "0":\n            c += b\n        if 10 <= int(s[i - 1:i + 1]) <= 26:\n            c += a\n        a, b = b, c\n    return b',
    (['226'], 3), [['12'], ['06'], ['10'], ['2101'], ['11106']])
add('dp-pal', 'Longest palindromic substring', S, H, 'Expand around centre', 2, [NC, B75],
    'Return the longest substring of s that is a palindrome. If several tie, return the one that starts first.',
    'longest_palindrome',
    'def longest_palindrome(s):\n    best = ""\n    for c in range(len(s)):\n        for lo, hi in ((c, c), (c, c + 1)):\n            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:\n                lo -= 1\n                hi += 1\n            if hi - lo - 1 > len(best):\n                best = s[lo + 1:hi]\n    return best',
    (['babad'], 'bab'), [['cbbd'], ['a'], ['forgeeksskeegfor'], ['abc']])
add('dp-maxprod', 'Maximum product subarray', S, H, 'Track max and min', 2, [NC, B75],
    'Return the largest product of a contiguous, non-empty piece of nums.',
    'max_product',
    'def max_product(nums):\n    hi = lo = best = nums[0]\n    for n in nums[1:]:\n        cands = (n, hi * n, lo * n)\n        hi, lo = max(cands), min(cands)\n        best = max(best, hi)\n    return best',
    ([[2, 3, -2, 4]], 6), [[[-2, 0, -1]], [[-2, 3, -4]], [[-3]], [[0, 2]]])
add('dp-partition', 'Partition equal subset sum', S, H, 'Subset-sum set', 2, [NC, B75],
    'Return True if nums can be split into two groups with equal sums.',
    'can_partition',
    'def can_partition(nums):\n    total = sum(nums)\n    if total % 2:\n        return False\n    half = total // 2\n    reach = {0}\n    for n in nums:\n        reach |= {r + n for r in reach if r + n <= half}\n    return half in reach',
    ([[1, 5, 11, 5]], True), [[[1, 2, 3, 5]], [[2, 2]], [[1]], [[100, 100, 100, 100, 99, 101]]])

H = '2-D Dynamic Programming'
add('dp2-paths', 'Unique paths', S, H, 'Grid DP', 2, [NC, B75],
    'A robot starts top-left of an m x n grid and can only move right or down. How many different paths reach the bottom-right?',
    'unique_paths',
    'def unique_paths(m, n):\n    row = [1] * n\n    for _ in range(1, m):\n        for j in range(1, n):\n            row[j] += row[j - 1]\n    return row[-1]',
    ([3, 7], 28), [[3, 2], [1, 1], [7, 3], [10, 10]])
add('dp2-lcs', 'Longest common subsequence', S, H, 'Two-string table', 2, [NC],
    'Return the length of the longest subsequence that appears in both a and b.',
    'lcs',
    'def lcs(a, b):\n    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]\n    for i in range(1, len(a) + 1):\n        for j in range(1, len(b) + 1):\n            if a[i - 1] == b[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1] + 1\n            else:\n                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n    return dp[-1][-1]',
    (['abcde', 'ace'], 3), [['abc', 'abc'], ['abc', 'def'], ['', 'a'], ['AGGTAB', 'GXTXAYB']])
add('dp2-edit', 'Edit distance', S, H, 'Two-string table', 3, [NC, T150],
    'Minimum number of insert, delete or replace operations to turn word1 into word2.',
    'min_distance',
    'def min_distance(w1, w2):\n    m, n = len(w1), len(w2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1):\n        dp[i][0] = i\n    for j in range(n + 1):\n        dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if w1[i - 1] == w2[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1]\n            else:\n                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n    return dp[m][n]',
    (['horse', 'ros'], 3), [['intention', 'execution'], ['', 'abc'], ['same', 'same'], ['kitten', 'sitting']])
add('dp2-knap', '0/1 knapsack', S, H, 'Capacity table', 2, [],
    'Each item has a weight and a value and may be used at most once. Return the largest total value that fits in capacity.',
    'knapsack',
    'def knapsack(weights, values, capacity):\n    dp = [0] * (capacity + 1)\n    for w, v in zip(weights, values):\n        for c in range(capacity, w - 1, -1):\n            dp[c] = max(dp[c], dp[c - w] + v)\n    return dp[capacity]',
    ([[1, 3, 4, 5], [1, 4, 5, 7], 7], 9), [[[10, 20, 30], [60, 100, 120], 50], [[5], [10], 4], [[2, 3, 4], [3, 4, 5], 5]])
add('dp2-coin2', 'Coin change (count the ways)', S, H, 'Unbounded knapsack', 2, [NC],
    'Return how many different combinations of coins (unlimited supply) add up to amount. Order does not matter.',
    'change_ways',
    'def change_ways(amount, coins):\n    dp = [1] + [0] * amount\n    for c in coins:\n        for a in range(c, amount + 1):\n            dp[a] += dp[a - c]\n    return dp[amount]',
    ([5, [1, 2, 5]], 4), [[3, [2]], [10, [10]], [0, [7]], [11, [1, 5, 10]]])
add('dp2-minpath', 'Minimum path sum', S, H, 'Grid DP', 2, [],
    'Move only right or down from top-left to bottom-right of a grid of costs. Return the smallest total cost of a path.',
    'min_path_sum',
    'def min_path_sum(grid):\n    r, c = len(grid), len(grid[0])\n    dp = [[0] * c for _ in range(r)]\n    for i in range(r):\n        for j in range(c):\n            best = 0\n            if i and j:\n                best = min(dp[i - 1][j], dp[i][j - 1])\n            elif i:\n                best = dp[i - 1][j]\n            elif j:\n                best = dp[i][j - 1]\n            dp[i][j] = grid[i][j] + best\n    return dp[-1][-1]',
    ([[[1, 3, 1], [1, 5, 1], [4, 2, 1]]], 7), [[[[1, 2, 3], [4, 5, 6]]], [[[5]]], [[[1, 2], [1, 1]]]])

# ---------------- Greedy
H = 'Greedy'
add('gr-kadane', 'Maximum subarray', S, H, "Kadane's algorithm", 2, [NC, B75, T150],
    'Return the largest sum of a contiguous, non-empty piece of nums.',
    'max_subarray',
    'def max_subarray(nums):\n    cur = best = nums[0]\n    for n in nums[1:]:\n        cur = max(n, cur + n)\n        best = max(best, cur)\n    return best',
    ([[-2, 1, -3, 4, -1, 2, 1, -5, 4]], 6), [[[1]], [[5, 4, -1, 7, 8]], [[-3, -2, -5]]],
    hints=['At each number: extend the running piece, or start fresh here.'])
add('gr-jump', 'Jump game', S, H, 'Furthest reach', 2, [NC, B75, T150],
    'nums[i] is the furthest you can jump from i. Starting at index 0, can you reach the last index?',
    'can_jump',
    'def can_jump(nums):\n    reach = 0\n    for i, n in enumerate(nums):\n        if i > reach:\n            return False\n        reach = max(reach, i + n)\n    return True',
    ([[2, 3, 1, 1, 4]], True), [[[3, 2, 1, 0, 4]], [[0]], [[2, 0, 0]], [[1, 0, 1]]])
add('gr-jump2', 'Jump game II', S, H, 'BFS-by-levels greedy', 2, [NC, T150],
    'Same jumps, and you can always reach the end. Return the minimum number of jumps.',
    'jump',
    'def jump(nums):\n    jumps = end = far = 0\n    for i in range(len(nums) - 1):\n        far = max(far, i + nums[i])\n        if i == end:\n            jumps += 1\n            end = far\n    return jumps',
    ([[2, 3, 1, 1, 4]], 2), [[[2, 3, 0, 1, 4]], [[1]], [[1, 1, 1, 1]]])
add('gr-gas', 'Gas station', S, H, 'Running tank reset', 2, [NC, T150],
    'Stations are on a circle. gas[i] is the fuel you get at i, cost[i] is the fuel to drive to the next. Return the index to start from to complete the circuit, or -1. The answer is unique if it exists.',
    'can_complete_circuit',
    'def can_complete_circuit(gas, cost):\n    if sum(gas) < sum(cost):\n        return -1\n    tank = start = 0\n    for i in range(len(gas)):\n        tank += gas[i] - cost[i]\n        if tank < 0:\n            tank = 0\n            start = i + 1\n    return start',
    ([[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], 3), [[[2, 3, 4], [3, 4, 3]], [[5], [4]], [[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]]])
add('gr-partlabels', 'Partition labels', S, H, 'Last occurrence', 2, [NC],
    'Cut s into as many pieces as possible so that each letter appears in at most one piece. Return the piece sizes.',
    'partition_labels',
    'def partition_labels(s):\n    last = {c: i for i, c in enumerate(s)}\n    out = []\n    start = end = 0\n    for i, c in enumerate(s):\n        end = max(end, last[c])\n        if i == end:\n            out.append(end - start + 1)\n            start = i + 1\n    return out',
    (['ababcbacadefegdehijhklij'], [9, 7, 8]), [['eccbbbbdec'], ['a'], ['abc']])

# ---------------- Intervals
H = 'Intervals'
add('iv-merge', 'Merge intervals', S, H, 'Sort by start', 2, [NC, B75, T150],
    'Merge all overlapping [start, end] intervals. Return the merged list sorted by start.',
    'merge',
    'def merge(intervals):\n    out = []\n    for s, e in sorted(intervals):\n        if out and s <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], e)\n        else:\n            out.append([s, e])\n    return out',
    ([[[1, 3], [2, 6], [8, 10], [15, 18]]], [[1, 6], [8, 10], [15, 18]]), [[[[1, 4], [4, 5]]], [[[1, 4], [0, 4]]], [[[1, 10], [2, 3], [4, 5]]]])
add('iv-insert', 'Insert interval', S, H, 'Before / overlap / after', 2, [NC, B75, T150],
    'intervals is sorted and non-overlapping. Insert new_interval, merging if needed, and return the result.',
    'insert',
    'def insert(intervals, new_interval):\n    out = []\n    s, e = new_interval\n    i = 0\n    while i < len(intervals) and intervals[i][1] < s:\n        out.append(intervals[i])\n        i += 1\n    while i < len(intervals) and intervals[i][0] <= e:\n        s = min(s, intervals[i][0])\n        e = max(e, intervals[i][1])\n        i += 1\n    out.append([s, e])\n    out.extend(intervals[i:])\n    return out',
    ([[[1, 3], [6, 9]], [2, 5]], [[1, 5], [6, 9]]), [[[], [5, 7]], [[[1, 5]], [2, 3]], [[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]]])
add('iv-nonover', 'Non-overlapping intervals', S, H, 'Sort by end', 2, [NC, B75],
    'Return the minimum number of intervals to remove so that the rest do not overlap (touching ends is fine).',
    'erase_overlap',
    'def erase_overlap(intervals):\n    removed = 0\n    end = float("-inf")\n    for s, e in sorted(intervals, key=lambda x: x[1]):\n        if s >= end:\n            end = e\n        else:\n            removed += 1\n    return removed',
    ([[[1, 2], [2, 3], [3, 4], [1, 3]]], 1), [[[[1, 2], [1, 2], [1, 2]]], [[[1, 2], [2, 3]]], [[]]])
add('iv-rooms', 'Meeting rooms II', S, H, 'Sweep line', 2, [NC, B75],
    'Given meeting [start, end) times, return the minimum number of rooms needed.',
    'min_meeting_rooms',
    'def min_meeting_rooms(intervals):\n    starts = sorted(s for s, e in intervals)\n    ends = sorted(e for s, e in intervals)\n    rooms = best = j = 0\n    for s in starts:\n        while ends[j] <= s:\n            j += 1\n            rooms -= 1\n        rooms += 1\n        best = max(best, rooms)\n    return best',
    ([[[0, 30], [5, 10], [15, 20]]], 2), [[[[7, 10], [2, 4]]], [[[1, 5], [2, 6], [3, 7]]], [[[1, 2], [2, 3]]]])

# ---------------- Math, bits, matrices
H = 'Math & Bit Manipulation'
add('mb-single', 'Single number', S, H, 'XOR cancels pairs', 1, [NC, B75],
    'Every value in nums appears twice except one. Return the one that appears once, using O(1) extra space.',
    'single_number',
    'def single_number(nums):\n    x = 0\n    for n in nums:\n        x ^= n\n    return x',
    ([[4, 1, 2, 1, 2]], 4), [[[2, 2, 1]], [[1]], [[-1, 5, -1]]])
add('mb-ones', 'Number of 1 bits', S, H, 'Clear the lowest set bit', 1, [NC, B75],
    'Return how many 1 bits are in the binary form of n (n >= 0).',
    'hamming_weight',
    'def hamming_weight(n):\n    count = 0\n    while n:\n        n &= n - 1\n        count += 1\n    return count',
    ([11], 3), [[128], [0], [255], [2147483645]])
add('mb-counting', 'Counting bits', S, H, 'DP on bits', 1, [NC, B75],
    'Return a list where element i is the number of 1 bits in i, for i = 0..n.',
    'count_bits',
    'def count_bits(n):\n    out = [0] * (n + 1)\n    for i in range(1, n + 1):\n        out[i] = out[i >> 1] + (i & 1)\n    return out',
    ([5], [0, 1, 1, 2, 1, 2]), [[0], [2], [10]])
add('mb-pow2', 'Power of two', S, H, 'n & (n-1)', 1, [],
    'Return True if n is a power of two.',
    'is_power_of_two',
    'def is_power_of_two(n):\n    return n > 0 and n & (n - 1) == 0',
    ([16], True), [[1], [3], [0], [-4], [1024]])
add('mb-gcd', 'Greatest common divisor', S, H, "Euclid's algorithm", 1, [],
    'Return the greatest common divisor of a and b without using math.gcd.',
    'my_gcd',
    'def my_gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a',
    ([48, 18], 6), [[7, 13], [0, 5], [100, 25], [270, 192]])
add('mb-primes', 'Count primes below n', S, H, 'Sieve of Eratosthenes', 2, [],
    'Return how many prime numbers are strictly less than n.',
    'count_primes',
    'def count_primes(n):\n    if n < 3:\n        return 0\n    sieve = [True] * n\n    sieve[0] = sieve[1] = False\n    for i in range(2, int(n ** 0.5) + 1):\n        if sieve[i]:\n            for j in range(i * i, n, i):\n                sieve[j] = False\n    return sum(sieve)',
    ([10], 4), [[0], [2], [3], [100], [1000]])
add('mb-pow', 'Pow(x, n)', S, H, 'Fast exponentiation', 2, [NC, T150],
    'Compute x raised to the integer power n (n can be negative) in O(log n) multiplications.',
    'my_pow',
    'def my_pow(x, n):\n    if n < 0:\n        x, n = 1 / x, -n\n    result = 1.0\n    while n:\n        if n & 1:\n            result *= x\n        x *= x\n        n >>= 1\n    return result',
    ([2.0, 10], 1024.0), [[2.0, -2], [3.0, 0], [2.0, 30], [0.5, 3]], compare='float')
add('mb-rotimg', 'Rotate image', S, H, 'Transpose then reverse rows', 2, [NC, B75, T150],
    'Rotate the square matrix 90 degrees clockwise, in place.',
    'rotate_matrix',
    'def rotate_matrix(m):\n    n = len(m)\n    for i in range(n):\n        for j in range(i + 1, n):\n            m[i][j], m[j][i] = m[j][i], m[i][j]\n    for row in m:\n        row.reverse()',
    ([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]]), [[[[1]]], [[[1, 2], [3, 4]]], [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]]], inplace=0)
add('mb-spiral', 'Spiral matrix', S, H, 'Shrinking boundaries', 2, [NC, B75, T150],
    'Return all elements of the matrix in clockwise spiral order, starting top-left.',
    'spiral_order',
    'def spiral_order(m):\n    out = []\n    top, bot, left, right = 0, len(m) - 1, 0, len(m[0]) - 1\n    while top <= bot and left <= right:\n        for j in range(left, right + 1):\n            out.append(m[top][j])\n        top += 1\n        for i in range(top, bot + 1):\n            out.append(m[i][right])\n        right -= 1\n        if top <= bot:\n            for j in range(right, left - 1, -1):\n                out.append(m[bot][j])\n            bot -= 1\n        if left <= right:\n            for i in range(bot, top - 1, -1):\n                out.append(m[i][left])\n            left += 1\n    return out',
    ([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [1, 2, 3, 6, 9, 8, 7, 4, 5]), [[[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], [[[1]]], [[[1], [2], [3]]]])
add('mb-zeroes', 'Set matrix zeroes', S, H, 'Mark rows and columns', 2, [NC, B75],
    'If a cell is 0, set its entire row and column to 0. Do it in place.',
    'set_zeroes',
    'def set_zeroes(m):\n    rows = {i for i, r in enumerate(m) if 0 in r}\n    cols = {j for r in m for j, v in enumerate(r) if v == 0}\n    for i in range(len(m)):\n        for j in range(len(m[0])):\n            if i in rows or j in cols:\n                m[i][j] = 0',
    ([[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]), [[[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]], [[[1]]], [[[1, 2], [3, 4]]]], inplace=0)

# ---------------- Heap / Priority queue
H = 'Heap / Priority Queue'
add('hp-kth', 'Kth largest element', S, H, 'Min-heap of size k', 2, [NC, B75],
    'Return the k-th largest value in nums (counting duplicates). Try a heap of size k.',
    'find_kth_largest',
    'def find_kth_largest(nums, k):\n    import heapq\n    heap = []\n    for n in nums:\n        heapq.heappush(heap, n)\n        if len(heap) > k:\n            heapq.heappop(heap)\n    return heap[0]',
    ([[3, 2, 1, 5, 6, 4], 2], 5), [[[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], [[1], 1], [[7, 7, 7], 3]])
add('hp-stones', 'Last stone weight', S, H, 'Max-heap simulation', 1, [NC],
    'Repeatedly smash the two heaviest stones: equal stones vanish, otherwise the heavier loses the lighter\'s weight. Return the last stone weight, or 0.',
    'last_stone_weight',
    'def last_stone_weight(stones):\n    import heapq\n    h = [-s for s in stones]\n    heapq.heapify(h)\n    while len(h) > 1:\n        a = -heapq.heappop(h)\n        b = -heapq.heappop(h)\n        if a != b:\n            heapq.heappush(h, -(a - b))\n    return -h[0] if h else 0',
    ([[2, 7, 4, 1, 8, 1]], 1), [[[1]], [[2, 2]], [[10, 4, 2, 10]]])
add('hp-kclose', 'K closest points to origin', S, H, 'Heap by distance', 2, [NC, B75],
    'Return the k points closest to (0, 0). The answer is unique; any order.',
    'k_closest',
    'def k_closest(points, k):\n    import heapq\n    return heapq.nsmallest(k, points, key=lambda p: p[0] ** 2 + p[1] ** 2)',
    ([[[1, 3], [-2, 2]], 1], [[-2, 2]]), [[[[3, 3], [5, -1], [-2, 4]], 2], [[[0, 1], [1, 0]], 2]], compare='unordered')
add('hp-sched', 'Task scheduler', S, H, 'Greedy on most frequent task', 2, [NC],
    'Each letter is a task taking 1 unit. The same task needs n idle-or-other units between runs. Return the least total time to finish all tasks.',
    'least_interval',
    'def least_interval(tasks, n):\n    count = {}\n    for t in tasks:\n        count[t] = count.get(t, 0) + 1\n    mx = max(count.values())\n    num_max = sum(1 for v in count.values() if v == mx)\n    return max(len(tasks), (mx - 1) * (n + 1) + num_max)',
    ([['A', 'A', 'A', 'B', 'B', 'B'], 2], 8), [[['A', 'A', 'A', 'B', 'B', 'B'], 0], [['A', 'A', 'A', 'A', 'A', 'A', 'B', 'C', 'D', 'E', 'F', 'G'], 2], [['A'], 5]])
add('hp-median', 'Running median', S, H, 'Two heaps', 3, [NC, B75],
    'Numbers arrive one at a time. After each arrival, report the median so far. Return the list of medians.',
    'running_median',
    'def running_median(stream):\n    import heapq\n    lo, hi = [], []\n    out = []\n    for x in stream:\n        heapq.heappush(lo, -x)\n        heapq.heappush(hi, -heapq.heappop(lo))\n        if len(hi) > len(lo):\n            heapq.heappush(lo, -heapq.heappop(hi))\n        out.append(float(-lo[0]) if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2)\n    return out',
    ([[5, 15, 1, 3]], [5.0, 10.0, 5.0, 4.0]), [[[1]], [[2, 1, 5, 7, 2, 0, 5]], [[3, 3, 3]]], compare='float')

# ---------------- Graphs
H = 'Graphs'
add('gp-islands', 'Number of islands', S, H, 'Grid flood fill (DFS)', 2, [NC, B75, T150],
    'grid has "1" for land and "0" for water. Count the islands (groups of land joined up/down/left/right).',
    'num_islands',
    'def num_islands(grid):\n    if not grid:\n        return 0\n    rows, cols = len(grid), len(grid[0])\n    seen = set()\n    def dfs(r, c):\n        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1" or (r, c) in seen:\n            return\n        seen.add((r, c))\n        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)\n    count = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == "1" and (r, c) not in seen:\n                dfs(r, c)\n                count += 1\n    return count',
    ([[["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]], 3), [[[["1"]]], [[["0"]]], [[["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]]])
add('gp-area', 'Max area of island', S, H, 'Grid DFS returning size', 2, [NC],
    'grid has 1 for land and 0 for water. Return the size of the biggest island.',
    'max_area_of_island',
    'def max_area_of_island(grid):\n    rows, cols = len(grid), len(grid[0])\n    def dfs(r, c):\n        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != 1:\n            return 0\n        grid[r][c] = 2\n        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)\n    return max(dfs(r, c) for r in range(rows) for c in range(cols))',
    ([[[0, 1, 1], [1, 1, 0], [0, 0, 1]]], 4), [[[[0, 0, 0]]], [[[1]]], [[[1, 1, 0, 0], [0, 0, 0, 1], [1, 1, 1, 1]]]])
add('gp-rotten', 'Rotting oranges', S, H, 'Multi-source BFS', 2, [NC, B75],
    'Grid: 0 empty, 1 fresh, 2 rotten. Each minute, fresh oranges next to a rotten one rot. Return the minutes until none is fresh, or -1 if impossible.',
    'oranges_rotting',
    'def oranges_rotting(grid):\n    from collections import deque\n    rows, cols = len(grid), len(grid[0])\n    q = deque()\n    fresh = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == 2:\n                q.append((r, c))\n            elif grid[r][c] == 1:\n                fresh += 1\n    minutes = 0\n    while q and fresh:\n        for _ in range(len(q)):\n            r, c = q.popleft()\n            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:\n                    grid[nr][nc] = 2\n                    fresh -= 1\n                    q.append((nr, nc))\n        minutes += 1\n    return -1 if fresh else minutes',
    ([[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], 4), [[[[2, 1, 1], [0, 1, 1], [1, 0, 1]]], [[[0, 2]]], [[[1]]]])
add('gp-course', 'Course schedule', S, H, 'Topological sort (cycle check)', 2, [NC, B75],
    'There are n courses 0..n-1. prereqs has pairs [a, b] meaning you must take b before a. Return True if all courses can be finished.',
    'can_finish',
    'def can_finish(n, prereqs):\n    from collections import deque\n    graph = [[] for _ in range(n)]\n    indeg = [0] * n\n    for a, b in prereqs:\n        graph[b].append(a)\n        indeg[a] += 1\n    q = deque(i for i in range(n) if indeg[i] == 0)\n    done = 0\n    while q:\n        x = q.popleft()\n        done += 1\n        for y in graph[x]:\n            indeg[y] -= 1\n            if indeg[y] == 0:\n                q.append(y)\n    return done == n',
    ([2, [[1, 0]]], True), [[2, [[1, 0], [0, 1]]], [1, []], [4, [[1, 0], [2, 1], [3, 2]]], [3, [[0, 1], [1, 2], [2, 0]]]])
add('gp-comps', 'Number of connected components', S, H, 'Union-Find', 2, [NC, B75],
    'n nodes (0..n-1) and a list of undirected edges. Return how many connected groups there are.',
    'count_components',
    'def count_components(n, edges):\n    parent = list(range(n))\n    def find(x):\n        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n    comps = n\n    for a, b in edges:\n        ra, rb = find(a), find(b)\n        if ra != rb:\n            parent[ra] = rb\n            comps -= 1\n    return comps',
    ([5, [[0, 1], [1, 2], [3, 4]]], 2), [[5, [[0, 1], [1, 2], [2, 3], [3, 4]]], [3, []], [4, [[0, 1], [2, 3]]]])
add('gp-tree', 'Is it a valid tree?', S, H, 'Union-Find / edge count', 2, [NC, B75],
    'Return True if the n nodes and undirected edges form a single tree (connected and no cycles).',
    'valid_tree',
    'def valid_tree(n, edges):\n    if len(edges) != n - 1:\n        return False\n    parent = list(range(n))\n    def find(x):\n        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n    for a, b in edges:\n        ra, rb = find(a), find(b)\n        if ra == rb:\n            return False\n        parent[ra] = rb\n    return True',
    ([5, [[0, 1], [0, 2], [0, 3], [1, 4]]], True), [[5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]], [1, []], [4, [[0, 1], [2, 3]]]])
add('gp-shortest', 'Shortest path in a grid', S, H, 'BFS', 2, [],
    'grid has 0 for open and 1 for blocked. Move in 4 directions from top-left to bottom-right. Return the number of cells on the shortest path, or -1.',
    'shortest_path',
    'def shortest_path(grid):\n    from collections import deque\n    n, m = len(grid), len(grid[0])\n    if grid[0][0] or grid[n - 1][m - 1]:\n        return -1\n    q = deque([(0, 0, 1)])\n    seen = {(0, 0)}\n    while q:\n        r, c, d = q.popleft()\n        if (r, c) == (n - 1, m - 1):\n            return d\n        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < n and 0 <= nc < m and not grid[nr][nc] and (nr, nc) not in seen:\n                seen.add((nr, nc))\n                q.append((nr, nc, d + 1))\n    return -1',
    ([[[0, 0, 0], [1, 1, 0], [1, 1, 0]]], 5), [[[[0]]], [[[0, 1], [1, 0]]], [[[0, 0], [0, 0]]], [[[1]]]])
add('gp-dijk', 'Network delay time', S, H, "Dijkstra's algorithm", 3, [NC, B75],
    'Signals travel along directed edges [from, to, time]. Starting at node k (nodes are 1..n), return the time for all nodes to receive it, or -1 if some never do.',
    'network_delay_time',
    'def network_delay_time(times, n, k):\n    import heapq\n    graph = {}\n    for u, v, w in times:\n        graph.setdefault(u, []).append((v, w))\n    dist = {}\n    heap = [(0, k)]\n    while heap:\n        d, u = heapq.heappop(heap)\n        if u in dist:\n            continue\n        dist[u] = d\n        for v, w in graph.get(u, []):\n            if v not in dist:\n                heapq.heappush(heap, (d + w, v))\n    return max(dist.values()) if len(dist) == n else -1',
    ([[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], 2), [[[[1, 2, 1]], 2, 1], [[[1, 2, 1]], 2, 2], [[[1, 2, 5], [1, 3, 1], [3, 2, 1]], 3, 1]])

# ---------------- Design problems (operations lists)
H = 'Design'
add('ds-minstack', 'Min stack', S, H, 'Stack with running minimum', 2, [NC, B75],
    'Write min_stack(ops). Each op is ["push", x], ["pop"], ["top"] or ["get_min"]. Run them on a stack that can report its minimum in O(1). Return the results of "top" and "get_min" ops, in order.',
    'min_stack',
    'def min_stack(ops):\n    stack = []\n    out = []\n    for op in ops:\n        if op[0] == "push":\n            x = op[1]\n            stack.append((x, min(x, stack[-1][1]) if stack else x))\n        elif op[0] == "pop":\n            stack.pop()\n        elif op[0] == "top":\n            out.append(stack[-1][0])\n        else:\n            out.append(stack[-1][1])\n    return out',
    ([[["push", -2], ["push", 0], ["push", -3], ["get_min"], ["pop"], ["top"], ["get_min"]]], [-3, 0, -2]), [[[["push", 1], ["get_min"]]], [[["push", 5], ["push", 7], ["get_min"], ["top"]]], [[["push", 2], ["push", 1], ["pop"], ["get_min"]]]])
add('ds-trie', 'Trie (prefix tree)', S, H, 'Nested dict of children', 2, [NC, B75],
    'Write trie_ops(ops). Ops are ["insert", word], ["search", word] (whole word present?) and ["starts_with", prefix]. Return the True/False results of search and starts_with, in order.',
    'trie_ops',
    'def trie_ops(ops):\n    root = {}\n    out = []\n    for op, w in ops:\n        if op == "insert":\n            node = root\n            for c in w:\n                node = node.setdefault(c, {})\n            node["$"] = True\n        else:\n            node = root\n            for c in w:\n                node = node.get(c)\n                if node is None:\n                    break\n            if node is None:\n                out.append(False)\n            elif op == "search":\n                out.append("$" in node)\n            else:\n                out.append(True)\n    return out',
    ([[["insert", "apple"], ["search", "apple"], ["search", "app"], ["starts_with", "app"], ["insert", "app"], ["search", "app"]]], [True, False, True, True]), [[[["insert", "a"], ["search", "b"]]], [[["starts_with", "x"]]], [[["insert", "cat"], ["insert", "car"], ["starts_with", "ca"], ["search", "ca"]]]])
add('ds-lru', 'LRU cache', S, H, 'Ordered dict', 2, [NC, B75, T150],
    'Write lru(capacity, ops). Ops are ["put", key, value] and ["get", key]. When full, put evicts the least recently used key. Both put and get count as a use. Return the result of every get (-1 if missing).',
    'lru',
    'def lru(capacity, ops):\n    from collections import OrderedDict\n    cache = OrderedDict()\n    out = []\n    for op in ops:\n        if op[0] == "put":\n            cache[op[1]] = op[2]\n            cache.move_to_end(op[1])\n            if len(cache) > capacity:\n                cache.popitem(last=False)\n        else:\n            if op[1] in cache:\n                cache.move_to_end(op[1])\n                out.append(cache[op[1]])\n            else:\n                out.append(-1)\n    return out',
    ([2, [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2], ["put", 4, 4], ["get", 1], ["get", 3], ["get", 4]]], [1, -1, -1, 3, 4]), [[1, [["put", 1, 1], ["put", 2, 2], ["get", 1], ["get", 2]]], [2, [["get", 5]]], [2, [["put", 1, 1], ["put", 1, 9], ["get", 1]]]])
