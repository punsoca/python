'''
    MULTI-PROCESSING USING 'concurrent.futures.ProcessPoolExecutor() that create worker processes.
    Will provide examples of process pool  wait() and shutdown() examples in a separate module.

    This module shows two ways to use the ProcessPoolExecutor:
    - function "concurrent_futures_process_pool_submit()" uses  'executor.submit()'
    - function "concurrent_futures_process_pool_map()")   uses  'executor.map()'

    Run this module - it will create a 'blurred_image' folder, apply Gaussian blur to each
    of the 15 images and save them into the blurred_image folder with the same name.  Total
    execution time for both execute.submit() and execute.map() are almost identical (total runtime
    of  just ~3 seconds when running it on Mac 2020 with os.cpu_count of 12).


    Miscellaneous:
    --------------
    This module uses pathlib.Path library to specify file path:
        - use Path() object instead of "os.path"
        - use Path.mkdir() method to create folders

    It also uses the PIL.image() and PIL.ImageFilter()  to process image files


'''
import concurrent.futures
from pathlib import Path
import time

from PIL import Image, ImageFilter

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

# specify the path of the source and destination images
fp = (Path(__file__).parent)
source = Path(fp/"orig_images")
destination = f'{fp}/blurred_images'

# specify thumbnail size of the images for preview
size = (1200, 1200)

def process_image(img_name):
    '''
    This method blurs the original images and saves them to the blurred_images folder with the same name
    '''
    img = Image.open(f'{source}/{img_name}')
    # apply Gaussian Blur on an image and specify the thumbnail size for previewing image
    img = img.filter(ImageFilter.GaussianBlur(15))
    img.thumbnail(size)

    # write the blurred Image object "img" to destination file
    dest_file = f'{destination}/{img_name}'
    img.save(dest_file)

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
    """
        This  function uses ProcessPoolExecution's submit() method
    """
    t1 = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for img in img_names:
            executor.submit(process_image, img)

    t2 = time.perf_counter()
    print(f'concurrent futures using ProcessPoolExecutor - Finished in {t2-t1} seconds')

def create_destination_folder():
    # create "blurred_images" folder on same path as python script
    Path(destination).mkdir(parents=True,exist_ok=True)

@funcname
def concurrent_futures_process_pool_map():
    """
        This  function uses ProcessPoolExecution's map() method
    """
    t1 = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image, img_names)

    t2 = time.perf_counter()
    print(f'concurrent futures using ProcessPoolExecutor - Finished in {t2-t1} seconds')

if __name__ == '__main__':

    create_destination_folder()

    # run concurrent_futures two ways:
    concurrent_futures_process_pool_submit() # concurrent.futures process pool executor method 1
    concurrent_futures_process_pool_map()    # concurrent.futures process pool executor method 1
