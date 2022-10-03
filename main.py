
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
        
    if st.button('Simulate',key='dens_sim_buttom'):     
        with st.empty():
            for dat in dens:
                st.write(dat)
                time.sleep(1) 
    
    


st.title('Solar Wind')
animation = load_lottie("https://assets8.lottiefiles.com/packages/lf20_m7xxkrvy.json")
st_lottie(animation)


text_input = st.text_input("Enter your location in 'latitude longitude' format",key="lat_lon_input",)
#g = geocoder.ip('me')
#g.latlng


if text_input:
    st.write("You entered: ", text_input)
    try:
        lat_lon = list(text_input.split(' '))
        lat = float(lat_lon[0])
        lon = float(lat_lon[1])
        st.pyplot(sun_coords(lat,lon))
    except:
        st.error("Please enter your location in 'latitud longitude' format")


d = st.date_input("PLease select a date",datetime.date.today(),key= 'date')
    
if(datetime.date.today()<d):       
    st.error("Please enter a past date, you can't see future data !!")

d_str = str(d).split('-')

date = datos(d_str[0],d_str[1],d_str[2])


tab1, tab2, tab3 = st.tabs(["Temperature", "Density", "Velocity"])

with tab1:
    with st.container():
        
        st.write("Solar wind temperature")
    
        st.text_area('Text to analyze', '''
        It was the best of times, it was the worst of times, it was
        the age of wisdom, it was the age of foolishness, it was
        the epoch of belief, it was the epoch of incredulity, it
        was the season of Light, it was the season of Darkness, it
        was the spring of hope, it was the winter of despair, (...)
        ''',key='temp_text')
    
        wind_temp(date)
with tab2:
    with st.container():
        
        st.write("")
    
        st.text_area('Text to analyze', '''
        It was the best of times, it was the worst of times, it was
        the age of wisdom, it was the age of foolishness, it was
        the epoch of belief, it was the epoch of incredulity, it
        was the season of Light, it was the season of Darkness, it
        was the spring of hope, it was the winter of despair, (...)
        ''',key='dens_text')
    
        wind_dens(date)
      
with tab3:
    with st.container():
        
        st.write("Solar wind velocity")
    
        st.text_area('Text to analyze', '''
        It was the best of times, it was the worst of times, it was
        the age of wisdom, it was the age of foolishness, it was
        the epoch of belief, it was the epoch of incredulity, it
        was the season of Light, it was the season of Darkness, it
        was the spring of hope, it was the winter of despair, (...)
        ''',key='vel_text')
        
        wind_vel(date)