import time
import contextlib

@contextlib.contextmanager
def profile(msg='operation'):
    try:
        s = time.time()
        yield
    finally:
        e = time.time()
        print('{} cost time: {}'.format(msg, e - s))
    
if __name__ == '__main__':
    with profile():
        time.sleep(3)