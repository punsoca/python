# Wikipedia links:
# ========================
# (1) url1 = Toy Story 3
# https://en.wikipedia.org/wiki/Toy_Story_3
#
# (2)) url2 = List of Disney Movies:
# https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films
#
# This exercise scrapes for ALL Disney movies
#
# ========================

## %%
from pathlib import Path
import time
import pandas as pd
import requests

from bs4 import BeautifulSoup as bs

# import submodules all on the same path

from modules.budget_gross_conversion import format_budget_and_gross
from modules.date_conversion import date_conversion, format_date_final
from modules.processing_data import get_info_box
from modules.file_save_and_load import load_movie_json_data, load_movie_pickle_data, \
     save_movie_json_data, save_movie_pickle_data

# file names and their paths
json_file_name = 'disney_test_all.json'
final_json_file_name = 'disney_movies_final.json'
json_file = Path(Path(__file__).parent/json_file_name) # jsonfile
final_json_file_ = Path(Path(__file__).parent/final_json_file_name) # jsonfile
pickle_file = Path(Path.cwd()/'disney_movie.pickle')    # pickle file



## %%
dis_movies_url = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films'

#  do request.get to disney movies wiki page to get the webpage html and convert to BeautifulSoup

# start_time = time.perf_counter()

r = requests.get(dis_movies_url)

if r.ok:
    disney_soup = bs(r.content, 'html.parser')

# getting movies info - we want to get all movies
# movies are grouped by decades and are in table with class = "wikitable sortable jquery-tablesorter"
# Using select() I slowly expand the selection to include the whole class name and stop at
# "wikitable sortable" - if I included "query-tablesorter" for some reason it gives me an empty list
# the following select() yields 12 items - each item for ever decade between 1930s-2020s
#         disney_movies = dis_movies.select("table.wikitable.sortable ")  # this returns 12 items

# but we need ALL movies regardless of the year - reviewing the HTML source I noticed that the movies are inside
# an italics tag, so we expand the select to include the <i> tag as follows, and that returns 518 items
#         disney_movies = disney_soup.select("table.wikitable.sortable i")  # this returns 518 items

# the task  is to get the href link of each of the 518 movies and the movie title
# run the following list comprehensions to check if there are any movie that doesnt have either the link or title
#        movie_titles = [movie.get_text().strip() if movie.get_text().strip() else 'None' for movie in disney_movies]
#        movie_links = [movie.a['href'] if movie.select_one("a") else 'None' for movie in disney_movies]

# running the above link, we found all movies have the get_text() info, but 9 movies do not have links
#         print(movie_titles.count("None"), movie_links.count("None"))   # returns 0 for missing titles, 9 for missing links

# so in light of this discovery, we decide to skip those movies that do not have links
# update the select() one more time to include the <a> tags (<a> tag holds the each movie's wiki page link)
disney_movies = disney_soup.select(".wikitable.sortable i a")


## %% Grab the details of each Disney movie and add to movie_info_list
start_time = time.perf_counter()

movie_info_list = []

for index, movie in enumerate(disney_movies):
    # impose a 25-second sleep timer  break after processing 100 movie transactions so as to not overwhelm wikipedia
    if index > 0 and index % 100 == 0: # let python take a break by setting a 25 second sleep timer
        time.sleep(25)
    
    ## I choose one the following if statements to just pull specific number of data 
    # if index == 50:
    #     break
    # if index < 490:
    #     continue
    # elif index == 505:
    #     break
    try:
        path = movie['href']
        full_path = f"https://en.wikipedia.org/{path}"
        movie_info_list.append(get_info_box(index+1, full_path))

    except Exception as e:
        print(f"\n{movie.get_text()}")
        print(e)

end_time = time.perf_counter()

print(f"\n\nProcess Completed: {end_time - start_time}")

# check number of movie records in the list
print(f"\n\n{len(movie_info_list) = }")



## %%
# write the current state of movie_info_list to a json file:
save_movie_json_data(json_file, movie_info_list)
# after saving the json data to a file, let's read the json data again
json_data_var = load_movie_json_data(json_file)

## %%
# check that json_data_var is exactly the same as movie_info_list (it should be)
# then throw away (delete) the json_data_var variable. If not, then it means our
# 'save and load json' methods are incorrect and must be fixed,
if movie_info_list == json_data_var:  # this should always be true
    del json_data_var  # no need to keep this variable for longer

#  update "budget", "Box office", and "Release date" values
for movie in movie_info_list:
    format_budget_and_gross(movie)
    # convert the release date value to a datetime object
    movie['Release date'] = date_conversion(movie.get('Release date', 'N/A'))

# now lets save the movie data once more - but because we just changed the release date value t a 
# python datetime object, and writing a python datetime object to JSON throws the following error:
#
#         datetime.datetime is not JSON serializable
#
# Python provides a module called pickle to serialize and deserialize data. We can write to a  
# pickle file instead.  Note that pickle is Python-specific thus pickle files can ONLY be processed
# by python, unlike JSON files which can be read and processed using other languages like Java, PHP, etc.
save_movie_pickle_data(pickle_file, movie_info_list)

## %%
# after saving the pickled JSON data to a file, let's read the pickle file just to 
# confirm that our 'save and load pickle data' functions are working properly.
pickled_json_data = load_movie_pickle_data(pickle_file)

## %%
# compare pickle_data with movie_info_list - they should be the same,
# otherwise we need to fix our 'save and load pickle data' functions
if movie_info_list != pickled_json_data:
    print("PICKLE DATA NOT MATCHED - fix 'save and load pickle data' functions")
else:
    print("Pickle data successfully saved and re-loaded")

# we read back the pickled JSON data AND convert the datetime object to "<MONTH NAME> DD, YYYY" string format
for item in pickled_json_data:
    if item.get('Release date'):
        date_obj = item.get('Release date')
        item['Release date'] = format_date_final(date_obj)


## %% - this pickle_json_data is now  JSON-ready after date format has been completed
# final_json_file_name = 'disney_movies_final.json'
# final_json_file_ = Path(Path(__file__).parent/final_json_file_name) # jsonfile

# save_movie_json_data(final_json_file_, pickled_json_data)
# final_movie_list = load_movie_json_data(final_json_file_)

## %%

#--- BONUS - PANDAS DATAFRAME
# lets pick up the data stored in the pickle file
# We are reading from the pickle_file instead of the final_json_file because pickle file can store the
# python datetime objects unlike json files.
pickled_data = load_movie_pickle_data(pickle_file)
df = pd.DataFrame(pickled_data)
## %%
final_movies_csv_file = Path(Path(__file__).parent/'final_movies_list.csv') # jsonfile

# write dataframe to csv file
df.to_csv(final_movies_csv_file)
## %%
df_dtypes = df.dtypes
print(df_dtypes)

# end_time = time.perf_counter()

# print(f"\n\nProcess Completed: {end_time - start_time}")
