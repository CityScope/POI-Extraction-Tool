import streamlit as st
import pandas as pd
from src.extractor import geocode_address, get_pois

st.title("POI Extraction Tool")

st.markdown("""
This tool allows you to extract Points of Interest (POIs) from OpenStreetMap.
Enter an address or latitude/longitude to get started.
""")

address = st.text_input("Enter an address")
lat = st.number_input("Or enter Latitude", format="%.6f")
lon = st.number_input("And Longitude", format="%.6f")

if st.button("Extract POIs"):
    if address:
        latitude, longitude = geocode_address(address)
        if not latitude:
            st.error("Could not geocode address. Please try again.")
        else:
            st.success(f"Geocoded address to: ({latitude}, {longitude})")
            df = get_pois(latitude, longitude)
            if not df.empty:
                st.success(f"Found {len(df)} POIs.")
                st.dataframe(df)
                
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='pois.csv',
                    mime='text/csv',
                )
            else:
                st.warning("No POIs found in the specified area.")

    elif lat and lon:
        df = get_pois(lat, lon)
        if not df.empty:
            st.success(f"Found {len(df)} POIs.")
            st.dataframe(df)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='pois.csv',
                mime='text/csv',
            )
        else:
            st.warning("No POIs found in the specified area.")

    else:
        st.warning("Please enter an address or coordinates.")
