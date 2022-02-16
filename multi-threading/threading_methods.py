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

def do_futures(seconds):
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
@funcname
def call_func_twice_no_threading():
    '''
    calling the function twice result in the process running for a whole two seconds - this is because this code waits for
    the first function call to complete before executing the function the second time (total of 2 seconds execution time)

    '''

    start = start_timer()

    # calls do_something function twice
    do_something()
    do_something()

    print(f'{total_time(start)}\n')

# --------------------------------- 2.  execute a function using threading ---------------------------------
@funcname
def run_two_threads_async():
    '''
        use python threading to run concurrent functions faster - instead of running the do_something function twice in a row, lets
        instead turn these into threads.

        this requires the 'import threading' statement and executes the .start()
    '''

    start = start_timer()
    # define the two threads - pass the function name we wish to execute to the 'target' parameter
    t1 = threading.Thread(target=do_something)
    t2 = threading.Thread(target=do_something)

    # to run the thread objects  we need to do a start() method on each thread
    # EXPECTATION: The function executes 'Finish executing' print statement  as soon as 't1.start()' and 't2.starts()' are executed
    # WITHOUT WAITING FOR COMPLETION OF  t1 and t2 thread execution.  Execution time is ZERO seconds.

    t1.start()
    t2.start()

    # the following line with be printed even while our thread are in sleep mode
    print('Finish executing our two threads')
    print(f'{total_time(start)}\n')
    time.sleep(3)

# --------------------------------- 3.  execute threading function with .join() method ---------------------------------
@funcname
def run_two_threads_with_join():
    '''
        use the '.join()' method to instruct the threading function to finish execution before moving on
        to the rest of the script.

    '''
# Requirement:  this requires the 'import threading' statement to execute do_something(). This multi-threading function
# uses the Thread.join() in addition to Thread.start().  Expected total execution time for both threads is ~1 second.
#
# Unlike the run_two_threads_async() function - this time, with the Thread.join() method implemented, python waits for
# the completion of the two threads before it runs the "Finishing executing..." and printing total execution time.
#

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
    '''
        This function runs 10 THREADS asynchronously USING for-loop - this is a better way to create multiple threads, 
        BUT this requires the multiple threads to be added to a thread list, with the explanation provided in the code 
        comments below.
    '''

    start = start_timer()
    threads = []

    # create 10 threads within our for- loop
    for _ in range(10):
        t = threading.Thread(target=do_something)
        # every time a thread is created, it should be started by calling  .start() method on the thread object
        t.start()

        # NOTE: You CANNOT put a "t.join()" within the same for-loop as the "t.start()", threads would behave as if they are run synchronously!
        # When creating thread using a loop, we need to create a thread list and join each thread to the list.
        threads.append(t)

    # after the threads are added to the thread list, we need a SEPARATE for- loop to execute the .join() method for each thread in the
    # thread list.  Doing this allows python to WAIT UNTIL ALL THREADS ARE COMPLETED before python runs the "total_time" print statement.
    for thread in threads:
        thread.join()

    print(f'{total_time(start)}\n')

# BEGINNING PYTHON 3.2, the 'concurrent.futures' can be used in place of threading without the need to do a .start()
# and join() on inividual threads.
# ------------------------------------------ 5.  using concurrent futures --------------------------------------------

@funcname
def conc_futures_threading():
    '''
        Create and execute multitheading using 'concurrent.futures.ThreadPoolExecutor'. The concurrent.futures module
        provides a high-level interface for asynchronously executing callables. The asynchronous execution can be
        performed with threads, using `ThreadPoolExecutor` subclass.

        - there is no need to specify thread.start() and thread.join()
        - Executor is an abstract class that provides methods to execute calls ASYNCHRONOUSLY
        - Executor object uses submit() method to schedule the callable
        - requires to call executor.shutdown() with no args - this will wait for the futures to complete

        Note on ThreadPoolExecutor's "max_workers" argument:
            ThreadPoolExecutor() provides a max_worker argument which provides us with a pool of X threads to
            execute calls ASYNCHRONOUSLY.  If max_worker=None or not provided, python will set the thread number
            to os.cpu_count().  As of Python3.8, it sets the number to os.cpu_count() + 4, or 32, whichever is lower.

        This function run 5 THREADS with varying seconds - longest is 2 seconds. The ThreadPoolExecutor is provided
        with "max_workers=None".  Each executor.submit() method (10 in all) creates a future object, calls the "do_futures"
        function along with the time.sleep() value for each future object.


    '''
    start = start_timer()

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=None)
    f1 = executor.submit(do_something2, 0.5)
    f2 = executor.submit(do_something2, 1.25)
    f3 = executor.submit(do_something2, 1.50)
    f4 = executor.submit(do_something2, 1.75)
    f5 = executor.submit(do_something2, 2)

    executor.shutdown()

    print(f1.result())
    print(f2.result())
    print(f3.result())
    print(f4.result())
    print(f5.result())


    print(f'{total_time(start)}\n')

# ----------------------- 6.  write concurrent futures ThreadPool as context manager  -----------------------
@funcname
def conc_futures_thrd_context_mgr():
    '''
        When written as context manager "with ThreadPoolExecutor()", there is no need to code for shutdown(),
        as the context manager includes IMPLICIT "shutdown()" call, which waits for the futures to complete
        before the executor shuts down.
    '''

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

# ------------------ 7.  using concurrent futures to run mutiple threads with as_completed ------------------
@funcname
def conc_futures_thrd_as_completed():
    '''
        This function uses the concurrent.futures 'as_completed()' method. It is implemented in the for- loop 
        where the results are to be printed in the order "as they are completed". 
        
        Meanwhile, the executor.submit is written differently, this time as a list comprehension, with the
        number of futures objects equal to the length of the secs list - "secs" list contains the list of numbers
        corresponds to the time.sleep() value for each future object that the executor.submit() creates in the 
        ist cmprehension.

    '''

    start = start_timer()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1, 2, 3 ,4, 1, 5]
        results = [executor.submit(do_futures, sec) for sec in secs]

        for f in concurrent.futures.as_completed(results):
            print(f.result())

    print(f'{total_time(start)}\n')

# -------------------------------------  8. threading pool executor using executor.map  ------------------------------
@funcname
def conc_futures_thrd_with_executor_map():
    '''
        Using concurrent_futures.ThreadPoolExecutor executor map():
        
        The 'executor.map()' replaces the 'executor.submit()', and the syntax follows closely to the regular map() function.  
        
        In the meantime, for- loop for displaying the thread results show each thread result  is displayed in the order it was started.

    '''

    start = start_timer()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [5, 4, 3, 2, 1, 2, 3 ,4, 1, 5]
        results = executor.map(do_futures, secs)

        for result in results:
            print(result)

    print(f'{total_time(start)}\n')


# --------------------------- 9. threading pool executor using max_workers args passed ------------------------------
@funcname
def conc_futures_thrd_with_max_workers(max_workers):
    '''
        Use concurrent_futures.ThreadPoolExecutor executor map().  For this function, we are passing the 
        ""max_workers" argument to the executor object.

        NOTE :
        The speed in which this function is executed is DEPENDENT ON the 'max_workers' value (if passed as an argument).
        By default, NOT PROVIDING the "max_workers" argument would produce faster result
    '''

    start = start_timer()
    print(f'\n{max_workers = }\n')

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        secs = [5, 4, 3, 2, 1, 2, 3 ,4, 1, 5]
        results = executor.map(do_futures, secs)

        for result in results:
            print(result)

    print(f'{total_time(start)}\n')

if __name__ == '__main__':

    # This program shows the different ways to create multi-threading function (except for 'call_func_twice_no_threads').
    # Each function shows the total time of execution.

    # calling a function twice normally with no threading
    call_func_twice_no_threading()                     # regular function call - function called twice

    ### following three functions use threading.Thread
    run_two_threads_async()                            # running one function concurrently using two threads with start() only
    run_two_threads_with_join()                        # run a function concurrently with two threads using start() and join()
    run_ten_threads_with_threadlist()                  # threading running 10 threads asynchronously using thread list

    ### the recommended way to do threading is to use concurrent.futures.ThreadPoolExecute, with four examples as shown below:
    conc_futures_threading()                            # basic concurrent.futures.ThreadPool
    conc_futures_thrd_context_mgr()                     # writing concurrent.futures.ThreadPool as context manager
    conc_futures_thrd_as_completed()                    #  concurrent.futures ThreadPoolExecutor() using as_completed()
    conc_futures_thrd_with_executor_map()               # concurrent.futures ThreadPoolExecutor() using executor.map()
    conc_futures_thrd_with_max_workers(5)               # concurrent.futures ThreadPoolExecutor() passing max_workers argument
