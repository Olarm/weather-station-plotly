
import socket
from datetime import datetime, date, timedelta

import pandas as pd

def date_strings(datestamp):
    year = str(datestamp.year)
    month = str(datestamp.month)
    day = str(datestamp.day)

    y_m = year + "-" + month.rjust(2, "0")
    y_m_d = y_m + "-" + day.rjust(2, "0")
    
    return year+"/"+y_m+"/"+y_m_d


def file_path(selected_date):
    datestring = date_strings(selected_date)

    hostname = socket.gethostname()
    if hostname == "Roma":
        path = "/home/terje/weather/data/raw/"+datestring+".txt"
    else:
        path = "/home/ola/dev/weather-dash/raw/"+datestring+".txt"

    return(path)


def get_data(date_from=date.today() - timedelta(days=1), date_to=date.today()):
    dt = timedelta(days=0)
    if date_to > date_from:
        dt = date_to - date_from

    dfs = []
    for d in range(dt.days + 1):
        path = file_path(date_from+timedelta(days=d))
        try:
            temp_df = pd.read_csv(path, names=[
                "timestamp", 
                "interval", 
                "Luftfuktighet inne", 
                "Temperatur inne", 
                "Luftfuktighet ute", 
                "Temperatur ute", 
                "Absolutt trykk", 
                "Vind gjennomsnitt", 
                "Vindkast", 
                "Vindretning", 
                "Regn akkumulert time", 
                "Regn akkumulert år"
            ])
        except FileNotFoundError:
            continue
        temp_df = temp_df.drop(columns=["Luftfuktighet inne", "Temperatur inne"])
        temp_df.timestamp = pd.to_datetime(temp_df.timestamp, format="%Y-%m-%d %X")
        dfs.append(temp_df)

    return pd.concat(dfs, ignore_index=True)
