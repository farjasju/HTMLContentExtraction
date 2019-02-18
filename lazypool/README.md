# lazypool

## What
thread pool executor that lazily maps over your iterable

## Why

Both `multiprocessing` pools and `concurrent.futures` executors have a problem where if you try to map them over some iterable,
they want to load that entire iterable into an internal queue for the threads to pull off of.
This is undesirable in cases where the individual items are particularly memory intensive,
or the iterable itself is infinite, and you're doing something like stream processing.

So in the finest tradition of my people, I decided to write my own thread pool,
one that would only load each item as it was ready to be worked on.

"Lazy" is probably a bit of a misnomer.
In terms of actually doing work, it's actually very not-lazy, and will start delegate items to worker threads as soon as you call `map`.

## How

```python

import itertools
from lazypool import LazyThreadPoolExecutor

stream = itertools.count(0)

def work(num):
  return num + 1

pool = LazyThreadPoolExecutor(4) # 4 threads
results = pool.map(work, stream)

# work has begun

for r in results:
  print r # print some numbers >= 1, not necessarily in order
```

Also see [examples.py](examples.py) for slightly more usage.
