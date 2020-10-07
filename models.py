from django.db import models
from django.http import Http404

import os
import datetime
import pandas as pd


# Create your models here.
def _lines_to_acronym_df(raw_data):
    """Parse standard-format string into a dataframe
    Columns of resulting dataframe:
      - acronym (string)
      - fulltext (string)
    """
    data = [[entry.strip() for entry in line.split(',')]
            for line in raw_data.split('\n')]
    data = [row if len(row) == 2 else [row[0]] + [", ".join(row[1:])]
            for row in data]
    print([row for row in data if len(row) != 2])
    df = pd.DataFrame(data, columns=["acronym", "fulltext"])
    return df


def acronym_of_the_day():
    file_name = "aotd.csv"
    path = os.path.realpath(__file__)
    path_dir = os.path.split(path)[0]
    filepath = os.path.join(path_dir, "data", file_name)

    # What is today, anyway?
    today = datetime.date.today()

    # If we already have acronyms in a csv by date, 1) load and 2) read
    if os.path.isfile(filepath):
        # Load
        daily_acronyms_df = pd.read_csv(filepath, sep='`')
        # Convert string (2020-10-07) to datetime to date
        daily_acronyms_df.date = [x.date() for x in
                                  pd.to_datetime(daily_acronyms_df.date)]
        # Check if today is in there
        if (daily_acronyms_df.date == today).any():
            today_row = daily_acronyms_df[daily_acronyms_df.date == today]
            # Guaranteed to have a row, or we wouldn't be in this if statement
            today_acronym = today_row.acronym.tolist()[0]
            today_fulltext = today_row.fulltext.tolist()[0]
            return (today_acronym, today_fulltext)

    # No existing acronyms: generate the next year's worth and save them
    df = load_data()
    days = [today + datetime.timedelta(days=n) for n in range(365)]
    daily_acronyms_df = df.sample(n=365)
    daily_acronyms_df['date'] = days
    daily_acronyms_df.to_csv(filepath, sep='`')
    return acronym_of_the_day()


def load_data():
    file_name = 'acronyms.csv'
    path = os.path.realpath(__file__)
    path_dir = os.path.split(path)[0]
    filepath = os.path.join(path_dir, "data", file_name)
    try:
        with open(filepath, "r+", encoding="utf-8") as myfile:
            raw = ''.join(myfile.readlines())
    except FileNotFoundError:
        # What do I raise here? Do I go straight to Http errors??
        raise Http404("Invalid pass name or year")

    # PROCESS DATA
    df = _lines_to_acronym_df(raw)
    return df


def search(df, search_string=None):
    if search_string is None:
        search_string = ""
    search_string = search_string.lower()
    df = df.copy()
    df['acronym_lower'] = df.acronym.str.lower()
    df['fulltext_lower'] = df.fulltext.str.lower()

    acronym_match = df[df.acronym_lower.str.contains('.*' +
                                                     search_string +
                                                     '.*')]
    fulltext_match = df[df.fulltext_lower.str.contains('.*' +
                                                       search_string +
                                                       '.*')]
    cols = ['acronym', 'fulltext']
    acronym_match = acronym_match[cols]
    fulltext_match = fulltext_match[cols]
    return (acronym_match, fulltext_match)
