import itertools
import threading

from lazypool import LazyThreadPoolExecutor


print_lock = threading.Lock()
def p(x):
    with print_lock:
        print x

finite = range(5)
infinite = itertools.count(0)

def work(num):
    p("WORKING in thread {0}".format(threading.current_thread()))
    p(num)
    return "a result"


pool = LazyThreadPoolExecutor(4)
results = pool.map(work, finite)

p("iterate over finite results")
p(list(results))


results = pool.map(work, infinite)

p("iterate over infinite results")
for i, r in enumerate(results):
    p(r)
    if i > 3:
        p("you get the idea...")
        break

pool.shutdown()

print "done"
