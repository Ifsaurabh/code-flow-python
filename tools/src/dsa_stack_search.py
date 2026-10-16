from qlib import add
S = 'Data Structures & Algorithms'
NC = 'NeetCode 150 style'; B75 = 'Blind 75 style'; T150 = 'Top Interview 150 style'

H = 'Stack'
add('st-paren', 'Valid parentheses', S, H, 'Stack of openers', 1, [NC, B75, T150],
    's contains only ()[]{}. Return True if every bracket is closed by the right kind, in the right order.',
    'is_valid',
    'def is_valid(s):\n    pairs = {")": "(", "]": "[", "}": "{"}\n    stack = []\n    for c in s:\n        if c in pairs:\n            if not stack or stack.pop() != pairs[c]:\n                return False\n        else:\n            stack.append(c)\n    return not stack',
    (['()[]{}'], True), [['(]'], ['([)]'], ['{[]}'], [''], ['(('], ['))']],
    hints=['Push openers. On a closer, the top of the stack must be its partner.'])
add('st-daily', 'Daily temperatures', S, H, 'Monotonic stack', 2, [NC, B75],
    'For each day, how many days until a warmer temperature? Use 0 if there is none.',
    'daily_temperatures',
    'def daily_temperatures(temps):\n    out = [0] * len(temps)\n    stack = []\n    for i, t in enumerate(temps):\n        while stack and temps[stack[-1]] < t:\n            j = stack.pop()\n            out[j] = i - j\n        stack.append(i)\n    return out',
    ([[73, 74, 75, 71, 69, 72, 76, 73]], [1, 1, 4, 2, 1, 1, 0, 0]), [[[30, 40, 50, 60]], [[30, 60, 90]], [[90, 80, 70]], [[5]]],
    hints=['Keep a stack of days still waiting for a warmer day.'])
add('st-rpn', 'Evaluate reverse Polish notation', S, H, 'Operand stack', 2, [NC, B75],
    'tokens is a list of numbers (as strings) and the operators + - * /. Evaluate it. Division truncates toward zero.',
    'eval_rpn',
    'def eval_rpn(tokens):\n    stack = []\n    for t in tokens:\n        if t in "+-*/" and len(t) == 1:\n            b = stack.pop()\n            a = stack.pop()\n            if t == "+":\n                stack.append(a + b)\n            elif t == "-":\n                stack.append(a - b)\n            elif t == "*":\n                stack.append(a * b)\n            else:\n                stack.append(int(a / b))\n        else:\n            stack.append(int(t))\n    return stack[0]',
    ([['2', '1', '+', '3', '*']], 9), [[['4', '13', '5', '/', '+']], [['10', '6', '9', '3', '+', '-11', '*', '/', '*', '17', '+', '5', '+']], [['7']], [['3', '-2', '/']]])
add('st-fleet', 'Car fleet', S, H, 'Sort + monotonic stack', 2, [NC],
    'Cars at given positions drive toward target at given speeds; a car cannot pass another, it joins its fleet at the slower speed. Return the number of fleets that arrive.',
    'car_fleet',
    'def car_fleet(target, position, speed):\n    cars = sorted(zip(position, speed), reverse=True)\n    stack = []\n    for p, s in cars:\n        t = (target - p) / s\n        if not stack or t > stack[-1]:\n            stack.append(t)\n    return len(stack)',
    ([12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]], 3), [[10, [3], [3]], [100, [0, 2, 4], [4, 2, 1]], [10, [6, 8], [3, 2]]])
add('st-hist', 'Largest rectangle in histogram', S, H, 'Monotonic stack', 3, [NC, B75],
    'heights are bar heights (each 1 wide). Return the area of the largest rectangle that fits entirely inside the bars.',
    'largest_rectangle',
    'def largest_rectangle(heights):\n    stack = []\n    best = 0\n    for i, h in enumerate(heights + [0]):\n        start = i\n        while stack and stack[-1][1] >= h:\n            idx, height = stack.pop()\n            best = max(best, height * (i - idx))\n            start = idx\n        stack.append((start, h))\n    return best',
    ([[2, 1, 5, 6, 2, 3]], 10), [[[2, 4]], [[1]], [[6, 2, 5, 4, 5, 1, 6]], [[]]])
add('st-nge', 'Next greater element', S, H, 'Monotonic stack', 1, [],
    'For each number, find the first larger number to its right. Use -1 if none.',
    'next_greater',
    'def next_greater(nums):\n    out = [-1] * len(nums)\n    stack = []\n    for i, n in enumerate(nums):\n        while stack and nums[stack[-1]] < n:\n            out[stack.pop()] = n\n        stack.append(i)\n    return out',
    ([[4, 5, 2, 25]], [5, 25, 25, -1]), [[[13, 7, 6, 12]], [[1, 1, 1]], [[3, 2, 1]]])
add('st-adj', 'Remove adjacent duplicates', S, H, 'Stack as a builder', 1, [],
    'Repeatedly delete two equal neighbouring letters from s until none are left. Return the result.',
    'remove_duplicates_str',
    'def remove_duplicates_str(s):\n    stack = []\n    for c in s:\n        if stack and stack[-1] == c:\n            stack.pop()\n        else:\n            stack.append(c)\n    return "".join(stack)',
    (['abbaca'], 'ca'), [['azxxzy'], [''], ['aaaa'], ['abc']])
add('st-decode', 'Decode string', S, H, 'Stack of (count, prefix)', 2, [],
    'Decode strings like 3[a2[c]] into accaccacc. The pattern is k[text] and it can nest.',
    'decode_string',
    'def decode_string(s):\n    stack = []\n    cur = ""\n    num = 0\n    for c in s:\n        if c.isdigit():\n            num = num * 10 + int(c)\n        elif c == "[":\n            stack.append((cur, num))\n            cur, num = "", 0\n        elif c == "]":\n            prev, k = stack.pop()\n            cur = prev + cur * k\n        else:\n            cur += c\n    return cur',
    (['3[a2[c]]'], 'accaccacc'), [['2[abc]3[cd]ef'], ['abc'], ['10[a]'], ['2[2[2[x]]]']])

H = 'Binary Search'
add('bs-basic', 'Binary search', S, H, 'Halve the range', 1, [NC],
    'nums is sorted ascending. Return the index of target, or -1.',
    'search',
    'def search(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1',
    ([[-1, 0, 3, 5, 9, 12], 9], 4), [[[-1, 0, 3, 5, 9, 12], 2], [[5], 5], [[], 1], [[1, 3], 3]],
    hints=['Look at the middle. Which half can the target still be in?'])
add('bs-insert', 'Search insert position', S, H, 'Lower bound', 1, [],
    'nums is sorted and has distinct values. Return the index of target, or the index where it would be inserted.',
    'search_insert',
    'def search_insert(nums, target):\n    lo, hi = 0, len(nums)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo',
    ([[1, 3, 5, 6], 5], 2), [[[1, 3, 5, 6], 2], [[1, 3, 5, 6], 7], [[1, 3, 5, 6], 0], [[], 4]])
add('bs-matrix', 'Search a sorted 2D matrix', S, H, 'Treat as one flat sorted list', 2, [NC, B75],
    'Each row is sorted and each row starts after the previous row ends. Return True if target is in the matrix.',
    'search_matrix',
    'def search_matrix(matrix, target):\n    if not matrix or not matrix[0]:\n        return False\n    rows, cols = len(matrix), len(matrix[0])\n    lo, hi = 0, rows * cols - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        v = matrix[mid // cols][mid % cols]\n        if v == target:\n            return True\n        if v < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return False',
    ([[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3], True), [[[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13], [[[1]], 1], [[[1], [3]], 3]])
add('bs-koko', 'Koko eating bananas', S, H, 'Binary search on the answer', 2, [NC],
    'piles[i] is a pile of bananas. Each hour Koko picks one pile and eats up to k from it. Return the smallest k that finishes everything within h hours.',
    'min_eating_speed',
    'def min_eating_speed(piles, h):\n    lo, hi = 1, max(piles)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        hours = sum((p + mid - 1) // mid for p in piles)\n        if hours <= h:\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo',
    ([[3, 6, 7, 11], 8], 4), [[[30, 11, 23, 4, 20], 5], [[30, 11, 23, 4, 20], 6], [[1], 1], [[312884470], 312884469]],
    hints=['If speed k works, any faster speed works too. That is a sorted yes/no question.'])
add('bs-minrot', 'Minimum in rotated sorted list', S, H, 'Compare with the right end', 2, [NC, B75],
    'A sorted list with distinct values was rotated. Return its minimum in O(log n).',
    'find_min',
    'def find_min(nums):\n    lo, hi = 0, len(nums) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] > nums[hi]:\n            lo = mid + 1\n        else:\n            hi = mid\n    return nums[lo]',
    ([[3, 4, 5, 1, 2]], 1), [[[4, 5, 6, 7, 0, 1, 2]], [[11, 13, 15, 17]], [[2, 1]], [[1]]])
add('bs-rot', 'Search in rotated sorted list', S, H, 'Find the sorted half', 2, [NC, B75, T150],
    'A sorted list with distinct values was rotated at an unknown spot. Return the index of target or -1 in O(log n).',
    'search_rotated',
    'def search_rotated(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[lo] <= nums[mid]:\n            if nums[lo] <= target < nums[mid]:\n                hi = mid - 1\n            else:\n                lo = mid + 1\n        else:\n            if nums[mid] < target <= nums[hi]:\n                lo = mid + 1\n            else:\n                hi = mid - 1\n    return -1',
    ([[4, 5, 6, 7, 0, 1, 2], 0], 4), [[[4, 5, 6, 7, 0, 1, 2], 3], [[1], 0], [[3, 1], 1], [[5, 1, 3], 5]])
add('bs-sqrt', 'Integer square root', S, H, 'Binary search on the answer', 1, [T150],
    'Return the integer part of the square root of x (x >= 0) without using sqrt or **0.5.',
    'my_sqrt',
    'def my_sqrt(x):\n    lo, hi = 0, x\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if mid * mid <= x:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return hi',
    ([8], 2), [[4], [0], [1], [99], [2147395599]])
add('bs-median', 'Median of two sorted lists', S, H, 'Partition binary search', 3, [NC, B75, T150],
    'Two sorted lists a and b. Return the median of all their values combined. Aim for O(log(min(m, n))).',
    'find_median',
    'def find_median(a, b):\n    if len(a) > len(b):\n        a, b = b, a\n    m, n = len(a), len(b)\n    half = (m + n + 1) // 2\n    lo, hi = 0, m\n    while lo <= hi:\n        i = (lo + hi) // 2\n        j = half - i\n        al = a[i - 1] if i > 0 else float("-inf")\n        ar = a[i] if i < m else float("inf")\n        bl = b[j - 1] if j > 0 else float("-inf")\n        br = b[j] if j < n else float("inf")\n        if al <= br and bl <= ar:\n            if (m + n) % 2:\n                return max(al, bl)\n            return (max(al, bl) + min(ar, br)) / 2\n        if al > br:\n            hi = i - 1\n        else:\n            lo = i + 1',
    ([[1, 3], [2]], 2), [[[1, 2], [3, 4]], [[], [1]], [[0, 0], [0, 0]], [[1, 5, 9], [2, 3, 4, 10]]], compare='float')
add('bs-peak', 'Find a peak element', S, H, 'Binary search on slope', 2, [],
    'A peak is bigger than both neighbours (edges count as -infinity). Return the index of any peak. For this exercise return the index of the LEFTMOST peak.',
    'find_peak',
    'def find_peak(nums):\n    for i in range(len(nums)):\n        left = nums[i - 1] if i > 0 else float("-inf")\n        right = nums[i + 1] if i < len(nums) - 1 else float("inf") * -1\n        if nums[i] > left and nums[i] > right:\n            return i',
    ([[1, 2, 3, 1]], 2), [[[1, 2, 1, 3, 5, 6, 4]], [[5]], [[1, 2]], [[3, 2, 1]]],
    note='Then try to beat O(n): can you solve it in O(log n) and still return a valid peak?')
