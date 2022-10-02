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
    self.path = self.create_path()
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
  
  def create_path(self):
    path = "https://sohoftp.nascom.nasa.gov/sdb/goes/ace/monthly/{year}{month}_ace_swepam_1h.txt".format(year = self.year, month = self.month)
    return path

  def get_dataset(self):
    return self.df

  def set_date(self, year, month, day):
    self.set_year(year)
    self.set_month(month)
    self.set_day(day)
    self.set_dataset()

  def set_dataset(self):
    self.path = self.create_path()
    self.create_dataset()

  def create_dataset(self):
    self.df = pd.read_fwf(self.path, skiprows = 18, header = None)
    cols = ["Year","Month","Day","Time","Modified Julian Day","Seconds of the Day",
            "S","Proton_Density","Bulk_Speed","Ion_Temperature"]
    self.df.columns = cols
    self.df = self.df.replace(to_replace=[-9999.9,-1.00e+05],value=[np.NaN, np.NaN]).bfill()
    self.df["Time"] = pd.to_datetime(self.df["Seconds of the Day"], unit='s').dt.strftime('%H:%M')
    self.df["Date"] = pd.to_datetime(dict(year = self.df["Year"],
                                    month = self.df["Month"],
                                    day = self.df["Day"]))#,
                                    #hours = self.df["Time"].apply(lambda x: x.split(":")[0])))
    index = pd.MultiIndex.from_frame(self.df[["Date","Time"]])
    self.df = self.df.set_index(index).drop(columns = ["Year", "Month", "Day","Date","Modified Julian Day","Seconds of the Day","Time"])
    #self.df = self.norm_dataset(self.df)
    return self.df

  def norm_dataset(self, df):
    return (df - df.min()) / ( df.max() - df.min())

  def get_values(self, opt):
    if opt == "density":
      request = "Proton_Density"
    elif opt == "velocity":
      request = "Bulk_Speed"
    elif opt == "temperature":
      request = "Ion_Temperature"

    resp = self.df.iloc[self.df.index.get_level_values('Date') == "{year}-{month}-{day}".format(year = self.year, month = self.month, day = self.day)]
    resp = resp[request]
    return resp.values

  def visualize_data(self):
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()

    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

    par2.axis["right"].toggle(all=True)

    #host.set_xlim(0, 2)
    #host.set_ylim(0, 2)

    host.set_xlabel("Hour")
    host.set_ylabel("Proton Density")
    par2.set_ylabel("Bulk Speed")
    par1.set_ylabel("Ion Temperature")

    x_axis = self.df.iloc[self.df.index.get_level_values('Date') == "{year}-{month}-{day}".format(year = self.year, month = self.month, day = self.day)]
    p1, = host.plot(x_axis.reset_index()["Time"].apply(lambda x: x.split(":")[0]).astype(int), x_axis["Proton_Density"], label="Proton Density")
    p2, = par1.plot(x_axis.reset_index()["Time"].apply(lambda x: x.split(":")[0]).astype(int), x_axis["Ion_Temperature"], label="Ion Temperature")
    p3, = par2.plot(x_axis.reset_index()["Time"].apply(lambda x: x.split(":")[0]).astype(int), x_axis["Bulk_Speed"], label="Bulk Speed")

    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    plt.draw()
    plt.show()
    return
