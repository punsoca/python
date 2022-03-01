'''
    Despite the built-in GIL for multi-threading, when running multi-threading
    you may have objects shared between threads. Even if one thread is active
    at one time (due to GIL), other threads may have access to the object.

    This is where threading.Lock() comes into play. Using threading.Lock() avoids
    an object being accessed by another thread when one thread is using it.

    This demo shows the result of shared_value1 with NO threading.Lock() applied,
    and the shared_value2 with threading.Lock() applied. 


'''
from threading import current_thread, Lock, Thread
import time

shared_value1 = 0
shared_value2 = 0


def increment_value_no_lock():
    '''
       this function attempts to increment the global variable shared_value1.
       when thread #1 hits the time.sleep(0.1), thread 2 starts executing the
       same function, with shared_value1 still equal to zero, so the end value
       of shared_value would be 1, not the expected value of 2.

    '''
    global shared_value1
    value_copy = shared_value1
    value_copy += 1
    time.sleep(0.1)

    # assigning a value TO a global variable turns it into a local variable
    # hence,  we need to declare the global variable in the first line of this function
    shared_value1 = value_copy


def increment_val_with_lock(lock):

    '''
       this function attempts to increment the global variable shared_value2.
       This time, we put a Thread.Lock() on the function so thread #2 would NOT
       be able to access object shared_value2 thread #1 is finished with it.
       With the thread lock in place, by the time thread #2 accesses this function,
       the shared_value2 already equals to 1, and thread #2 is able to update the
       shared_value2 to 2 after the increment.
    '''
    global shared_value2

    # apply lock.acquire() and lock.release() at the beginning and end of
    # the code segment,  respectively

    lock.acquire()
    value_copy = shared_value2
    value_copy += 1
    time.sleep(0.1)
    shared_value2 = value_copy
    lock.release()

    '''
    Note that you could rewrite the thread lock more "elegantly" using the "with lock" conditional 
    statement, without the need for lock.acquire() and lock.release() (as the "with lock" will 
    handle them automatically) - just indent the codes under the with lock conditional as shown below.

            with lock:
                value_copy = shared_value2
                value_copy += 1
                time.sleep(0.1)
                shared_value2 = value_copy

    '''


def multi_functions(lock):
    increment_value_no_lock()
    print(f" increment_value_no_lock():   {current_thread().name}:  {shared_value1 = }")

    increment_val_with_lock(lock)
    print(f" increment_val_with_lock:  {current_thread().name}:  {shared_value2 = }")



thread_lock = Lock()
t1 = Thread(target=multi_functions, args=(thread_lock,))
t2 = Thread(target=multi_functions, args=(thread_lock,))
t1.start()
t2.start()
t1.join()
t2.join()
