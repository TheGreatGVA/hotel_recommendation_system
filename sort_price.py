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

def main(city):
    data = pd.read_csv('cleaned_data.csv')
    st.title('Recommendation by Price')
    st.write("we are sorting the hotels by prices")
    # unique_cities = data['City'].unique()
    # unique_cities.sort()

    # city = st.selectbox('Select your city',unique_cities)
    st.write("here are the list of hotels by price")
    hotels = data[data['City'] == city]

    # Sort the filtered data by price (ascending order)

    sorted_data = hotels.sort_values(by="Price",ascending =True)
    selected_columns = sorted_data[['hotel_name','Price','Rating']]

    # the following function is used to reset the column numbers which are displayed in the output
    no_index_data = selected_columns.reset_index(drop=True)
    st.table(no_index_data)
    # return no_index_data # not needed if we use main() but needed if we use sort_hotels_by_price(data)

# sort_hotels_by_price(data)

def main_sort():
    data = pd.read_csv('cleaned_data.csv')
    st.title('Recommendation by Price')
    st.write("we are sorting the hotels by prices")
    unique_cities = data['City'].unique()
    unique_cities.sort()

    city = st.selectbox('Select your city',unique_cities)
    st.write("here are the list of hotels by price")
    hotels = data[data['City'] == city]

    # Sort the filtered data by price (ascending order)

    sorted_data = hotels.sort_values(by="Price",ascending =True)
    selected_columns = sorted_data[['hotel_name','Price','Rating']]

    # the following function is used to reset the column numbers which are displayed in the output
    no_index_data = selected_columns.reset_index(drop=True)
    st.table(no_index_data)
    # return no_index_data # not needed if we use main() but needed if we use sort_hotels_by_price(data)

# sort_hotels_by_price(data)

if __name__ == "__main__":
    main_sort()