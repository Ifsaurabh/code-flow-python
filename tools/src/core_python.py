from qlib import add
S = 'Core Python'
C = 'Classic'

add('cp-fizz', 'FizzBuzz list', S, 'Control flow', 'Modulo', 1, [C],
    'Return a list for 1..n: "FizzBuzz" for multiples of 15, "Fizz" for 3, "Buzz" for 5, otherwise the number as a string.',
    'fizzbuzz',
    'def fizzbuzz(n):\n    out = []\n    for i in range(1, n + 1):\n        if i % 15 == 0:\n            out.append("FizzBuzz")\n        elif i % 3 == 0:\n            out.append("Fizz")\n        elif i % 5 == 0:\n            out.append("Buzz")\n        else:\n            out.append(str(i))\n    return out',
    ([5], ['1', '2', 'Fizz', '4', 'Buzz']), [[15], [1], [0]])
add('cp-vowels', 'Count vowels', S, 'Strings', 'Loop + membership', 1, [C],
    'Return how many vowels (a, e, i, o, u, any case) are in text.',
    'count_vowels',
    'def count_vowels(text):\n    return sum(1 for c in text.lower() if c in "aeiou")',
    (['Hello World'], 3), [[''], ['rhythm'], ['AEIOU']])
add('cp-wordfreq', 'Word frequencies', S, 'Dictionaries', 'Counting with dict', 1, [C],
    'Return a dict mapping each lower-cased word of text to how many times it appears. Words are separated by spaces.',
    'word_freq',
    'def word_freq(text):\n    freq = {}\n    for w in text.lower().split():\n        freq[w] = freq.get(w, 0) + 1\n    return freq',
    (['the cat and The dog'], {'the': 2, 'cat': 1, 'and': 1, 'dog': 1}), [[''], ['a a a'], ['Go go GO stop']])
add('cp-flatten', 'Flatten a nested list', S, 'Recursion', 'Recursion on lists', 2, [C],
    'Flatten lists nested to any depth into one flat list, keeping order.',
    'flatten',
    'def flatten(items):\n    out = []\n    for x in items:\n        if isinstance(x, list):\n            out.extend(flatten(x))\n        else:\n            out.append(x)\n    return out',
    ([[1, [2, [3, 4]], 5]], [1, 2, 3, 4, 5]), [[[]], [[[[[1]]]]], [[1, 2, 3]]])
add('cp-fib', 'Fibonacci with memoization', S, 'Recursion', 'Memoization', 1, [C],
    'Return the n-th Fibonacci number (fib(0)=0, fib(1)=1). It must stay fast for n = 80.',
    'fib',
    'def fib(n, memo={}):\n    if n < 2:\n        return n\n    if n not in memo:\n        memo[n] = fib(n - 1) + fib(n - 2)\n    return memo[n]',
    ([10], 55), [[0], [1], [30], [80]],
    hints=['Remember answers you already computed. A dict works.'])
add('cp-comp', 'Squares of the evens', S, 'Comprehensions', 'List comprehension', 1, [C],
    'In ONE list comprehension, return the squares of the even numbers in nums.',
    'even_squares',
    'def even_squares(nums):\n    return [n * n for n in nums if n % 2 == 0]',
    ([[1, 2, 3, 4]], [4, 16]), [[[]], [[1, 3]], [[-2, 0, 6]]])
add('cp-invert', 'Invert a dictionary', S, 'Dictionaries', 'Dict comprehension', 1, [C],
    'Swap keys and values of d. If a value repeats, collect its keys in a list. Return {value: [keys...]}.',
    'invert_dict',
    'def invert_dict(d):\n    out = {}\n    for k, v in d.items():\n        out.setdefault(v, []).append(k)\n    return out',
    ([{'a': 1, 'b': 2, 'c': 1}], {1: ['a', 'c'], 2: ['b']}), [[{}], [{'x': 'y'}], [{'p': 0, 'q': 0, 'r': 0}]])
add('cp-genprimes', 'First n primes (generator style)', S, 'Iterators & generators', 'Generator', 2, [C],
    'Return a list of the first n prime numbers. (Challenge: write it with a generator function using yield, then call list() on it.)',
    'first_primes',
    'def first_primes(n):\n    def gen():\n        k = 2\n        while True:\n            if all(k % p for p in range(2, int(k ** 0.5) + 1)):\n                yield k\n            k += 1\n    g = gen()\n    return [next(g) for _ in range(n)]',
    ([5], [2, 3, 5, 7, 11]), [[0], [1], [10]])
add('cp-decor', 'Count calls with a decorator', S, 'Functions & decorators', 'Decorator', 2, [C],
    'Write counted_calls(n): it defines a function add(a, b) wrapped by a decorator that counts calls, calls add n times with (i, i), and returns a pair [sum of results, number of calls counted].',
    'counted_calls',
    'def counted_calls(n):\n    def counter(fn):\n        def wrapper(*args):\n            wrapper.calls += 1\n            return fn(*args)\n        wrapper.calls = 0\n        return wrapper\n    @counter\n    def add(a, b):\n        return a + b\n    total = sum(add(i, i) for i in range(n))\n    return [total, add.calls]',
    ([4], [12, 4]), [[0], [1], [10]])
add('cp-class', 'A bank account class', S, 'OOP', 'Class with state', 2, [C],
    'Write run_account(ops) with a BankAccount class inside it (balance starts at 0). Ops are ["deposit", x] or ["withdraw", x]. A withdraw bigger than the balance is ignored. Return the final balance.',
    'run_account',
    'def run_account(ops):\n    class BankAccount:\n        def __init__(self):\n            self.balance = 0\n        def deposit(self, x):\n            self.balance += x\n        def withdraw(self, x):\n            if x <= self.balance:\n                self.balance -= x\n    acct = BankAccount()\n    for op, x in ops:\n        getattr(acct, op)(x)\n    return acct.balance',
    ([[["deposit", 100], ["withdraw", 30], ["withdraw", 100]]], 70), [[[]], [[["deposit", 5]]], [[["withdraw", 5], ["deposit", 5], ["withdraw", 5]]]])
add('cp-exc', 'Safe division with exceptions', S, 'Errors & exceptions', 'try / except', 1, [C],
    'Return a / b. If b is zero return the string "error". If either is not a number return "bad input".',
    'safe_div',
    'def safe_div(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return "error"\n    except TypeError:\n        return "bad input"',
    ([10, 2], 5.0), [[1, 0], ['x', 2], [7, 'y'], [0, 5]])
add('cp-sortkey', 'Sort people by age then name', S, 'Sorting', 'sorted with key', 1, [C],
    'people is a list of [name, age]. Return it sorted by age (youngest first); ties by name A-Z.',
    'sort_people',
    'def sort_people(people):\n    return sorted(people, key=lambda p: (p[1], p[0]))',
    ([[["Zoe", 30], ["Al", 25], ["Bo", 30]]], [["Al", 25], ["Bo", 30], ["Zoe", 30]]), [[[]], [[["a", 1]]], [[["b", 2], ["a", 2], ["c", 1]]]])
add('cp-caesar', 'Caesar cipher', S, 'Strings', 'ord / chr arithmetic', 1, [C],
    'Shift each letter of text forward by k places (wrapping z to a), keeping case. Leave other characters alone.',
    'caesar',
    'def caesar(text, k):\n    out = []\n    for c in text:\n        if c.isalpha():\n            base = ord("A") if c.isupper() else ord("a")\n            out.append(chr((ord(c) - base + k) % 26 + base))\n        else:\n            out.append(c)\n    return "".join(out)',
    (['Hello, World!', 3], 'Khoor, Zruog!'), [['xyz', 3], ['abc', 0], ['Abc', 26], ['Zz', -1]])
add('cp-matmul', 'Matrix multiplication', S, 'Lists', 'Nested loops', 2, [C],
    'Multiply matrix a (m x n) by matrix b (n x p) without libraries and return the m x p result.',
    'matmul',
    'def matmul(a, b):\n    n, p = len(b), len(b[0])\n    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(p)] for i in range(len(a))]',
    ([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], [[19, 22], [43, 50]]), [[[[1, 0], [0, 1]], [[9, 8], [7, 6]]], [[[2]], [[3]]], [[[1, 2, 3]], [[1], [2], [3]]]])
add('cp-anagram-sort', 'Sort words by length then alphabet', S, 'Sorting', 'Multi-key sort', 1, [C],
    'Return words sorted by length (shortest first), ties alphabetical.',
    'sort_words',
    'def sort_words(words):\n    return sorted(words, key=lambda w: (len(w), w))',
    ([['pear', 'fig', 'apple', 'kiwi']], ['fig', 'kiwi', 'pear', 'apple']), [[[]], [['b', 'a']], [['bb', 'a', 'aa', 'c']]])
