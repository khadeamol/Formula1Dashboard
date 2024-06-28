import streamlit as st 
import pandas as pd
import os 
import fastf1 as ff
from time import time
import driver_trace
import trace_options
from google.cloud import storage

bucket_name = "f1dashboard"
client = storage.Client()
bucket = client.bucket(bucket_name)

def yearList():
    cache = "https://console.cloud.google.com/storage/browser/f1dashboard"
    yearList = bucket.list_blobs()
    print(yearList)
    return yearList

def raceListGenerator(year):
    raceList = os.listdir(f"{cache}/{year}")
    return raceList

schedule = pd.read_parquet("./races_by_year.pq")
yearSel = '2024'
eventList = schedule[schedule['EventYear'] == yearSel]
lapTimingDetails = ""


tab1, tab2, tab3 = st.tabs(["Driver Analysis", "Comparison", "Placeholder"])

with st.sidebar:
    with st.form("Sidebar form"):
        yearSel = st.selectbox("Select Year",yearList())
        raceSel = st.selectbox("Select Event:", eventList)
        sessionSel = st.selectbox("Select Session:",options=["Race","Qualifying","FP1","FP2", "FP3", "Sprint"])
        print("Good work!")
        typeSubmit = st.form_submit_button("Go!")

with tab1:
    with st.form("Single Driver Form"):
        driverSel = st.text_input("Enter Driver Identifier")
        lapSelect = st.text_input("Enter Lap Number", placeholder="Pick Fastest")
        submitted = st.form_submit_button("Submit")
        if submitted:
            print("You selected driver:", driverSel)
            lapTimingDetails = driver_trace.plot_traces(int(yearSel), raceSel, sessionSel, driverSel, lapSelect)
            st.pyplot(lapTimingDetails, use_container_width=True)


with tab2:     
    with st.form("Two Driver Form"):
        driverSel = st.text_input("Enter First Driver")
        driver2Sel = st.text_input("Enter Second Driver")
        lapSelect = st.text_input("Enter Lap Number", placeholder="Pick Fastest")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            print(driverSel)
            lapTimingDetails = trace_options.fastestLapTrace(int(yearSel), raceSel, sessionSel, driverSel, driver2Sel)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(lapTimingDetails, use_container_width=True)


# with st.sidebar:
#     with st.form("Base Form"):
#         yearSel = st.selectbox("Select Year",yearList())
#         # yearSel = st.text_input("Enter Year:")
#         raceSel = st.selectbox("Select Event:", eventList)
#         sessionSel = st.selectbox("Select Session:",options=["Race","Qualifying","FP1","FP2", "FP3", "Sprint"])
#         print("Good work!")
#         typeSel = st.radio("Analysis Type:", options=['Driver Lap Speed Trace', 'Driver Speed Comparison'])
#         typeSubmit = st.form_submit_button("Go!")
#         if typeSel == "Driver Lap Speed Trace":
#             driverSel = st.text_input("Enter Driver Identifier")
#             lapSelect = st.text_input("Enter Lap Number", placeholder="Pick Fastest")
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 print(driverSel)
#                 lapTimingDetails = driver_trace.plot_traces(int(yearSel), raceSel, sessionSel, driverSel, lapSelect)

#         elif typeSel == 'Driver Speed Comparison':
#             driverSel = st.text_input("Enter First Driver")
#             driver2Sel = st.text_input("Enter Second Driver")
#             lapSelect = st.text_input("Enter Lap Number", placeholder="Pick Fastest")
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 print(driverSel)
#                 lapTimingDetails = trace_options.fastestLapTrace(int(yearSel), raceSel, sessionSel, driverSel, driver2Sel)
        

        # driver2Sel = st.text_input("Add Second Driver for comparison")


# st.set_option('deprecation.showPyplotGlobalUse', False)
# st.pyplot(lapTimingDetails, use_container_width=True)

# Once user selects a year, the race dropdown will change
# depending on the races that happened that year
# Does this add