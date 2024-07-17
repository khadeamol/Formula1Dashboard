import streamlit as st 
import pandas as pd
import os 
import fastf1 as ff
from time import time
import driver_trace
import trace_options
import fastf1SessionLoad

import mpld3
import streamlit.components.v1 as components


def yearList():
    yearList = os.listdir("cache")
    print(yearList.sort())
    return yearList   

schedule = pd.read_parquet("./races_by_year.pq")

def generateRaceList(year):
    df = schedule
    raceList = pd.DataFrame(df[df['EventYear']==year]['EventName'])
    # df[df["team"].str.contains("Team 1") == False]
    print("Printing racelist ")
    
    raceList = raceList[raceList['EventName'].str.contains("Pre") == False]
    print(raceList)
    return raceList

lapTimingDetails = ""

tab1, tab2= st.tabs(["Race Summary","Driver Analysis"])

if 'responsePacket' not in st.session_state:
    responsePacket = {}
    responsePacket['maxSpeed'] = ""
    responsePacket['tyreCompound'] = ""
    responsePacket['gridPosition'] = ""
    responsePacket['lapNumber'] = "int(driver1_lap['LapNumber'].item())"
    st.session_state['responsePacket'] = responsePacket

with st.sidebar:
    with st.expander("Select Race to begin analysis."):
        with st.form("New form"):
            yearSelect = st.selectbox("Enter year", options = ['2024', '2023', '2022', '2021', '2020', '2019'])
            st.form_submit_button("Select Year.")
            st.session_state['yearSel'] = yearSelect

        
        if yearSelect:
            raceList = generateRaceList(yearSelect)    
            st.session_state['raceList'] = raceList
            raceSelect = st.radio(label = "Pick Race", options=raceList)
            if raceSelect:
                print(f"Race picked {raceSelect}")
            # submitRaceSelect = st.button("Let's Go.")

        with st.form("New form 2"):
            # raceSelect = st.selectbox(f"Select Race for {yearSelect}:", raceList)
            # st.session_state['raceSelect'] = raceSelect
            submitRaceSelect = st.form_submit_button("Let's go!")
        
            if submitRaceSelect:
                st.session_state['raceSelect'] = raceSelect
                if 'sessionObj' not in st.session_state:
                    sessionObj = fastf1SessionLoad.loadSession(int(yearSelect), raceSelect)
                    st.session_state['sessionObj'] = sessionObj
                    sessionObj=st.session_state.get('sessionObj')
                    driverList = sessionObj.results.Abbreviation
                    st.session_state['driverList'] = sessionObj.results.Abbreviation
                    driverWinner = sessionObj.results.Abbreviation[0]
                    st.session_state['driverWinner'] = driverWinner
                    scatterplot = driver_trace.scatterPlot(driverSel=st.session_state.get('driverWinner'))
                    st.session_state['scatterplot'] = scatterplot
                    
                else:
                    print("In else")
                    sessionObj = fastf1SessionLoad.loadSession(int(st.session_state['yearSel']), st.session_state['raceSelect'])
                    st.write("Race loaded.")
                    st.session_state['sessionObj'] = sessionObj
                    st.session_state['driverList'] = sessionObj.results.Abbreviation
                    driverWinner = sessionObj.results.Abbreviation[0]
                    st.session_state['driverWinner'] = driverWinner
                    print("Who won",driverWinner)
                    scatterplot = driver_trace.scatterPlot(driverSel=st.session_state.get('driverWinner'))
                    st.session_state['scatterplot'] = scatterplot
           
with tab2:
        driverList = st.session_state.get("driverList")
        driverSel = st.session_state.get("driverSel")
        scatterplot = st.session_state.get('scatterplot')

        try:
            with st.container():
                coln1, coln2 = st.columns(2)
                with coln1:
                    driverSel = st.selectbox("Pick Driver", options = driverList)
                    totalLaps = int(max((st.session_state.get('sessionObj')).laps.pick_driver(driverSel)['LapNumber']))
                    st.write(f"{driverSel} completed {totalLaps} laps at this race.")

                with coln2:
                    lapSelect = st.text_input("Enter Lap Number")
            
            col1, col2, col3= st.columns(3)
            with col1:
                scatterplotButton = st.button("Lap Times Distribution")
                st.session_state['driverSel'] = driverSel
                print(f"selected driver {driverSel}")
                print("Col 1")

            with col2:
                fastestLap = st.button("Speed Trace for Fastest Lap")
                st.session_state["lapSelect"] = lapSelect
                print("Col 2")
            
            with col3:
                buildViz = st.button("Custom Lap")

                print("Col 3")
            if driverSel:
                sessionObj = st.session_state.get("sessionObj")
                print(f"Printing scatterplot")
                # st.session_state['responseObj'] = driver_trace.plotTraces(driverSel)
                scatterplot = driver_trace.scatterPlot(driverSel=st.session_state.get('driverSel'))
                print(st.session_state.get('responseObj'))

            

                if fastestLap:
                    sessionObj = st.session_state.get("sessionObj")
                    print(f"{driverSel}'s Fastest Lap.")
                    st.session_state['responseObj'] = driver_trace.plotTraces(sessionObj, driverSel, st.session_state.get('yearSel'), st.session_state.get('raceSelect'))
                
                if buildViz:
                    sessionObj = st.session_state.get("sessionObj")
                    print(f"Building custom lap {lapSelect}")
                    st.session_state['responseObj'] = driver_trace.plotTraces(sessionObj, driverSel, st.session_state.get('yearSel'), st.session_state.get('raceSelect'), st.session_state.get('lapSelect'))


        except Exception as e:
            st.write("Pick race")
        try:
            print("Got response object")
            st.set_option('deprecation.showPyplotGlobalUse', False)

            responseObj = st.session_state.get('responseObj')
            print("failing here?")
            responsePacket = responseObj['packet']
            lapMetrics = pd.DataFrame.from_dict([responsePacket])
            st.session_state['lapMetrics'] = lapMetrics
            print("printed dataframe")
            if responsePacket['chartType'] == "timeTrace":  
                    try:
                        print("try to read return")
                        st.pyplot((responseObj['plot']).show(), use_container_width=True)
                        print("printed scatterplot")
                    except Exception as e:
                        print("try to read return success")
                        print(e)
                    st.dataframe(lapMetrics)
                    print("Done with tis")
            
            else:
                print("entered here")   
                st.pyplot((responseObj['plot']).show(), use_container_width=True)
        except Exception as e:
            print("complete fail")
            print(e)
            st.write("Waiting...")

with tab1:
    try:
        if submitRaceSelect:   
            
            sessionObj = st.session_state.get('sessionObj')
            resultsDF = sessionObj.results
            raceWinner = sessionObj.results.FullName[0]
            st.header(f"    {yearSelect} {raceSelect}", divider="red")
            tab1c1, tab1c2, tab1c3 = st.columns(3)
            with tab1c2:
                st.image(sessionObj.results.HeadshotUrl[0])
                st.subheader(raceWinner)
        
        print(f"raceWinner {raceWinner}")
        st.dataframe(resultsDF[['TeamName','ClassifiedPosition', 'BroadcastName']], use_container_width=True, hide_index=True)
    except Exception as e:
        print(e)
        st.write("Waiting for user input")

