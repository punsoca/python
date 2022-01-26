import json

def open_json_file(filename):
    try:
        with open(filename) as f:
            try:
                return json.load(f)
            except ValueError as val_error:
                raise ValueError('{} is not valid JSON.'.format(filename)) from val_error
    except IOError as io_error:
        raise IOError('{} does not exist.'.format(filename)) from io_error
