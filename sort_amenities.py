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

def main():
    data = pd.read_csv('modified_merged.csv')
    comb_amen = pd.read_csv('combined_amenities.csv') # City,Combined_Amenities
    st.title('Recommendation by Amenities')

    data["Amenities"] = data["Amenities"].apply(literal_eval)

    unique_cities = data['City'].unique()
    unique_cities.sort()

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("Select your city",unique_cities,key="city")

    # need to display the amenities one by one and onegroup by onegroup
    amen = comb_amen[comb_amen['City']==city]['Combined_Amenities']
    raw_amen = amen.iloc[0]
    actual_amen = literal_eval(raw_amen)

    with col2:
        required_amenities = st.multiselect("Select your amenities",actual_amen,key="required_amenities")

    # Function to check if a hotel's amenities contain any the required amenities
    def has_required_amenities(amenities_list, required):
        if not required:
            return True  # If no required amenities, return all hotels in the city
        return any(amenity in amenities_list for amenity in required)

    # Filter by city and check if amenities contain all the required amenities
    filtered_hotels = data[
        (data['City'].str.lower() == city.lower()) & 
        (data['Amenities'].apply(lambda x: has_required_amenities(x, required_amenities)))
    ]

    st.write("The number of hotels available are",len(filtered_hotels))
    # Display the filtered hotels in a table
    if not filtered_hotels.empty:
        st.table(filtered_hotels[['hotel_name','Amenities']])  # Display selected columns
    else:
        st.write("No hotels found matching the criteria.")

if __name__ == "__main__":
    main()