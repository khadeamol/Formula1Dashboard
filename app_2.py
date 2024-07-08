import streamlit as st 
import pandas as pd
import os 
import fastf1 as ff
from time import time
import driver_trace
import trace_options
import fastf1SessionLoad

def yearList():
    yearList = os.listdir("cache")
    print(yearList.sort())
    return yearList   

schedule = pd.read_parquet("./races_by_year.pq")

def yearRaceCheck(df, year, race):
    allEventsYear = list(df[df['EventYear'] == str(year)]['EventName'])
    if race in allEventsYear:
        print("yes")
        return "Exists."
    else:
        print()
        return "You played yo'self"

def generateDriverList(sessionObj, yearSel, raceSel):
    driverList = sessionObj.results.Abbreviation
    return driverList


lapTimingDetails = ""

raceSel = ""
sessionSel = ""
driverList = ""
tab1, tab2, tab3 = st.tabs(["Driver Analysis", "Comparison", "Placeholder"])
# if "sessionObj" not in st.session_state:
#     st.session_state['sessionObj'] = 0

with st.sidebar:
    yearSelect = st.text_input("Enter year")
    raceSelect = st.selectbox(f"Select Race for {yearSelect}:", schedule.EventName.unique())
    raceSubmit = st.button("Pick race")
    if raceSubmit:
        # yearSelect = st.text_input("Enter year")
        # raceSelect = st.selectbox(f"Select Race for {yearSelect}:", schedule.EventName.unique())
        checkResult = yearRaceCheck(schedule, yearSelect, raceSelect)
        if checkResult == "Exists.":
            print("Checking items")
            if 'sessionObj' not in st.session_state:
                st.session_state['sessionObj'] = fastf1SessionLoad.loadSession(int(yearSelect), raceSelect)
                print("In if")
                sessionObj=st.session_state.get('sessionObj')
                st.session_state['driverList'] = generateDriverList(sessionObj, yearSelect, raceSelect)        
            else:
                print("In else")
                sessionObj = st.session_state.get('sessionObj')
                print(generateDriverList(sessionObj, yearSelect, raceSelect))
                st.session_state['driverList'] = generateDriverList(sessionObj, yearSelect, raceSelect)        
        else:
            st.write("Wrong Year-Race combination. Try again.")


with tab1:
    sessionObj = st.session_state.get('sessionObj')
    driverList = st.session_state.get('driverList')
    with st.sidebar:
        st.write("Drivers in the session.")
        x = st.dataframe(driverList, use_container_width=True, hide_index=True)

    driverSel = st.text_input("Enter Driver Initials")
    lapSel = st.text_input("Enter Lap Number. Defaults to fastest lap.", "Fastest Lap.")
    goButton = st.button("Let's Go!")
    if goButton:
        print("Driver selected:", driverSel)
        lapTimingDetails = driver_trace.plot_traces(sessionObj, driverSel)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(lapTimingDetails, use_container_width=True)


with tab2:
    sessionObj = st.session_state.get('sessionObj')
    driverSel1 = st.text_input("Enter Driver 1 Identifier")
    driverSel2 = st.text_input("Enter Driver 2 Identifier")
    lapSel = st.text_input("Enter lap to compare. Defaults to fastest lap.")
    
    goButton = st.button("Compare Laps.")
    if goButton:
        print("Driver selected:", driverSel)
        lapsCompared = trace_options.fastestLapTrace(sessionObj, driverSel1, driverSel2)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(lapsCompared, use_container_width=True)