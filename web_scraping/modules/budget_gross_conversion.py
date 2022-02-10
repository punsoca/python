import re
from decimal import Decimal

# =================================================================================
# Convert budget and box office amounts to numeric values
# =================================================================================

get_unit_value_dict = {'thousand':1000, "million": 1000000, "billion": 1000000000}

units = '|'.join([k for k in get_unit_value_dict.keys()]) # equals to "thousand|million|billion"

# regex variables
# following regex accepts amount figures with or without commas and decimal places
# Accepts  "4",  "3000", "3,000",  "3000.5"  or "3,000.90"
number = r"\d+(,\d{3})*\.*\d*"

# detect and process amount values with words in ('thousand', 'million', 'billion')
# e.g. $12 million, $1-2 thousand, $3-4 million, $5 to 6 million
word_re = rf"\${number}\s*(-|\sto\s|–)?({number})?\s({units})"

# get the numeric value that immediately follows a dollar figure
# e.g. $120,000 - 400,000 million   - returns '120,000'
#      $1-2 BILLION  - returns '1'
value_re = rf"\${number}"

def money_conversion(money):

    # money_conversion("$12.2 million") --> 12200000    # word_syntax
    # money_conversion("$790,000") --> 790000           # value syntax

    # convert a amount value in word syntax (e.g., "$4 million") to a float value (i.e., 4000000.0)
    def parse_word_syntax(amt_string, num_string):
        value_string = re.search(number,num_string).group()
        # strip off commas from the value_string - e.g., from '3,000 thousand' to '3000 thousand'
        value  = float(value_string.replace(',',''))

        unit = re.search(units, amt_string, flags=re.I).group().lower()  # convert unit to lowercase
        unit_to_number = get_unit_value_dict[unit]
        # converting floating point arithmetic to decimal arithmetic
        return (float(Decimal(str(value)) * unit_to_number)) if unit else None

    def parse_value_syntax(amount):
        # value_string = re.search(currency_pattern,amount).group()
        value_string = re.search(number,amount).group()
        # strip off commas after regex
        value  = float(value_string.replace(',',''))
        return value


    if money == 'N/A':
        return None

    if isinstance(money, list):
        # only process amounts with dollar figures. otherwise return None
        money = [amt for amt in money if '$' in amt]
        money = money[0] if money else 'None'

    # ignore case when doing re.search in word_syntax by passing "flags=re.I" parameter
    word_syntax = re.search(word_re, money, flags=re.I)
    value_syntax = re.search(value_re, money)

    if word_syntax:
        # return parse_word_syntax(word_syntax.group())  # commented out temporarily
        return parse_word_syntax(word_syntax.group(), value_syntax.group())

    elif value_syntax:
        return parse_value_syntax(value_syntax.group())
    else:
        return None

def format_budget_and_gross(the_movie):
    the_movie['Budget (US$)'] = money_conversion(the_movie.get('Budget', 'N/A'))
    the_movie['Box office (US$)'] = money_conversion(the_movie.get('Box office', 'N/A'))
    del_keys = ("Budget", "Box office")
    list(map(the_movie.__delitem__, filter(the_movie.__contains__,del_keys)))
    # print(d)
    return the_movie

# --- END OF Monetary Conversion functions
