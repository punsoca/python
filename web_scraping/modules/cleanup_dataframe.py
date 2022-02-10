'''
    This function performs clean-up of dataframes.

    The code shows a few ways of how to remove columns from a dataframe.
    IT also shows different ways to replace values in a column.
    
    TIP: 
    I  ran the dataframes.info  in the background to decide which columns 
    to remove based on the total percentage of NULL values per column 
    (I went with columns whose total rows have NaN values that are 90% and higher).

'''
import pandas as pd

def clean_up_columns(df):

# DROP ONE COLUMN
    df.drop(columns='Hepburn', inplace=True)

    # DROP COLUMNS (USE A LIST)
    df.drop(columns=['Languages','Countries'], inplace=True)

    # DROP COLUMN USING COLUMN INDEX 
    # when not specify 'columns=' for the following commands, use axis=1 to indicate column items
    df.drop(df.iloc[:, [34,]], axis=1, inplace=True) # delete one column only using column index
    df.drop(df.iloc[:, [31,32,33]], axis=1, inplace=True) # delete  multiple columns using their respective column indices

    # DELETING A RANGE OF COLUMNS FROM A DATAFRAME
    #----
    # (1) to delete a range of columns, code it as follows (two steps) - more readable
    cols = df.columns[22:]
    df = df.drop(columns=cols)  # no need for inplace=True cause you're re-assigning df with "df = df.drop ..."

    # (2) or you could do it as a one liner, but this way you need to include inplace= option
    df.drop(columns=df.columns[22:], inplace=True)
    #----

def cleanup_dataframe(dataset):

    dataset = clean_up_columns(dataset)
    return clean_up_nan_values(dataset)
