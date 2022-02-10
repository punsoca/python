from datetime import datetime as dt

# cleaning up the "release date" data, convert it to datetime object
def date_conversion(date): # we want to convert all dates to MMMMM dd, YYYY format

    def date_cleanup(date):
        return date.split("(")[0].strip()

    if date == 'N/A':
        return None
    if isinstance(date, list):
        date = date[0]

    date_str = date_cleanup(date)

    date_fmts = ["%B %d, %Y", "%d %B %Y"]
    for fmt in date_fmts:
        try:
            return dt.strptime(date_str, fmt)
        except:
            # when the data does not match format, don't fail it and just let it continue (pass)
            pass
    # if no formatting was done, just return None
    return None

def format_date_final(date_object):
    final_date_format = '%B %d %Y'
    return dt.strftime(date_object,final_date_format)
