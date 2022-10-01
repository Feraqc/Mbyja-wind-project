"""
    Streamlit test
    
"""

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


def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    
    return r.json()

def wind_temp():

    
    d = st.date_input(
        "PLease select a date",
        datetime.date.today(),
        key= 'temp')
    st.write('You selected: ', d)
    
    if st.button('Simulate'):

        width = 1000
        height = 1000

        blank_image = np.zeros([height, width, 3], dtype=np.uint8)

        blank_image[:,:] = [0, 0, 0]
        img = Image.fromarray(blank_image)

        img_holder = st.empty()

        with st.empty():
            for seconds in range(0,250):
                blank_image[:,:] = [seconds, 250-seconds, 0]
                img = Image.fromarray(blank_image)
                st.image(img)
                time.sleep(0.001)    
        
    else:
        st.write('Click to begin simulation')

def wind_vel():
    d = st.date_input(
    "PLease select a date",
    datetime.date.today(),key='vel')
    st.write('You selected: ', d)
    
    vel_animation = load_lottie('https://assets7.lottiefiles.com/packages/lf20_zsn2p2gv.json')
    st_lottie(
        vel_animation,
        speed=0.3
    )
    
    

st.title('Solar Wind')
animation = load_lottie("https://assets8.lottiefiles.com/packages/lf20_m7xxkrvy.json")
st_lottie(animation)




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
        ''')
    
        wind_temp()
    
with tab3:
    wind_vel()