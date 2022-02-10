import json
import pickle

# saving json data to a file
def save_movie_json_data(fname, data):
    with fname.open('w') as f:
        # MAKE SURE TO PASS PARAMETER 'ensure_ascii=False' IN json.dump()
        json.dump(data, f, ensure_ascii=False, indent=4)

# loading json data from a file
def load_movie_json_data(fname):
    with fname.open() as f:
        # MAKE SURE TO PASS PARAMETER 'ensure_ascii=False' IN json.dump()
        return json.load(f)

# saving  data to a pickle file
def save_movie_pickle_data(fname, data):
    with open(fname, 'wb') as f:
        pickle.dump(data, f)

# loading data from a pickle file
def load_movie_pickle_data(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)
