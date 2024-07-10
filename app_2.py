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

def generateRaceList(year):
    df = schedule
    raceList = df[df['EventYear']==year]['EventName']
    # print(raceList)
    # st.write(raceList)
    return raceList

lapTimingDetails = ""
resetButton = st.button("Reset")
if resetButton:
    st.session_state.clear()
raceSel = ""
sessionSel = ""
driverList = ""
tab1, tab2, tab3 = st.tabs(["Driver Analysis", "Comparison", "Placeholder"])

with st.sidebar:
    with st.form("New form"):
        yearSelect = st.selectbox("Enter year", options = schedule.EventYear.unique())
        st.session_state['yearSel'] = yearSelect
        st.form_submit_button("Select Year.")
        # st.session_state.clear('sessionObj')
        
        if yearSelect:
            raceList = generateRaceList(yearSelect)    
            st.session_state['raceList'] = raceList
        
    with st.form("New form 2"):
        raceSelect = st.selectbox(f"Select Race for {yearSelect}:", raceList)
        st.session_state['raceSelect'] = raceSelect
        # st.session_state['raceSubmit'] = raceSubmit
        submitForm = st.form_submit_button("Let's go!")

        if submitForm:
            if 'sessionObj' not in st.session_state:
                st.session_state['sessionObj'] = fastf1SessionLoad.loadSession(int(yearSelect), raceSelect)
                print("In if")
                sessionObj=st.session_state.get('sessionObj')
                st.session_state['driverList'] = generateDriverList(sessionObj, yearSelect, raceSelect)        
                
            else:
                print("In else")
                sessionObj = fastf1SessionLoad.loadSession(int(st.session_state['yearSel']), st.session_state['raceSelect'])
                print(generateDriverList(sessionObj, yearSelect, raceSelect))
                st.session_state['driverList'] = generateDriverList(sessionObj, yearSelect, raceSelect)        
    st.write(driverList)



with tab1:
    
    sessionObj = st.session_state.get('sessionObj')
    driverList = st.session_state.get('driverList')

    driverSel = st.selectbox("Enter Driver Initials", options = driverList)

    lapSel = st.text_input("Enter Lap Number. Defaults to fastest lap.", "Fastest Lap.")
    goButton = st.button("Let's Go!")
    if goButton:
        print("Driver selected:", driverSel)
        st.write(f"Selected Lap for {driverSel} at {st.session_state.get('yearSel')} {st.session_state.get('raceSelect')}")
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

        st.write(f"Comparing selected lap {driverSel1} and {driverSel2} at {st.session_state.get('yearSel')} {st.session_state.get('raceSelect')}")
        lapsCompared = trace_options.fastestLapTrace(sessionObj, driverSel1, driverSel2)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(lapsCompared, use_container_width=True)