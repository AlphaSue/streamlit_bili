import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd

def get_bilibili_video_views(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # The number of views might be in a tag like this, but this could vary
    # You'll need to inspect the page to find out where the information is
    views_tag = soup.find('span', {'class': 'view'})  
    #views = int(views_tag.text.replace(',', '')) if views_tag else None
    if '万' in views_tag.text:
        ratio = 10000
    else:
        ratio = 1
    views = int(float(views_tag.text.replace(',', '').replace('万',''))*ratio) if views_tag else None

    return views

# Streamlit code
st.title('恭喜AlphaSue视频播放量达到:')

#url = st.text_input('Enter the URL of a Bilibili video')
url = "https://b23.tv/RRZRizt"
title_name = "我的超级工作站：Mac mini与Windows台式机的强强联手"

if url:
    views_placeholder = st.empty()
    time_placeholder = st.empty()
    title_placeholder = st.empty()

    # Load the data from the CSV file, or create a new dataframe if the file doesn't exist
    try:
        data = pd.read_csv('data.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Time", "Views"])

    # Create a line chart
    chart = st.line_chart(data.set_index("Time"))

    while True:
        views = get_bilibili_video_views(url)
        current_time = datetime.now().strftime("%H:%M:%S")

        # Add the new data to the dataframe
        if views is not None:
            new_data = pd.DataFrame({"Time": [current_time], "Views": [views]})
            data = pd.concat([data, new_data], ignore_index=True)

            # Update the line chart
            chart.add_rows(new_data.set_index("Time"))

            # Save the data to the CSV file
            data.to_csv('data.csv', index=False)

        title_placeholder.markdown(f'<h2 style="color:blue;">{title_name} "链接:"{url}</h2>', unsafe_allow_html=True)
        views_placeholder.markdown(f'<h2 style="color:blue;">The video has {views if views is not None else "Unknown"} views.</h2>', unsafe_allow_html=True)
        time_placeholder.markdown(f'<h2 style="color:green;">Current time: {current_time}</h2>', unsafe_allow_html=True)

        time.sleep(0.5)

