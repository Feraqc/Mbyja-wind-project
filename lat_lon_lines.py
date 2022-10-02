from codecs import latin_1_encode
import matplotlib.pyplot as plt
import numpy as np

import astropy.units as u
from astropy.coordinates import SkyCoord

import sunpy.map
from sunpy.coordinates import frames
from sunpy.data.sample import AIA_171_IMAGE


def sun_coords(lat_in,lon_in):
    aia = sunpy.map.Map(AIA_171_IMAGE)

    stonyhurst_center = SkyCoord(lon_in * u.deg, lat_in * u.deg,
                                frame=frames.HeliographicStonyhurst)

    hpc_stonyhurst_center = stonyhurst_center.transform_to(aia.coordinate_frame)

    num_points = 100
    lat_value = lat_in * u.deg
    lon_value = lon_in * u.deg
    lon0 = SkyCoord(np.linspace(-80, 80, num_points) * u.deg,
                    np.ones(num_points) * lon_value, frame=frames.HeliographicStonyhurst)
    lat0 = SkyCoord(np.ones(num_points) * lat_value,
                    np.linspace(-90, 90, num_points) * u.deg,
                    frame=frames.HeliographicStonyhurst)

    fig = plt.figure()
    ax = fig.add_subplot(projection=aia)
    aia.plot(axes=ax, clip_interval=(1, 99.99)*u.percent)
    ax.plot_coord(lat0, color="C0")
    ax.plot_coord(lon0, color="C0")
    aia.draw_grid(axes=ax)

    return fig
