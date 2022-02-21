'''
    MULTI-PROCESSING USING 'concurrent.futures.ProcessPoolExecutor()

    Using concurrent_futures to process multiple images at once

    NOTE:
    This module also demonstrates the use of pathlib.Path library T specify path:
    - use Path() object use this instead of "os.path":
    - use Path.mkdir() method to create folders

'''
import concurrent.futures
from pathlib import Path
import time

from PIL import Image, ImageFilter

# note - images should have already been downloaded with the thread-images.py script
source = Path("images")
img_names = [
    'photo-1516117172878-fd2c41f4a759.jpg',
    'photo-1532009324734-20a7a5813719.jpg',
    'photo-1524429656589-6633a470097c.jpg',
    'photo-1530224264768-7ff8c1789d79.jpg',
    'photo-1564135624576-c5c88640f235.jpg',
    'photo-1541698444083-023c97d3f4b6.jpg',
    'photo-1522364723953-452d3431c267.jpg',
    'photo-1513938709626-033611b8cc03.jpg',
    'photo-1507143550189-fed454f93097.jpg',
    'photo-1493976040374-85c8e12f0c0e.jpg',
    'photo-1504198453319-5ce911bafcde.jpg',
    'photo-1530122037265-a5f1f91d3b99.jpg',
    'photo-1516972810927-80185027ca84.jpg',
    'photo-1550439062-609e1531270e.jpg',
    'photo-1549692520-acc6669e2f0c.jpg'
]

output_folder = 'processed_images'
size = (1200, 1200)


def create_dir_if_not_exist(folder):
    Path(folder).mkdir(parents=True, exist_ok=True) # preferred for python3.6 and over

def process_image(img_name):
    img = Image.open(source/img_name)

    img = img.filter(ImageFilter.GaussianBlur(15))

    img.thumbnail(size)
    img_file = f'{output_folder}/{img_name}'
    img.save(img_file)
    print(f'{img_name} was processed...')

# decorator function 'funcname' is created solely for the purpose of printing the name of the decorated function as it executes
def funcname(func):
    def wrapper_function(*args, **kwargs):
        print(f'\n... Executing Function "{func.__name__}()" ...\n')
        func(*args, **kwargs)
        print(f'\n... Function "{func.__name__}()" completed!\n')

    return wrapper_function

@funcname
def concurrent_futures_process_pool_submit():
    t1 = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for img in img_names:
            executor.submit(process_image, img)

    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())

    t2 = time.perf_counter()
    print(f'concurrent futures using ProcessPoolExecutor - Finished in {t2-t1} seconds')

@funcname
def concurrent_futures_process_pool_map():
    t1 = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image, img_names)

    t2 = time.perf_counter()
    print(f'concurrent futures using ProcessPoolExecutor - Finished in {t2-t1} seconds')

if __name__ == '__main__':

    create_dir_if_not_exist(output_folder)

    # concurrent_futures_process_pool_submit()

    concurrent_futures_process_pool_map()
