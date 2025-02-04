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
                    sessionObj = fastf1SessionLoad.loadSession(int(yearSelect), raceSelect)
                    st.session_state['sessionObj'] = sessionObj
                    st.write("Race loaded.")
                    sessionObj=st.session_state.get('sessionObj')
                    st.session_state['driverList'] = generateDriverList(sessionObj, yearSelect, raceSelect)        
                    
                else:
                    print("In else")
                    sessionObj = fastf1SessionLoad.loadSession(int(st.session_state['yearSel']), st.session_state['raceSelect'])
                    st.write("Race loaded.")
                    st.session_state['sessionObj'] = sessionObj
                    print(generateDriverList(sessionObj, yearSelect, raceSelect))
                    st.session_state['driverList'] = generateDriverList(sessionObj, yearSelect, raceSelect)        
        # st.write(driverList)

    with st.expander("Driver Analysis"):
        driverList = st.session_state.get("driverList")
        # if 'driverSel' not in st.session_state:
        try:
            driverSel = st.selectbox("Pick Driver", options = driverList)
            st.session_state['driverSel'] = driverSel
            maxLaps = int(max((st.session_state.get('sessionObj')).laps.pick_driver(driverSel)['LapNumber']))
            st.write(f"{driverSel} completed {maxLaps} laps at this race.")
            with st.form("Lap Selection:"):
                lapSelect = st.text_input("Enter Lap Number to analyze, or hit Pick Fastest", "")
                st.session_state["lapSelect"] = lapSelect
                buildViz = st.form_submit_button("Build Visualization")
            if buildViz:
                if lapSelect != "":
                    sessionObj = st.session_state.get("sessionObj")
                    st.write(f"{st.session_state.get('lapSelect')}")
                    
                    st.session_state['responsePacket'] = {}
                    st.session_state['responsePacket'] = driver_trace.plotTraces(sessionObj, driverSel, st.session_state.get('yearSel'), st.session_state.get('raceSelect'), st.session_state.get('lapSelect'))

                elif lapSelect == "":
                    sessionObj = st.session_state.get("sessionObj")
                    print(f"{driverSel}'s Fastest Lap.")
                    responsePacket = driver_trace.plotTraces(sessionObj, driverSel, st.session_state.get('yearSel'), st.session_state.get('raceSelect'))
                    st.session_state['lapTimingDetails'] = lapTimingDetails
        except:
            st.write("Waiting for user input.")


    with st.expander("Driver Comparison"):
        sessionObj = st.session_state.get('sessionObj')
        driverList = st.session_state.get('driverList')
        try:
            driverSel1 = st.selectbox("Select Driver 1", options = driverList)
        except:
            driverSel1 = st.selectbox("Select Driver 1", options = [])

        try:
            driverSel2 = st.selectbox("Select Driver 2", options = driverList)
        except:
            driverSel2 = st.selectbox("Select Driver 2", options = [])

        resetButton = st.button("Reset")
        if resetButton:
            st.session_state.clear()
try:
    responsePacket = st.session_state.get('responsePacket')
    print("break after")
    # for i in st.session_state.items():
    #     st.write(i)
    if 'responsePacket' in st.session_state:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(responsePacket['plotShow'], use_container_width=True)
        st.write(f"Lap Number: {responsePacket['lapNumber']}")
        st.write(f"Maximum Speed: {responsePacket['maxSpeed']}")
        st.write(f"Tyre Compound: {responsePacket['tyreCompound']}")
        st.write(f"Grid Position: {responsePacket['gridPosition']}")
        print("Does it break ere")
        scatterplot = st.button("Scatterplot")
        if scatterplot:
            print("entered scatterplot if case")
            scatterplot = driver_trace.scatterPlot(responsePacket['sessionObj'],driverSel=st.session_state.get('driverSel'))
            print("Came back with plot")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(scatterplot, use_container_width=True)
        else:
            print("bop bop")
    else:
        st.write("Waiting for user")
except:
    st.write("Waiting...")


# try:
#     if vizButton:
#         sessionObj = st.session_state.get("sessionObj")
#         print(f"Working on lap {st.session_state.get('lapSelect')}")
#         lapTimingDetails = driver_trace.plotTraces(sessionObj, driverSel, st.session_state.get('yearSel'), st.session_state.get('raceSelect'), st.session_state.get('lapSelect'))
#         st.set_option('deprecation.showPyplotGlobalUse', False)
#         print("Did it get here")
#         st.pyplot(lapTimingDetails, use_container_width=True)
# except:
#         st.write("")

# try:
#     if fastestLap:
#         sessionObj = st.session_state.get("sessionObj")
#         lapTimingDetails = driver_trace.plotTraces(sessionObj, driverSel, st.session_state.get('yearSel'), st.session_state.get('raceSelect'))
#         st.set_option('deprecation.showPyplotGlobalUse', False)
#         print("Did it get here")
#         st.pyplot(lapTimingDetails, use_container_width=True)
# except:
#         st.write("")



# with tab1:
#     lapSel = st.text_input("Enter Lap Number. Defaults to fastest lap.", "Fastest Lap.")
#     goButton = st.button("Let's Go!")
#     if goButton:
#         print("Driver selected:", driverSel)
#         st.write(f"Selected Lap for {driverSel} at {st.session_state.get('yearSel')} {st.session_state.get('raceSelect')}")
#         lapTimingDetails = driver_trace.plotTraces(sessionObj, driverSel, st.session_state.get('yearSel'), st.session_state.get('raceSelect'))
#         st.set_option('deprecation.showPyplotGlobalUse', False)
#         st.pyplot(lapTimingDetails, use_container_width=True)


# with tab2:


#     if driverSel1 == driverSel2:
#         st.write("Please select two different drivers.")
#     else:
#         if 'lapSelect' not in st.session_state:
#             st.session_state['lapSelect'] = st.text_input("Enter lap to compare. Defaults to fastest lap.")
        
#         goButton = st.button("Compare Laps.")
#         if goButton:

#             st.write(f"Comparing selected lap {driverSel1} and {driverSel2} at {st.session_state.get('yearSel')} {st.session_state.get('raceSelect')}")
#             lapsCompared = trace_options.fastestLapTrace(sessionObj, driverSel1, driverSel2, st.session_state.get('lapSelect'))
#             st.set_option('deprecation.showPyplotGlobalUse', False)
#             st.pyplot(lapsCompared, use_container_width=True)


# with tab3:
#     with st.expander("New"):
#         with st.form("Test form"):
#             expnd = st.text_input("Write here")
#             btn = st.form_submit_button("Go")
#             if btn:
#                 st.write(expnd)

#     featureSelect = st.selectbox("Choose option", options = ['Lap Trace', 'Lap Time Scatterplot'])

#     if featureSelect == 'Lap Trace':
#     elif featureSelect == 'Lap Time Scatterplot':
#         st.write("First option")
#         st.write("Second option")