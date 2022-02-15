#
#   API URL: https://jsonmock.hackerrank.com/api/article_users?page=<pagenumber>
#
#   This is a simple API request to read in a json file from a given url.
#   Create a list of authors whose submission count is greater than the threshold.
#   Write out the list to a json file named 'authors_list.json'.
#

# %%
from pathlib import Path
import json
import requests

# %%
# users array and threshold
authors = []
threshold = 50
current_page = 1
url = "https://jsonmock.hackerrank.com/api/article_users?page="

def run_api_request(page):
    r = requests.get(url + str(page))
    if r.ok:
        # return the json() object from the response
        return r.json()
    else:
        print('Error while accessing URL - check URL link')

def write_to_json(authors_list):
    '''
        write the list of authors onto  a json file
    '''
    filepath = Path(__file__).parent
    results = { "authors_list" : authors_list}
    f = Path(filepath/'authors_list.json')
    with f.open( 'w') as outfile:
        json.dump(results, outfile, indent=4)

# %%

article_users = run_api_request(current_page)
total_pages = article_users['total_pages']

while True:
    user_data = article_users['data']
    for user in user_data:
        if user['submission_count'] > threshold:
            authors.append(user['username'])

    current_page +=1
    if current_page <= total_pages:
        article_users = run_api_request(current_page)
    else:
        break

print(authors)
write_to_json(authors)
