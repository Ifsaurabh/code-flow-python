from qlib import add
S = 'Data Structures & Algorithms'
NC = 'NeetCode 150 style'; B75 = 'Blind 75 style'; T150 = 'Top Interview 150 style'

# ---------------- Arrays & Hashing
H = 'Arrays & Hashing'
add('ah-dup', 'Contains duplicate', S, H, 'Hash set', 1, [NC, B75, T150],
    'Return True if any value appears at least twice in nums, otherwise False.',
    'contains_duplicate',
    'def contains_duplicate(nums):\n    seen = set()\n    for n in nums:\n        if n in seen:\n            return True\n        seen.add(n)\n    return False',
    ([[1, 2, 3, 1]], True), [[[1, 2, 3, 4]], [[]], [[5]], [[7, 7]]],
    hints=['A set remembers what you have seen in O(1) per lookup.', 'Check membership before you add.'])
add('ah-anagram', 'Valid anagram', S, H, 'Frequency map', 1, [NC, B75],
    'Return True if t uses exactly the same letters as s, the same number of times each.',
    'is_anagram',
    'def is_anagram(s, t):\n    if len(s) != len(t):\n        return False\n    count = {}\n    for c in s:\n        count[c] = count.get(c, 0) + 1\n    for c in t:\n        if count.get(c, 0) == 0:\n            return False\n        count[c] -= 1\n    return True',
    (['listen', 'silent'], True), [['rat', 'car'], ['a', 'a'], ['ab', 'a'], ['aacc', 'ccac']],
    hints=['Count letters of s in a dict, then spend them with t.'])
add('ah-twosum', 'Two sum', S, H, 'Hash map complement', 1, [NC, B75, T150],
    'nums has exactly one pair adding up to target. Return the two indices as [smaller, larger].',
    'two_sum',
    'def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        need = target - n\n        if need in seen:\n            return [seen[need], i]\n        seen[n] = i',
    ([[2, 7, 11, 15], 9], [0, 1]), [[[3, 2, 4], 6], [[3, 3], 6], [[-1, -2, -3, -4, -5], -8]],
    hints=['For each number, which partner would complete the target?', 'Store value -> index as you go.'])
add('ah-groupana', 'Group anagrams', S, H, 'Canonical key', 2, [NC, B75],
    'Group the words that are anagrams of each other. Return a list of groups (any order, any order inside a group).',
    'group_anagrams',
    'def group_anagrams(words):\n    groups = {}\n    for w in words:\n        key = "".join(sorted(w))\n        groups.setdefault(key, []).append(w)\n    return list(groups.values())',
    ([['eat', 'tea', 'tan', 'ate', 'nat', 'bat']], [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]),
    [[['a']], [['']], [['abc', 'bca', 'xyz', 'zyx', 'cab']]], compare='nested_unordered',
    hints=['Anagrams share the same sorted letters.'])
add('ah-topk', 'Top K frequent elements', S, H, 'Frequency map + bucket', 2, [NC, B75],
    'Return the k values that occur most often in nums. Any order. The answer is unique.',
    'top_k_frequent',
    'def top_k_frequent(nums, k):\n    count = {}\n    for n in nums:\n        count[n] = count.get(n, 0) + 1\n    buckets = [[] for _ in range(len(nums) + 1)]\n    for n, c in count.items():\n        buckets[c].append(n)\n    out = []\n    for c in range(len(buckets) - 1, 0, -1):\n        for n in buckets[c]:\n            out.append(n)\n            if len(out) == k:\n                return out\n    return out',
    ([[1, 1, 1, 2, 2, 3], 2], [1, 2]), [[[1], 1], [[4, 4, 4, 5, 5, 6, 6, 6, 6], 2], [[-1, -1, 2, 2, 2, 3], 1]],
    compare='unordered', hints=['Count first. Then think: how large can a count be? Use that as an index.'])
add('ah-product', 'Product of array except self', S, H, 'Prefix and suffix', 2, [NC, B75, T150],
    'Return a list where element i is the product of every number except nums[i]. Do not use division.',
    'product_except_self',
    'def product_except_self(nums):\n    n = len(nums)\n    out = [1] * n\n    left = 1\n    for i in range(n):\n        out[i] = left\n        left *= nums[i]\n    right = 1\n    for i in range(n - 1, -1, -1):\n        out[i] *= right\n        right *= nums[i]\n    return out',
    ([[1, 2, 3, 4]], [24, 12, 8, 6]), [[[-1, 1, 0, -3, 3]], [[2, 3]], [[0, 0, 2]]],
    hints=['Product of everything to the left of i times everything to the right.'])
add('ah-consec', 'Longest consecutive sequence', S, H, 'Hash set + sequence starts', 2, [NC, B75, T150],
    'Return the length of the longest run of consecutive integers (like 3,4,5,6) that can be found in nums, in any order.',
    'longest_consecutive',
    'def longest_consecutive(nums):\n    s = set(nums)\n    best = 0\n    for n in s:\n        if n - 1 not in s:\n            length = 1\n            while n + length in s:\n                length += 1\n            best = max(best, length)\n    return best',
    ([[100, 4, 200, 1, 3, 2]], 4), [[[]], [[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], [[1, 2, 0, 1]], [[9]]],
    hints=['Only start counting at numbers whose predecessor is missing.'])
add('ah-firstuniq', 'First unique character', S, H, 'Frequency map', 1, [],
    'Return the index of the first character in s that appears only once, or -1.',
    'first_unique_char',
    'def first_unique_char(s):\n    count = {}\n    for c in s:\n        count[c] = count.get(c, 0) + 1\n    for i, c in enumerate(s):\n        if count[c] == 1:\n            return i\n    return -1',
    (['leetcode'], 0), [['loveleetcode'], ['aabb'], [''], ['z']])
add('ah-majority', 'Majority element', S, H, 'Boyer-Moore voting', 1, [T150],
    'One value appears more than len(nums)/2 times. Return it. Try to use O(1) extra memory.',
    'majority_element',
    'def majority_element(nums):\n    cand, votes = None, 0\n    for n in nums:\n        if votes == 0:\n            cand = n\n        votes += 1 if n == cand else -1\n    return cand',
    ([[2, 2, 1, 1, 1, 2, 2]], 2), [[[3, 2, 3]], [[1]], [[5, 5, 5, 1, 2]]],
    hints=['Pair off different values. The majority always survives.'])
add('ah-missing', 'Missing number', S, H, 'Sum / XOR trick', 1, [],
    'nums holds n distinct numbers taken from 0..n. Return the one number missing from the range.',
    'missing_number',
    'def missing_number(nums):\n    n = len(nums)\n    return n * (n + 1) // 2 - sum(nums)',
    ([[3, 0, 1]], 2), [[[0, 1]], [[9, 6, 4, 2, 3, 5, 7, 0, 1]], [[0]]])
add('ah-subsumk', 'Subarray sum equals K', S, H, 'Prefix sum + hash map', 2, [],
    'Count the contiguous subarrays of nums whose sum equals k.',
    'subarray_sum',
    'def subarray_sum(nums, k):\n    seen = {0: 1}\n    total = 0\n    count = 0\n    for n in nums:\n        total += n\n        count += seen.get(total - k, 0)\n        seen[total] = seen.get(total, 0) + 1\n    return count',
    ([[1, 1, 1], 2], 2), [[[1, 2, 3], 3], [[1, -1, 0], 0], [[3, 4, 7, 2, -3, 1, 4, 2], 7]],
    hints=['prefix[j] - prefix[i] == k means prefix[i] == prefix[j] - k.'])
add('ah-zeroes', 'Move zeroes', S, H, 'In-place write pointer', 1, [],
    'Move every 0 to the end of nums, keeping the order of the other values. Change the list in place.',
    'move_zeroes',
    'def move_zeroes(nums):\n    w = 0\n    for r in range(len(nums)):\n        if nums[r] != 0:\n            nums[w], nums[r] = nums[r], nums[w]\n            w += 1',
    ([[0, 1, 0, 3, 12]], [1, 3, 12, 0, 0]), [[[0]], [[1, 2, 3]], [[0, 0, 1]], [[4, 0, 5, 0, 0, 6]]], inplace=0)
add('ah-rotate', 'Rotate array', S, H, 'Reverse trick', 2, [T150],
    'Rotate nums to the right by k steps, in place.',
    'rotate',
    'def rotate(nums, k):\n    n = len(nums)\n    k %= n\n    nums.reverse()\n    nums[:k] = reversed(nums[:k])\n    nums[k:] = reversed(nums[k:])',
    ([[1, 2, 3, 4, 5, 6, 7], 3], [5, 6, 7, 1, 2, 3, 4]), [[[-1, -100, 3, 99], 2], [[1, 2], 5], [[1], 3]], inplace=0)
add('ah-isomorphic', 'Isomorphic strings', S, H, 'Two-way mapping', 1, [T150],
    'Return True if the characters of s can be replaced one-to-one to get t (same positions, no two letters share a target).',
    'is_isomorphic',
    'def is_isomorphic(s, t):\n    a, b = {}, {}\n    for x, y in zip(s, t):\n        if a.setdefault(x, y) != y or b.setdefault(y, x) != x:\n            return False\n    return True',
    (['egg', 'add'], True), [['foo', 'bar'], ['paper', 'title'], ['ab', 'aa']])
add('ah-happy', 'Happy number', S, H, 'Cycle detection with set', 1, [T150],
    'Repeatedly replace n with the sum of the squares of its digits. Return True if you reach 1, False if it loops forever.',
    'is_happy',
    'def is_happy(n):\n    seen = set()\n    while n != 1 and n not in seen:\n        seen.add(n)\n        n = sum(int(d) ** 2 for d in str(n))\n    return n == 1',
    ([19], True), [[2], [1], [7], [4]])

# ---------------- Two Pointers
H = 'Two Pointers'
add('tp-palin', 'Valid palindrome', S, H, 'Two pointers from both ends', 1, [NC, B75, T150],
    'Ignoring case and anything that is not a letter or digit, is s a palindrome?',
    'is_palindrome',
    'def is_palindrome(s):\n    i, j = 0, len(s) - 1\n    while i < j:\n        while i < j and not s[i].isalnum():\n            i += 1\n        while i < j and not s[j].isalnum():\n            j -= 1\n        if s[i].lower() != s[j].lower():\n            return False\n        i += 1\n        j -= 1\n    return True',
    (['A man, a plan, a canal: Panama'], True), [['race a car'], [' '], ['0P'], ['No lemon, no melon']])
add('tp-twosum2', 'Two sum in a sorted list', S, H, 'Converging pointers', 1, [NC, B75],
    'numbers is sorted ascending. Return the 1-based positions [i, j] (i < j) of the two values that add up to target.',
    'two_sum_sorted',
    'def two_sum_sorted(numbers, target):\n    i, j = 0, len(numbers) - 1\n    while i < j:\n        s = numbers[i] + numbers[j]\n        if s == target:\n            return [i + 1, j + 1]\n        if s < target:\n            i += 1\n        else:\n            j -= 1',
    ([[2, 7, 11, 15], 9], [1, 2]), [[[2, 3, 4], 6], [[-1, 0], -1], [[1, 2, 3, 4, 4, 9, 56, 90], 8]])
add('tp-3sum', '3Sum', S, H, 'Sort + two pointers', 2, [NC, B75, T150],
    'Return every unique triplet in nums that adds up to 0. No duplicate triplets. Any order.',
    'three_sum',
    'def three_sum(nums):\n    nums = sorted(nums)\n    out = []\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n        j, k = i + 1, len(nums) - 1\n        while j < k:\n            s = nums[i] + nums[j] + nums[k]\n            if s < 0:\n                j += 1\n            elif s > 0:\n                k -= 1\n            else:\n                out.append([nums[i], nums[j], nums[k]])\n                j += 1\n                while j < k and nums[j] == nums[j - 1]:\n                    j += 1\n    return out',
    ([[-1, 0, 1, 2, -1, -4]], [[-1, -1, 2], [-1, 0, 1]]), [[[0, 1, 1]], [[0, 0, 0, 0]], [[-2, 0, 1, 1, 2]]],
    compare='nested_unordered', hints=['Sort. Fix one number, then run two pointers on the rest.', 'Skip repeated values so triplets stay unique.'])
add('tp-water', 'Container with most water', S, H, 'Converging pointers (greedy move)', 2, [NC, B75, T150],
    'heights[i] is a vertical line at x = i. Pick two lines; the water held is (distance apart) x (the shorter line). Return the maximum.',
    'max_area',
    'def max_area(heights):\n    i, j = 0, len(heights) - 1\n    best = 0\n    while i < j:\n        best = max(best, (j - i) * min(heights[i], heights[j]))\n        if heights[i] < heights[j]:\n            i += 1\n        else:\n            j -= 1\n    return best',
    ([[1, 8, 6, 2, 5, 4, 8, 3, 7]], 49), [[[1, 1]], [[4, 3, 2, 1, 4]], [[1, 2, 1]]],
    hints=['Moving the taller line can never help. Move the shorter one.'])
add('tp-trap', 'Trapping rain water', S, H, 'Two pointers with running max', 3, [NC, B75, T150],
    'heights are bar heights, each 1 wide. After rain, how many units of water are trapped between the bars?',
    'trap',
    'def trap(heights):\n    i, j = 0, len(heights) - 1\n    lmax = rmax = water = 0\n    while i < j:\n        if heights[i] < heights[j]:\n            lmax = max(lmax, heights[i])\n            water += lmax - heights[i]\n            i += 1\n        else:\n            rmax = max(rmax, heights[j])\n            water += rmax - heights[j]\n            j -= 1\n    return water',
    ([[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], 6), [[[4, 2, 0, 3, 2, 5]], [[]], [[3, 3, 3]], [[5, 0, 5]]],
    hints=['Water above a bar = min(tallest on left, tallest on right) - bar.'])
add('tp-dedup', 'Remove duplicates from sorted list', S, H, 'Slow and fast pointers', 1, [T150],
    'nums is sorted. Remove duplicates in place and return how many unique values remain (the first part of nums must hold them).',
    'remove_duplicates',
    'def remove_duplicates(nums):\n    if not nums:\n        return 0\n    w = 1\n    for r in range(1, len(nums)):\n        if nums[r] != nums[w - 1]:\n            nums[w] = nums[r]\n            w += 1\n    return w',
    ([[1, 1, 2]], 2), [[[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]], [[]], [[7]]])
add('tp-squares', 'Squares of a sorted list', S, H, 'Two pointers, fill from the back', 1, [],
    'nums is sorted ascending and may contain negatives. Return the squares, also sorted ascending, in O(n).',
    'sorted_squares',
    'def sorted_squares(nums):\n    out = [0] * len(nums)\n    i, j = 0, len(nums) - 1\n    for k in range(len(nums) - 1, -1, -1):\n        if abs(nums[i]) > abs(nums[j]):\n            out[k] = nums[i] ** 2\n            i += 1\n        else:\n            out[k] = nums[j] ** 2\n            j -= 1\n    return out',
    ([[-4, -1, 0, 3, 10]], [0, 1, 9, 16, 100]), [[[-7, -3, 2, 3, 11]], [[-5]], [[1, 2, 3]]])
add('tp-reverse', 'Reverse a list of characters', S, H, 'Swap from both ends', 1, [],
    'Reverse the list chars in place. Do not create a new list.',
    'reverse_chars',
    'def reverse_chars(chars):\n    i, j = 0, len(chars) - 1\n    while i < j:\n        chars[i], chars[j] = chars[j], chars[i]\n        i += 1\n        j -= 1',
    ([['h', 'e', 'l', 'l', 'o']], ['o', 'l', 'l', 'e', 'h']), [[['a']], [[]], [['a', 'b']]], inplace=0)
add('tp-subseq', 'Is subsequence', S, H, 'Two pointers on two strings', 1, [T150],
    'Return True if s can be made from t by deleting some characters of t without reordering the rest.',
    'is_subsequence',
    'def is_subsequence(s, t):\n    i = 0\n    for c in t:\n        if i < len(s) and s[i] == c:\n            i += 1\n    return i == len(s)',
    (['abc', 'ahbgdc'], True), [['axc', 'ahbgdc'], ['', 'abc'], ['a', '']])

# ---------------- Sliding Window
H = 'Sliding Window'
add('sw-stock', 'Best time to buy and sell stock', S, H, 'Running minimum', 1, [NC, B75, T150],
    'prices[i] is the price on day i. Buy once, then sell on a later day. Return the largest profit, or 0 if none is possible.',
    'max_profit',
    'def max_profit(prices):\n    low = float("inf")\n    best = 0\n    for p in prices:\n        low = min(low, p)\n        best = max(best, p - low)\n    return best',
    ([[7, 1, 5, 3, 6, 4]], 5), [[[7, 6, 4, 3, 1]], [[1, 2]], [[2, 4, 1]], [[3]]])
add('sw-nonrep', 'Longest substring without repeating characters', S, H, 'Variable window + last-seen map', 2, [NC, B75, T150],
    'Return the length of the longest stretch of s in which no character repeats.',
    'length_of_longest_substring',
    'def length_of_longest_substring(s):\n    last = {}\n    left = best = 0\n    for right, c in enumerate(s):\n        if c in last and last[c] >= left:\n            left = last[c] + 1\n        last[c] = right\n        best = max(best, right - left + 1)\n    return best',
    (['abcabcbb'], 3), [['bbbbb'], ['pwwkew'], [''], ['dvdf'], ['abba']],
    hints=['Move the left edge just past the previous copy of the repeated character.'])
add('sw-replace', 'Longest repeating character replacement', S, H, 'Variable window + max frequency', 2, [NC, B75],
    'You may change at most k characters of s to any letter. Return the length of the longest stretch that can become one repeated letter.',
    'character_replacement',
    'def character_replacement(s, k):\n    count = {}\n    left = best = maxf = 0\n    for right, c in enumerate(s):\n        count[c] = count.get(c, 0) + 1\n        maxf = max(maxf, count[c])\n        while (right - left + 1) - maxf > k:\n            count[s[left]] -= 1\n            left += 1\n        best = max(best, right - left + 1)\n    return best',
    (['AABABBA', 1], 4), [['ABAB', 2], ['AAAA', 2], ['ABCDE', 1], ['', 3]])
add('sw-maxsumk', 'Maximum sum of k in a row', S, H, 'Fixed window', 1, [],
    'Return the largest sum of any k consecutive numbers in nums (k <= len(nums)).',
    'max_sum_k',
    'def max_sum_k(nums, k):\n    window = sum(nums[:k])\n    best = window\n    for i in range(k, len(nums)):\n        window += nums[i] - nums[i - k]\n        best = max(best, window)\n    return best',
    ([[2, 1, 5, 1, 3, 2], 3], 9), [[[1, 4, 2, 10, 23, 3, 1, 0, 20], 4], [[-1, -2, -3], 2], [[5], 1]],
    hints=['Slide: add the new element, drop the one that left.'])
add('sw-minlen', 'Minimum size subarray sum', S, H, 'Variable window (shrink when valid)', 2, [T150],
    'All numbers in nums are positive. Return the length of the shortest contiguous piece with sum >= target, or 0 if none.',
    'min_subarray_len',
    'def min_subarray_len(target, nums):\n    left = total = 0\n    best = float("inf")\n    for right, n in enumerate(nums):\n        total += n\n        while total >= target:\n            best = min(best, right - left + 1)\n            total -= nums[left]\n            left += 1\n    return 0 if best == float("inf") else best',
    ([7, [2, 3, 1, 2, 4, 3]], 2), [[4, [1, 4, 4]], [11, [1, 1, 1, 1, 1, 1, 1, 1]], [15, [1, 2, 3, 4, 5]]])
add('sw-permstr', 'Permutation in string', S, H, 'Fixed window + frequency compare', 2, [NC, B75],
    'Return True if some rearrangement of s1 appears as a contiguous piece of s2.',
    'check_inclusion',
    'def check_inclusion(s1, s2):\n    if len(s1) > len(s2):\n        return False\n    need = {}\n    for c in s1:\n        need[c] = need.get(c, 0) + 1\n    have = {}\n    k = len(s1)\n    for i, c in enumerate(s2):\n        have[c] = have.get(c, 0) + 1\n        if i >= k:\n            old = s2[i - k]\n            have[old] -= 1\n            if have[old] == 0:\n                del have[old]\n        if have == need:\n            return True\n    return False',
    (['ab', 'eidbaooo'], True), [['ab', 'eidboaoo'], ['a', 'a'], ['abc', 'ab'], ['adc', 'dcda']])
add('sw-maxwin', 'Sliding window maximum', S, H, 'Monotonic deque', 3, [NC, B75],
    'For every window of k consecutive numbers in nums, report its maximum. Return the list of maximums.',
    'max_sliding_window',
    'def max_sliding_window(nums, k):\n    from collections import deque\n    dq = deque()\n    out = []\n    for i, n in enumerate(nums):\n        while dq and nums[dq[-1]] <= n:\n            dq.pop()\n        dq.append(i)\n        if dq[0] <= i - k:\n            dq.popleft()\n        if i >= k - 1:\n            out.append(nums[dq[0]])\n    return out',
    ([[1, 3, -1, -3, 5, 3, 6, 7], 3], [3, 3, 5, 5, 6, 7]), [[[1], 1], [[9, 11], 2], [[4, 3, 2, 1], 2], [[1, 3, 1, 2, 0, 5], 3]],
    hints=['Keep a deque of indices whose values are in decreasing order.'])
add('sw-minwin', 'Minimum window substring', S, H, 'Variable window + need/have counters', 3, [NC, B75, T150],
    'Return the shortest piece of s that contains every character of t (with repeats). Return "" if none exists.',
    'min_window',
    'def min_window(s, t):\n    if not t or len(t) > len(s):\n        return ""\n    need = {}\n    for c in t:\n        need[c] = need.get(c, 0) + 1\n    missing = len(t)\n    left = 0\n    best = (float("inf"), 0, 0)\n    for right, c in enumerate(s):\n        if need.get(c, 0) > 0:\n            missing -= 1\n        need[c] = need.get(c, 0) - 1\n        if missing == 0:\n            while need[s[left]] < 0:\n                need[s[left]] += 1\n                left += 1\n            if right - left + 1 < best[0]:\n                best = (right - left + 1, left, right)\n            need[s[left]] += 1\n            missing += 1\n            left += 1\n    return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]',
    (['ADOBECODEBANC', 'ABC'], 'BANC'), [['a', 'a'], ['a', 'aa'], ['ab', 'b'], ['aa', 'aa']])
add('sw-ones3', 'Max consecutive ones with k flips', S, H, 'Variable window (count zeros)', 2, [],
    'nums holds 0s and 1s. You may flip at most k zeros to 1. Return the longest run of 1s you can make.',
    'longest_ones',
    'def longest_ones(nums, k):\n    left = zeros = best = 0\n    for right, n in enumerate(nums):\n        zeros += n == 0\n        while zeros > k:\n            zeros -= nums[left] == 0\n            left += 1\n        best = max(best, right - left + 1)\n    return best',
    ([[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2], 6), [[[0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3], [[0, 0], 0], [[1, 1], 0]])
