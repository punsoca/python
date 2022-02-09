# this module is created based on the python threading lesson from https://www.youtube.com/watch?v=IEEhzQoKtQU
# note that the recommended way to do multithreading is to use concurrent.futures (avaiable begining Python3.2)

import concurrent.futures
import threading
import time

# timer functions
def start_timer():
    return time.perf_counter()

def total_time(started):
    finished = time.perf_counter()
    return f'Total execution time is {round(finished-started,2)} second(s)'

# the do_xxxxxxxx functions use time.sleep to test the different multi-threading methods 
def do_something():
    print('Sleeping one second...')
    time.sleep(1)
    print('Done sleeping.')

def do_something2(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done sleeping {seconds} seconds.'

def do_thread_concurrent_futures(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done sleeping {seconds} seconds.'

# decorator function 'funcname' to print the name of the decorated function
def funcname(func):
    def wrapper_function(*args, **kwargs):
        print(f'\n... Function "{func.__name__}()" ...')
        return func(*args, **kwargs)

    return wrapper_function   # function without () indicates returning the function as an argument without executing it



# ALL eight (8) multi-threading methods are decorated with @funcname
# --------------------------------- 1. call function twice without threading ---------------------------------
# calling the function twice result in the process running for a whole two seconds - this is because this code waits for
# the first function call to complete before executing the function the second time (total of 2 seconds execution time)
@funcname
def call_func_twice_no_threading():

    start = start_timer()

    # calls do_something function twice 
    do_something()
    do_something()

    print(f'{total_time(start)}\n')

# --------------------------------- 2.  execute a function using threading ---------------------------------
# use python threading to run concurrent functions faster - instead of running the do_something function twice in a row, lets
# instead turn these into threads
@funcname
def run_two_threads_async():
# Requirement:  this requires the 'import threading' statement and execute the .start() and .join() methods.

    start = start_timer()
    # define the two threads - pass the function name we wish to execute to the 'target' parameter
    t1 = threading.Thread(target=do_something)
    t2 = threading.Thread(target=do_something)

    # to run the thread objects  we need to do a start() method on each thread
    # EXPECTATION: The function executes 'Finish executing' print statement  as soon as 't1.start()' and 't2.starts()' are executed
    # while t1 and t2 threads are in sleep mode - WITHOUT WAITING FOR COMPLETION OF  t1 and t2 thread execution.

    t1.start()
    t2.start()

    # the following line with be printed even while our thread are in sleep mode
    print('Finish executing our two threads')
    print(f'{total_time(start)}\n')
    time.sleep(3)

# --------------------------------- 3.  execute threading function with .join() method ---------------------------------
# use the '.join()' method to instruct the threading function to finish execution before cmoving on to the rest of the script.

@funcname
def run_two_threads_with_join():
# Requirement:  this requires the 'import threading' statement and execute the .start() and .join() methods
# each thread has a sleep delay of TWO SECONDS

    start = start_timer()
    # define the two threads - pass the function name we wish to execute to the 'target' parameter
    t1 = threading.Thread(target=do_something)
    t2 = threading.Thread(target=do_something)

    # to run the thread objects  we need to do a start() method on each thread
    # EXPECTATION: Finish time still 0 seconds because python started both threads and while the threads are sleeping, our script ran
    # .............concurrently and continued on with the rest of the script - immediately coming down and calculate our finish time.
    t1.start()
    t2.start()

    # use the threading 'join()' method to specify that we want our threads to finish before contiuing running the rest of the script
    t1.join()
    t2.join()

    print('Finish executing our two threads with .join() method')
    print(f'{total_time(start)}\n')
    time.sleep(2)

# --------------------------------- 4. using a thread list to run multiple threads asynchronously ---------------------------------
@funcname
def run_ten_threads_with_threadlist():
    # running 10 THREADS asynchronously - each thread has a ONE SECOND sleep funcname

    # Similar to above, but add each thread to a thread list and loop thru the thread to do .join() instead of coding individually per thread
    # - create a for loop to do the following: create and start each thread, then append each thread to a thread list
    # - create another for- loop to loop thru the created thread list to allow ALL threads to run asynchronously and completed
    #   before executing the next line in the script.

    start = start_timer()
    threads = []

    # create 10 threads within our for- loop
    for _ in range(10):
        t = threading.Thread(target=do_something)
        # every time a thread is created, it should be started by calling  .start() method on the thread object
        t.start()

        # we cannot put a "t.join()" within the same for-loop as the "t.start()", because this would just start and complete one thread per loop
        # which is similar to running one thread at a time.  The correct way is that after the multi-threads have been created and started, append
        # these threads into a thread list
        threads.append(t)

    # after the multiple threads are added to the thread list, create another for- loop through the thread list and run the join() method
    # on each thread to ensure that these threads can run concurrently, and allow all threads to finish running before executing the
    # next line in the script.
    for thread in threads:
        thread.join()

        # print(total_time(start))
    print(f'{total_time(start)}\n')

# BEGINNING PYTHON 3.2, the 'concurrent.futures' can be used in place of threading without the need to do a .start()
# and join() on inividual threads.
# ------------------------------------------ 5.  using concurrent futures --------------------------------------------
#
# run 5 THREADS with varying seconds - longest is 2 seconds
@funcname
def concurrent_threading_basic():
    # Requirement:  This function uses 'concurrent.futures.ThreadPoolExecutor' with executor.submit()

    start = start_timer()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(do_something2, 0.5)
        f2 = executor.submit(do_something2, 1.25)
        f3 = executor.submit(do_something2, 1.50)
        f4 = executor.submit(do_something2, 1.75)
        f5 = executor.submit(do_something2, 2)

        print(f1.result())
        print(f2.result())
        print(f3.result())
        print(f4.result())
        print(f5.result())


    print(f'{total_time(start)}\n')

# ------------------ 6.  using concurrent futures to run mutiple threads with as_completed ------------------
# use do_thread_concurrent_futures function with the DEFAULT max_workers value assigned by python
# this function uses the 'as_completed()' function which  prints the thread results in the order they are completed

@funcname
def concurrent_thread_as_completed():

    start = start_timer()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1, 2, 3 ,4, 1, 5]
        results = [executor.submit(do_thread_concurrent_futures, sec) for sec in secs]

        for f in concurrent.futures.as_completed(results):
            print(f.result())

    print(f'{total_time(start)}\n')

# -------------------------------------  7. threading pool executor using executor.map  ------------------------------
# use concurrent_futures.ThreadPoolExecutor executor map()
# with executor.map, it will return the results in the order that they were started, NOT the order as they completed

# NOTE 1:
# the executor.map() function in itself does not wait for all threads to complete, but writing the executor.map() within
# a context manager  ensures that all threads are completed before python executes the rest of the script

# NOTE 2:
# The speed in which this function is executed is DEPENDENT ON the 'max_workers' value provided
# by default, NOT PROVIDING the "max_workers" argument would produce faster result
@funcname
def conc_future_thrd_with_executor_map():

    start = start_timer()


    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1, 2, 3 ,4, 1, 5]
        results = executor.map(do_thread_concurrent_futures, secs)

        for result in results:
            print(result)

    print(f'{total_time(start)}\n')


# --------------------------- 8. threading pool executor using max_workers args passed ------------------------------
# use concurrent_futures.ThreadPoolExecutor executor map()
# with executor.map, it will return the results in the order that they were started, NOT the order as they completed

# NOTE :
# The speed in which this function is executed is DEPENDENT ON the 'max_workers' value (if passed as an argument).
# By default, NOT PROVIDING the "max_workers" argument would produce faster result

@funcname
def conc_future_thrd_with_max_workers(max_workers):

    start = start_timer()
    print(f'\n{max_workers = }\n')

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        secs = [5, 4, 3, 2, 1, 2, 3 ,4, 1, 5]
        results = executor.map(do_thread_concurrent_futures, secs)

        for result in results:
            print(result)

    print(f'{total_time(start)}\n')

if __name__ == '__main__':
    # calling a function twice normally with no threading 
    call_func_twice_no_threading()                         

    ### following three functions use threading.Thread
    run_two_threads_async()                            # calling a function twice using basic threading and running asynchronously
    run_two_threads_with_join()                 # calling a function twice using basic threading and running asynchronously
    run_ten_threads_with_threadlist()           # threading running 10 threads asynchronously using thread list

    ### the recommended way to do threading is to use concurrent.futures.ThreadPoolExecute, with four examples as shown below:
    concurrent_threading_basic()                # basic concurrent.futures.ThreadPool with 'executor.submit()'
    concurrent_thread_as_completed()            # use multithreading with concurrent.futures ThreadPoolExecutor() and as_completed()
    conc_future_thrd_with_executor_map()       # use multithreading with concurrent.futures ThreadPoolExecutor() and executor.map()
    conc_future_thrd_with_max_workers(5)       # use multithreading with concurrent.futures ThreadPoolExecutor() passing max_workers arg
