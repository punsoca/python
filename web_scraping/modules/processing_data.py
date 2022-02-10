from bs4 import BeautifulSoup as bs

import requests

# %%
# --- BEGIN functions that handle data formatting
def clean_up_references(soup):
    # remove superscript tags using decompose()
    for tag in soup.find_all("sup"):
        tag.decompose()

    # remove the extranenous "(YYYY-MM-DD)"" tags , we only need the MONTH DAY, YEAR format
    for span in soup.find_all("span", class_= "bday dtstart published updated"):
        span.find_parent().decompose()

def get_dict_val(row_data):
    '''
    We have to make some adjustments so the texts gleaned from the infobox would display corectly:
    #1 - for running minutes, return the integer value of minutes (i.e., 60 for '60 minutes')

    #1 - we replace the literal "/xa0" string to a space
    #2 - using  get_text (" ", strip=True) instead of get_text() to allow texts separated by a
         line break <br> to display in the same line WITH a space between them (for readability)
        Example:
            when we do a div.get_text() on the following: <div>Production<br>company</br?<div>,
            it prints "Productioncompany" without a space in between texts.  To fix it, use
            div.get_text(" ", strip=True) which will render it into "Production company".

    #3 - handling table rows with table data containing lists or line breaks
    '''

    # Change  "Running time" value from string "50 minutes" to integer value 50
    if ' min' in row_data.get_text():
        return int(row_data.get_text().split()[0])

    # group text value of elements with "li" items' into a list
    # also replace 'xa0' with whitespace e.g. "good\xa0morning" -> "good morning"
    elif row_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ")  for li in row_data.find_all("li")]

    # some elements use <br> instead of <li> to list items, collect the texts from these line breaks into a list
    elif row_data.find("br"):
        return [item for item in row_data.stripped_strings]

    else:
        return row_data.get_text(" ", strip=True).replace("\xa0", " ")

# process the infobox to gather all information from a movie
def get_info_box(movie_indx, href):
    resp = requests.get(href)
    if resp.ok:
        movie_html = bs(resp.content, 'html.parser')

    # first check if mov object has an "infobox-header summary" - if present, DO NOT PROCESS as it is not a movie
    if movie_html.find("th", class_= "infobox-header summary"):
        raise Exception(f"{href} is incorrectly linked to a TV show, not movie")
    else:
        clean_up_references(movie_html)

        # Grab table tag with class="infobox vevent", as it contains all the movie info data we need
        infobox = movie_html.select_one("table.infobox.vevent") # infobox is under table element class=infobox.vevent

        # get infobox table rows (info_tr) from the infobox
        info_tr = infobox.select("tr")
        # print(f"{info_tr = }")

        movie_info = {}
        for idx, row in enumerate(info_tr):
            if idx==0:
                movie_title = row.find("th").get_text(" ", strip=True)
                movie_info['title'] = f"# {movie_indx:03d}: {movie_title}"
                # add the wiki link for the movie in the dictionary
                movie_info['wiki_link'] = href
            # elif index > 1:
            elif row.find("th"):  # if there is a row header then process
                d_key = row.find("th").get_text(" ", strip=True)
                d_val = get_dict_val(row.find("td"))
                movie_info[d_key] = d_val

    return movie_info
