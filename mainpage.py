import streamlit as st
from streamlit_option_menu import option_menu
import nltk
import ssl
import numpy as np
import pandas as pd
import pickle
import streamlit as st
import folium
from streamlit_folium import st_folium
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from ast import literal_eval

#importing the sorting files
import sort_amenities
import sort_price
import sort_rating

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "main"

stays_data = pd.read_csv('cleaned_data.csv')
data = pd.read_csv('modified_data.csv')
merged = pd.read_csv('modified_merged.csv')

pages = {
    "s_amenities" : sort_amenities.main,
    "s_price" : sort_price.main,
    "s_rating" : sort_rating.main

}


# Define function to display page content based on selection
def display_page(selected_option):
    if selected_option == "Home":
        # need to change the font size and maybe the font type as well
        st.title("Find the perfect HOTEL for your needs")
        st.write("We will provide you with all the required details to find the perfect hotel that you're looking for")
        st.write("")
        st.write("")
        unique_cities = data['City'].unique()
        unique_cities.sort()
        city = st.selectbox("Select your destination City",unique_cities,key="city")
        # st.write(f"The destination city is {city}")
        st.write(f"To find all the hotels available in {city}, please go to Search ")
        
    
    elif selected_option == "Search":
        st.write("Welcome to the Search page!")
        
        st.title('HOTEL INFORMATION')

        unique_cities = data['City'].unique()
        unique_cities.sort()

        # This creates two columns of equal width
        col1, col2 = st.columns(2)  

        with col1:
            city = st.selectbox("Select your city", unique_cities, key="city")

        with col2:
            hotel = st.selectbox("Select your hotel", data[data['City'] == city]['hotel_name'], key="hotel")

        # st.write(f"The city is ***{city}***")
        # st.write(f"The hotel is ***{hotel}***")

        city_hotels = data[data['City'] == city]
        hotel_address = data[data['hotel_name'] == hotel]['Address']

        # iloc allows you to select rows and columns by their integer indices
        # loc allows you to select rows and columns by their label indexing 
        raw_add = hotel_address.iloc[0]
        hotel_amenities = data[data['hotel_name'] == hotel]['Amenities']
        raw_amenities = hotel_amenities.iloc[0]

        # st.write(f"Here are the detaiils of ***{hotel}*** in ***{city}***")

        # this is the details part 
        st.write("Here are the details :")
        st.subheader(f"{hotel}")
        st.write(f"📍 {raw_add}")

        hotel_rating = data[data['hotel_name'] == hotel]['Rating']
        hotel_star = hotel_rating.iloc[0]
        st.write(f"⭐ Hotel Rating : {hotel_star}")
        st.write("")
        st.write("📌 Popular Amenities :")
        # st.write(f"{raw_amenities}")
        # st.write()
        l=[]
        prev=0
        for i in range(len(raw_amenities)):
            if raw_amenities[i]==",":
                l.append(raw_amenities[prev+1:i])
                prev=i
        # st.table(l)
        actual_list = literal_eval(raw_amenities)
        st.table(actual_list)

        # maps, details , link, and in last add functions 
        # this is the hyperlink part
        first_link = "[Goibibo Link](https://www.goibibo.com"
        url = data[data['hotel_name'] == hotel]['URL']
        second_link = str(url.iloc[0])
        link = first_link + second_link + ")"

        st.subheader("🔗 Hotel Website Link :")
        st.write(link)
        

        # this is the map part of the project
        latitude = merged[merged['hotel_name'] == hotel]['Latitude']
        longitude = merged[merged['hotel_name'] == hotel]['Longitude']

        map = folium.Map(location=[latitude,longitude],zoom_start=12)
        folium.Marker(location=[latitude,longitude],tooltip = "Location").add_to(map)
        st.subheader("🗺️ Hotel Map Location :")
        st_folium(map,width=700,height=500)
    # here include the footer 
    
        
    elif selected_option == "Stays":
        st.write("Welcome to the Stays page!")
        st.title("HOTEL RECOMMENDATION")
        st.write("🎡Explore the perfect stay for your next trip with our intuitive recommendation system.🏂 We understand that every traveler has unique preferences, 🏖️ which is why we offer three different ways to find your ideal hotel ✨ : ")
        st.write("1. RECOMMEND BY PRICE 💸: Looking for a budget-friendly option? Click this button to discover hotels that fit your budget while still offering great amenities and services.                Recommend by Rating: Quality is key! Click here to find hotels with top ratings and excellent guest reviews, ensuring a memorable and satisfying stay.")
        st.write("2. RECOMMEND BY AMENITIES 📚: Customize your search based on the amenities that matter most to you. Whether it's a swimming pool, free Wi-Fi, or complimentary breakfast, we'll find the perfect match for your needs.")
        st.write("3. RECOMMEND BY RATING ⭐: Quality is key! Whether you prefer luxury or value, click here to find hotels with top ratings and excellent guest reviews, ensuring a memorable and satisfying stay.")
        st.write("Simply click on one of the buttons above to get started, and let us take care of the rest! Travel planning has never been easier.""")
        st.write("")

        col1,col2,col3=st.columns([3,3,3])
        if col1.button("RECOMMEND BY PRICE", key="price_button"):
            unique_cities = stays_data['City'].unique()
            unique_cities.sort()
            city = st.selectbox('Select your city',unique_cities)

            pages["s_price"](city)
        if col2.button("RECOMMEND BY AMENITIES", key="amenities_button"):
            pages["s_amenities"]()
        if col3.button("RECOMMEND BY RATING", key="rating_button"):
            pages["s_rating"]()
            


    elif selected_option == "Attractions":
        st.write("Welcome to the Attractions page!")
    elif selected_option == "Settings":
        st.write("Welcome to the Settings page!")
    elif selected_option == "Help":
        st.write("Welcome to the Help page!")
    elif selected_option == "Account":
        st.write("Welcome to the Account page!")
        col1,col2=st.columns([3,3])
        with col1:
            st.button("LOGIN")
        with col2:
            st.button("SIGNUP")


# ------------------------------------------------------------------------------------------------------------------------------------------
with st.sidebar:
    selected = option_menu("HOTEL RECOMMENDER", ["Home", 'Search','Stays','Attractions','Settings',"Account",'Help'], 
        icons=['house-heart','search','luggage','pin-map', 'gear','person-circle','question-circle'], menu_icon="buildings", default_index=0)
    
# Display page content based on selection
display_page(selected)


