import pandas as pd
import numpy as np
from datetime import datetime
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

class datos():
  def __init__(self, year, month, day):
    self.year = year
    self.month = month
    self.day = day
    self.path = "https://sohoftp.nascom.nasa.gov/sdb/goes/ace/monthly/{year}{month}_ace_swepam_1h.txt".format(year = self.year, month = self.month)
    self.df = pd.DataFrame()
    self.create_dataset()

  def get_year(self):
    return self.year

  def set_year(self, new_year):
    self.year = new_year
    return

  def get_month(self):
    return self.month

  def set_month(self, new_month):
    self.month = new_month
    return

  def get_day(self):
    return self.day

  def set_day(self, new_day):
    self.day = new_day
    return
    
  def get_dataset(self):
    return self.df

  def set_dataset(self):
    self.path = "https://sohoftp.nascom.nasa.gov/sdb/goes/ace/monthly/{year}{month}_ace_swepam_1h.txt".format(year = self.year, month = self.month)
    self.create_dataset()

  def create_dataset(self):
    self.df = pd.read_fwf(self.path, skiprows = 18, header = None)
    cols = ["Year","Month","Day","Time","Modified Julian Day","Seconds of the Day",
            "S","Proton_Density","Bulk_Speed","Ion_Temperature"]
    self.df.columns = cols
    self.df = self.df.replace(to_replace=[-9999.9,-1.00e+05],value=[np.NaN, np.NaN]).dropna()
    self.df["Date"] = pd.to_datetime(dict(year = self.df["Year"],
                                    month = self.df["Month"],
                                    day = self.df["Day"]))
    self.df["Time"] = pd.to_datetime(self.df["Seconds of the Day"], unit='s').dt.strftime('%H:%M')
    index = pd.MultiIndex.from_frame(self.df[["Date","Time"]])
    self.df = self.df.set_index(index).drop(columns = ["Year", "Month", "Day","Date","Modified Julian Day","Seconds of the Day","Time"])
    return self.df