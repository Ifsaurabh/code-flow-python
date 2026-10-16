from qlib import qa

# ---------------- Basic
qa('qa-b-mutable', 'Mutable vs immutable types', 'Data types', 'Basic',
   'What is the difference between mutable and immutable objects in Python? Give examples of each and one bug it can cause.',
   'Mutable objects can be changed after creation (list, dict, set). Immutable ones cannot (int, float, str, tuple, frozenset, bytes): any "change" builds a new object.\n\nBug: two names can point at the same mutable object, so changing it through one name changes it for the other:\n\na = [1, 2]; b = a; b.append(3)  -> a is now [1, 2, 3]\n\nAnother classic: a mutable default argument like def f(x, acc=[]) shares one list across all calls. Use None as the default and create the list inside.',
   ['Think about what "b = a" copies: the object or the reference?'])
qa('qa-b-listtuple', 'List vs tuple', 'Data types', 'Basic',
   'When would you use a tuple instead of a list?',
   'A tuple is an ordered, immutable sequence; a list is an ordered, mutable one. Use a tuple for fixed groups of values that belong together (a point (x, y), a database row, a return value with several parts) and when you need something hashable, e.g. as a dict key or set member (a tuple of hashables is hashable, a list never is). Tuples are slightly smaller and faster to create. Use a list when the collection grows, shrinks or gets reordered.')
qa('qa-b-is-eq', '== versus is', 'Basics', 'Basic',
   'What is the difference between == and is? Why is "x is None" the recommended way to test for None?',
   '== asks "do these two objects have equal values?" (it calls __eq__). is asks "are these literally the same object in memory?" (identity, compares id()).\n\na = [1]; b = [1]  ->  a == b is True, a is b is False.\n\nNone is a singleton, so there is exactly one None object. "is None" is exact, fast, and cannot be fooled by a class that overrides __eq__ to claim equality with None. Never rely on "is" for numbers or strings: small ints and interned strings may or may not be shared, that is an implementation detail.')
qa('qa-b-dictorder', 'Dictionary basics and ordering', 'Data types', 'Basic',
   'How do dicts work at a high level, and are they ordered? What can be a key?',
   'A dict is a hash table: the key is hashed to find where its value lives, giving average O(1) lookup, insert and delete. Keys must be hashable (immutable-like): str, int, float, tuple of hashables, frozenset. Lists, dicts and sets cannot be keys.\n\nSince Python 3.7 dicts keep insertion order as a language guarantee. Updating an existing key keeps its original position; deleting and re-adding moves it to the end.')
qa('qa-b-args', '*args and **kwargs', 'Functions', 'Basic',
   'What do *args and **kwargs do? Show how to call a function with a list and a dict unpacked.',
   'In a definition, *args collects extra positional arguments into a tuple and **kwargs collects extra keyword arguments into a dict. They let a function accept a flexible number of arguments.\n\ndef show(*args, **kwargs): print(args, kwargs)\nshow(1, 2, a=3) -> (1, 2) {"a": 3}\n\nIn a call, * unpacks an iterable into positional arguments and ** unpacks a dict into keyword arguments:\nnums = [1, 2]; opts = {"sep": "-"}; print(*nums, **opts) -> 1-2')
qa('qa-b-slicing', 'Slicing', 'Strings & lists', 'Basic',
   'Explain slicing syntax a[start:stop:step]. What do a[::-1], a[:], and a[-3:] give?',
   'a[start:stop:step] returns a new sequence from start (included) to stop (excluded), moving by step. Any part can be left out. Negative indexes count from the end. Slices never raise IndexError for out-of-range bounds; they are clipped.\n\na[::-1] is a reversed copy. a[:] is a shallow copy of the whole list. a[-3:] is the last three items.',
   code='a = [0, 1, 2, 3, 4, 5]\nprint(a[::-1], a[:], a[-3:], a[1:5:2])')
qa('qa-b-lcomp', 'List comprehension vs a for loop', 'Comprehensions', 'Basic',
   'What is a list comprehension and when should you avoid one?',
   'A list comprehension builds a list in one expression: [expr for x in items if cond]. It is usually shorter and a bit faster than a loop with append, and the result is built with no leftover loop variable.\n\nAvoid it when it needs several nested loops/conditions that hurt readability, when you only want side effects (use a plain for loop), or when the result is huge and you only iterate once (use a generator expression with parentheses so nothing is stored).')
qa('qa-b-pyvars', 'How Python variables work', 'Basics', 'Basic',
   'Explain "variables are names bound to objects". What happens on x = 5; y = x; x = 6?',
   'In Python a variable is a name that refers to an object; it is not a box holding a value. Assignment binds the name to an object. x = 5 binds x to the int 5, y = x binds y to the same object, x = 6 rebinds x to a different object, and y still refers to 5. Nothing was "copied" or "changed in place". With mutable objects the picture matters: y = x followed by x.append(1) changes the one shared list that both names see.')
qa('qa-b-exceptions', 'try / except / else / finally', 'Errors & exceptions', 'Basic',
   'What do else and finally do in a try statement?',
   'try runs the code that may fail. except handles a specific error. else runs only when the try block raised nothing, a good place for code that should not be covered by the except. finally always runs, error or not, even on return: use it for cleanup like closing files (or, better, use a with statement). Catch specific exceptions, not a bare except, which also hides KeyboardInterrupt and real bugs.')
qa('qa-b-with', 'The with statement', 'Files & context managers', 'Basic',
   'Why do we write "with open(path) as f:" instead of f = open(path)?',
   'with uses a context manager: on entering it gets the resource, on leaving the block (normally or through an exception) it releases it automatically. For files that means f.close() is guaranteed, so you do not leak file handles or lose buffered writes. Any object with __enter__ and __exit__ works, and contextlib.contextmanager lets you write one with a generator.')

# ---------------- Intermediate
qa('qa-i-mutdef', 'Mutable default argument bug', 'Functions', 'Intermediate',
   'What does this print, and why? How do you fix it?',
   'It prints [1], then [1, 2]. A default value is evaluated ONCE, when the def statement runs, and the same list object is reused by every call that omits the argument.\n\nFix: use None as the sentinel and create a fresh list inside:\n\ndef add(x, acc=None):\n    if acc is None:\n        acc = []\n    acc.append(x)\n    return acc',
   code='def add(x, acc=[]):\n    acc.append(x)\n    return acc\nprint(add(1))\nprint(add(2))')
qa('qa-i-copy', 'Shallow vs deep copy', 'Data types', 'Intermediate',
   'What is the difference between a shallow and a deep copy? When does it matter?',
   'A shallow copy (list.copy(), a[:], copy.copy) makes a new outer container but the items inside are the SAME objects. A deep copy (copy.deepcopy) recursively copies everything.\n\nIt matters with nested mutable objects: after b = a.copy() on [[1], [2]], b[0].append(9) also changes a[0], because both lists hold the same inner list. Use deepcopy when you need full independence. Beware of [[0] * 3] * 3: it makes three references to one row.')
qa('qa-i-gen', 'Generators and yield', 'Iterators & generators', 'Intermediate',
   'What is a generator and why use one instead of returning a list?',
   'A generator function contains yield. Calling it returns an iterator that produces values lazily: execution pauses at each yield and resumes on the next request, keeping local state. Benefits: constant memory for huge or infinite streams, work starts immediately, and values can be pipelined. Drawbacks: single pass (exhausted after one loop) and no indexing or len(). A generator expression (x*x for x in data) is the one-line form.')
qa('qa-i-iter', 'Iterable vs iterator', 'Iterators & generators', 'Intermediate',
   'What is the difference between an iterable and an iterator? What happens in a for loop?',
   'An iterable has __iter__ and can produce an iterator (lists, strs, dicts, files). An iterator has __next__ (returns the next item, raises StopIteration at the end) and __iter__ (returns itself). A for loop calls iter() on the iterable once, then calls next() repeatedly until StopIteration. Iterators are single-use and remember their position; iterables like lists can be looped many times because each loop gets a fresh iterator.')
qa('qa-i-decor', 'Decorators', 'Functions', 'Intermediate',
   'What is a decorator? Write the idea of one in a few lines and explain what functools.wraps is for.',
   'A decorator is a function that takes a function and returns a replacement, usually a wrapper adding behaviour (timing, logging, caching, auth). The @name syntax above a def is shorthand for f = name(f).\n\ndef timed(fn):\n    @functools.wraps(fn)\n    def wrapper(*a, **k):\n        t = time.perf_counter()\n        try: return fn(*a, **k)\n        finally: print(fn.__name__, time.perf_counter() - t)\n    return wrapper\n\nfunctools.wraps copies the original __name__, __doc__ and signature info onto the wrapper so debugging, help() and introspection still show the real function.')
qa('qa-i-closure', 'Closures and nonlocal', 'Functions', 'Intermediate',
   'What is a closure? What does nonlocal do?',
   'A closure is an inner function that remembers variables from the enclosing function after that function has returned. Example: make_counter returns an inner function that increments a variable of the outer scope. Reading outer variables just works; to REASSIGN one you must declare it nonlocal, otherwise Python treats the name as a new local and raises UnboundLocalError. Late binding gotcha: closures look up the variable when called, so lambdas created in a loop all see the last value unless you bind it (lambda i=i: i).')
qa('qa-i-ldeg', 'LEGB scope rule', 'Functions', 'Intermediate',
   'What is the LEGB rule?',
   'Python looks a name up in this order: Local (current function), Enclosing (outer functions), Global (module), Built-in. The first match wins. Assigning to a name inside a function makes it local for the whole function unless declared global or nonlocal. That is why reading a global then assigning it later in the same function raises UnboundLocalError.')
qa('qa-i-dunder', 'Dunder methods: __str__ vs __repr__', 'OOP', 'Intermediate',
   'What is the difference between __str__ and __repr__? What are __eq__ and __hash__ responsible for?',
   '__repr__ is the unambiguous developer representation (ideally something you could paste to rebuild the object); __str__ is the friendly one used by print() and str(). If only __repr__ exists, it is used for both. __eq__ defines ==; if you define __eq__ without __hash__, instances become unhashable. Objects that compare equal must have equal hashes, so define them together. @dataclass generates __init__, __repr__ and __eq__ for you.')
qa('qa-i-classstatic', '@classmethod vs @staticmethod', 'OOP', 'Intermediate',
   'Explain instance methods, classmethods and staticmethods.',
   'An instance method receives self, the instance. A classmethod receives cls, the class, so it works with subclasses; it is the usual way to write alternative constructors (Date.from_string). A staticmethod receives neither: it is just a plain function that lives in the class namespace for organisation.')
qa('qa-i-inherit', 'Inheritance, super() and MRO', 'OOP', 'Intermediate',
   'How does super() work and what is the MRO?',
   'The Method Resolution Order is the linear order Python searches for attributes through a class and its bases, computed by C3 linearisation (see Class.__mro__). super() returns a proxy that continues the search AFTER the current class in the MRO of the instance, so cooperative multiple inheritance works when every class calls super().__init__(...). It does not simply mean "my parent".')
qa('qa-i-setops', 'Sets', 'Data types', 'Intermediate',
   'When should you use a set? What are union, intersection and difference, and their cost?',
   'Use a set for fast membership tests (x in s is average O(1)), removing duplicates and comparing groups. a | b is union, a & b is intersection, a - b is difference (in a, not in b), a ^ b is symmetric difference. Elements must be hashable and the set is unordered. Building a set from n items is O(n). Turning a list lookup that happens repeatedly into a set lookup is a classic speed-up.')
qa('qa-i-complexity', 'Time complexity of common operations', 'Complexity', 'Intermediate',
   'Give the complexity of: list append, list insert(0, x), x in list, x in set, dict get, sorting, and string concatenation in a loop.',
   'list.append: amortised O(1). list.insert(0, x): O(n) because everything shifts (use collections.deque for O(1) both ends). x in list: O(n). x in set / dict get: average O(1). sorted/list.sort: O(n log n) (Timsort, stable). Repeated s += "x" in a loop can be O(n^2) in the worst case because strings are immutable; collect pieces in a list and "".join them at the end.')
qa('qa-i-sortstable', 'Sorting in Python', 'Sorting', 'Intermediate',
   'What is the difference between sorted() and list.sort()? What is a key function? Is the sort stable?',
   'list.sort() sorts in place and returns None; sorted() returns a new list from any iterable. Both are stable (equal items keep their original order) and use Timsort. key= is a function applied once per item to produce the value compared: sorted(words, key=len), key=lambda p: (p.age, p.name). reverse=True flips the order while keeping stability. Because it is stable you can sort by several keys by sorting repeatedly from the least to the most important.')
qa('qa-i-fstring', 'String formatting', 'Strings', 'Intermediate',
   'What are f-strings and what can go inside the braces?',
   'f-strings (Python 3.6+) evaluate expressions inside {} at runtime: f"{name} is {age + 1} next year". After a colon you give a format spec: {pi:.2f}, {n:,}, {x:>8}, {ratio:.1%}. {value!r} uses repr. {x=} prints both the expression and its value, handy for debugging. They are faster and more readable than % formatting and str.format.')

# ---------------- Advanced
qa('qa-a-gil', 'The GIL', 'Concurrency', 'Advanced',
   'What is the GIL, what does it limit, and how do you get parallelism in Python?',
   'The Global Interpreter Lock lets only one thread execute Python bytecode at a time in CPython, which protects interpreter internals (like reference counts). Effect: threads do not speed up CPU-bound pure-Python code. They DO help I/O-bound work because the lock is released while waiting on the network, disk or sleep.\n\nFor CPU-bound work use multiprocessing / concurrent.futures.ProcessPoolExecutor (separate processes), native extensions that release the GIL (NumPy), or compiled code. For many concurrent I/O tasks asyncio is lighter than threads. Recent CPython versions also offer an experimental free-threaded build, so check what your version supports.')
qa('qa-a-async', 'asyncio basics', 'Concurrency', 'Advanced',
   'How does async/await work? How is it different from threading?',
   'asyncio runs many coroutines on one thread with an event loop. A coroutine (async def) runs until it hits await on something that is not ready (a network call, asyncio.sleep); then it hands control back to the loop, which runs another coroutine. It is cooperative: a coroutine that never awaits (or does blocking work such as time.sleep or heavy CPU) freezes everyone. Threads are pre-emptive and the OS switches them; asyncio switches only at await points, so there are fewer race conditions and lower overhead, but you need async-aware libraries. Use asyncio.gather to run several awaitables concurrently and asyncio.to_thread for unavoidable blocking calls.')
qa('qa-a-gc', 'Memory management and garbage collection', 'Internals', 'Advanced',
   'How does CPython manage memory?',
   'CPython uses reference counting: each object stores how many references point to it and is freed immediately at zero. Reference counting cannot free cycles (a list that contains itself), so a generational cyclic garbage collector periodically finds and frees unreachable cycles (gc module). Small objects are served from pymalloc arenas, and some (small ints, interned strings, None) are shared. Weak references (weakref) refer to an object without keeping it alive, useful for caches. Objects with __del__ are not a reliable cleanup mechanism; use context managers.')
qa('qa-a-slots', '__slots__', 'OOP', 'Advanced',
   'What does __slots__ do and what are the trade-offs?',
   'By default each instance stores attributes in a per-instance __dict__. Declaring __slots__ = ("x", "y") replaces that dict with fixed slots, which cuts memory a lot when you create millions of small objects and slightly speeds attribute access. Trade-offs: you cannot add attributes outside the list, there is no __dict__ or weakref support unless you list them, and inheritance and multiple inheritance with slots need care.')
qa('qa-a-meta', 'Metaclasses and descriptors', 'OOP', 'Advanced',
   'What is a metaclass? What is a descriptor? Give a real use of each.',
   'Everything is an object, including classes; a class is an instance of its metaclass (type by default). A metaclass customises class creation: registering subclasses automatically, validating class bodies, building ORMs. Often a class decorator or __init_subclass__ is simpler.\n\nA descriptor is an object with __get__ / __set__ / __delete__ placed as a class attribute; attribute access on instances calls them. Properties, methods (functions are descriptors that bind self), classmethod, staticmethod and many ORM fields are built on this.')
qa('qa-a-ctxmgr', 'Writing a context manager', 'Files & context managers', 'Advanced',
   'How can you write your own context manager? Show both ways.',
   'Class way: define __enter__(self) (returns the value bound by as) and __exit__(self, exc_type, exc, tb); returning True from __exit__ suppresses the exception.\n\nGenerator way:\n\nfrom contextlib import contextmanager\n@contextmanager\ndef timer():\n    t = time.perf_counter()\n    try:\n        yield\n    finally:\n        print(time.perf_counter() - t)\n\nCode before yield is __enter__, code after (in finally) is __exit__. Use try/finally so cleanup runs when the body raises.')
qa('qa-a-typing', 'Type hints', 'Typing', 'Advanced',
   'What do type hints do at runtime? Name a few useful typing tools.',
   'At runtime almost nothing: the interpreter stores annotations but does not enforce them. Their value is for tools (mypy, pyright), editors and documentation, and for libraries that read them (dataclasses, pydantic, FastAPI). Useful pieces: list[int], dict[str, int], X | None (Optional), Callable, Iterable, Protocol (structural typing), TypedDict, Literal, Generic and TypeVar. Gradual typing means you can add hints piece by piece.')
qa('qa-a-dataclass', 'dataclasses', 'OOP', 'Advanced',
   'What does @dataclass generate? Mention frozen, field(default_factory=...) and ordering.',
   '@dataclass writes __init__, __repr__ and __eq__ from the annotated fields. frozen=True makes instances immutable (and hashable), order=True generates comparison methods using field order, slots=True adds __slots__. A mutable default like a list is not allowed directly; use field(default_factory=list) so each instance gets its own. __post_init__ runs after __init__ for validation and derived fields.')
qa('qa-a-profile', 'Making slow Python fast', 'Performance', 'Advanced',
   'Your Python code is slow. What is your process?',
   '1) Measure first: cProfile / py-spy / timeit, find the real hot spot. 2) Fix the algorithm or data structure (set or dict lookup instead of list scan, avoid O(n^2), heapq, bisect, deque). 3) Use built-ins and comprehensions, which run in C, move work out of inner loops, cache with functools.lru_cache. 4) Vectorise with NumPy or pandas, or batch I/O. 5) For CPU-bound parallel work use multiprocessing; for I/O-bound use asyncio or threads. 6) Only then consider Cython, Numba or rewriting hot code in a compiled language.')
qa('qa-a-copyonwrite', 'Hashing and dict internals', 'Internals', 'Advanced',
   'Why must dict keys be hashable and what happens on a hash collision?',
   'A dict finds a slot from hash(key). Two keys with the same hash (or landing in the same slot) are a collision; CPython uses open addressing with probing and then compares keys with == to find the right entry. The hash must never change while the key is in the table, so mutable containers are not allowed as keys. Lookup is average O(1) but degrades toward O(n) with many collisions, which is why hash functions try to spread values and why Python randomises str hashes per process (hash-flooding protection).')
qa('qa-a-gensend', 'Generators: send, close, yield from', 'Iterators & generators', 'Advanced',
   'What do generator.send(), yield from and return inside a generator do?',
   'yield is also an expression: gen.send(value) resumes the generator and the paused yield evaluates to value (prime it first with next()). yield from other delegates to a sub-iterator and passes through sent values and exceptions, and its value is the sub-generator return value. return x inside a generator ends it with StopIteration(x). gen.close() raises GeneratorExit at the paused yield so finally blocks run. These form the basis of the older coroutine design that async/await later replaced.')
qa('qa-a-test', 'Testing with pytest', 'Testing', 'Advanced',
   'How do you test Python code? Mention fixtures, parametrization and mocking.',
   'pytest finds test_*.py files and functions and uses plain assert with rich failure output. Fixtures (@pytest.fixture) provide set-up and tear-down and are injected by argument name. @pytest.mark.parametrize runs one test over many inputs. Mock external services or time with unittest.mock.patch / monkeypatch so tests are fast and deterministic. Test behaviour through public interfaces, keep tests independent, and measure coverage with pytest-cov as a guide rather than a goal.')
