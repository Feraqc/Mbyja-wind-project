
import streamlit as st
import numpy as np
import pandas as pd
import time
import PIL.Image as Image
import random
import datetime
import json
import requests
from streamlit_lottie import st_lottie
from lat_lon_lines import sun_coords
import geocoder
from audio_output import audio_output
from class_datos import datos
from temp_rgb import conversion_temp_rgb
from Densidad import repr_den



def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    
    return r.json()

def wind_temp(date):
    
    data = date.get_values('temperature')
    st.write(date.visualize_data('temperature'))
    rgb = []
    for dat in data:
        rgb.append(conversion_temp_rgb(dat))
    st.text('In the simulation above the canvas color represents the Ion temperature equivalence in RGB code ')
    if st.button('Simulate'):

        width = 1000
        height = 1000

        blank_image = np.zeros([height, width, 3], dtype=np.uint8)

        blank_image[:,:] = [0, 0, 0]
        img = Image.fromarray(blank_image)

        im_holder = st.empty()
        with st.empty():
            for dat in rgb:
                blank_image[:,:] = [dat[0],dat[1],dat[2]]
                img = Image.fromarray(blank_image)
                st.write(dat)
                st.image(img)
                time.sleep(1)     
        
    else:
        st.write('Click to begin simulation')

def wind_vel(date):
        
    data = date.get_values('speed')
    st.write(date.visualize_data('speed'))
    st.text("In the simulation above the bulk speeds its representated as a sinusoidal wave sound where it's magnitude corresponds to the wave frequency ")
    
    if st.button('Simulate',key='audio_butt'):
        audio_output(data)  
    else:
        st.write('Click to begin simulation')
    
    
    
    
    vel_animation = load_lottie('https://assets7.lottiefiles.com/packages/lf20_zsn2p2gv.json')
    st_lottie(
        vel_animation,
        speed=0.3   
    )
    
def wind_dens(date):
    data = date.get_values('density')
    st.write(date.visualize_data('density'))
    
    dens = []
    for dat in data:
        dens.append(repr_den(dat))
    st.text("In the simulation above the density it's representated graphically as points in a square ")
    if st.button('Simulate',key='dens_sim_buttom'):     
        with st.empty():
            for dat in dens:
                st.write(dat)
                time.sleep(1) 
    
    


st.title('\tSolar Wind')
animation = load_lottie("https://assets8.lottiefiles.com/packages/lf20_m7xxkrvy.json")
st_lottie(animation)

st.text_area('A brief introduction to solar wind', '''  The solar wind is a stream of charged particles, mainly electrons and protons, that are released from the very hot corona, the upper atmosphere of the Sun. The particles escape the Sun’s gravity because of their high kinetic energy w3. This stream of particles reaching Earth varies in density, temperature and speed, depending on time and longitude. When these particles approach Earth, they can have various effects: from spectacular aurorae to great geomagnetic storms. As geostationary satellites are near the edge of Earth’s protective magnetism, they can be exposed to these storms.!! ''',key='intro_text')




if st.button('Click here for your IP current location equivalent to the SUN !!'):
    g = geocoder.ip('me')
    g.latlng
    st.pyplot(sun_coords(g.latlng[0],g.latlng[1]))


d = st.date_input("Select a date for the data analysis",datetime.date.today(),key= 'date')
    
if(datetime.date.today()<d):       
    st.error("Please enter a past date, you can't see future data !!")

d_str = str(d).split('-')

date = datos(d_str[0],d_str[1],d_str[2])


tab1, tab2, tab3 = st.tabs(["Temperature", "Density", "Velocity"])

with tab1:
    with st.container():
        
        st.text_area('Solar wind temperature ', '''The solar wind is composed of materials found in the solar plasma, composed of ionized hydrogen with 8% helium and some heavy ions and atomic nuclei torn apart by heating of the solar corona.
        ''',key='temp_text')
    
        wind_temp(date)
with tab2:
    with st.container():
        
        st.text_area('Solar wind density', '''At the orbit of the Earth, the solar wind has an average density of about 6 ions/cm3. This is not very dense at all!.
        ''',key='dens_text')
    
        wind_dens(date)
      
with tab3:
    with st.container():
        
    
        st.text_area('Solar wind velocity', '''Near the Earth's orbit at 1 Astronomical Unit (AU) the plasma flows at speeds ranging from 250–750 km/s (155-404 mi/s) ''',key='vel_text')
        
        wind_vel(date)