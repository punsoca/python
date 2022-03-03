'''
This code is a mofification of a sample code from https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example
I wanted to modify the code to allow for the following:
- specify the thread_name_prefix parameter in the ThreadPoolExecutor() class
- use 'threading.currentThread().getName() to get the name for each thread within the 'load_url' threading function
- pass the thread name back to the main function so we can accurately display the thread name
- move the try-except logic to the thread function 'load_url' 
- return (thread name, url, url contents, and exception message) values as a tuple back to main function as our future.result() per url processed
'''


from threading import currentThread
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://www.bbc.co.uk/',
        'http://europe.wsj.com/',
        'http://some-made-up-domain.com/'
        ]

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    try:
        # if urllib.request read URL success then pass url contents (conn.rread()) as 3rd parameter and the 4th parameter is set to None
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            return url, currentThread().getName(), conn.read(), None
    except Exception as exc:
        # if urllib.request read URL FAILED then pass exception message (exc) as the 4th parameter and set 3rd parameter to None
        return url, currentThread().getName(), None, exc

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5, thread_name_prefix='url_thread') as executor:
    futures = (executor.submit(load_url, url, 60) for url in URLS)
    for future in concurrent.futures.as_completed(futures):
        # break down the tuple to its individual parts
        url, thread_name, data, exc = future.result()

        if exc:
            print(f'Thread Name {thread_name}: {url} generated an exception {exc}')
        else:
            print(f'Thread Name {thread_name}: content length of {url} = {len(data)} bytes')
