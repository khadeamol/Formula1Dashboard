from time import time
import matplotlib.pyplot as plt
import fastf1 as ff
import fastf1.plotting
import pandas as pd
import seaborn as sns 
import streamlit as st


fastf1.plotting.setup_mpl(misc_mpl_mods=False)
ff.Cache.enable_cache("cache")


def plotTraces(session, driver1, yearSel, raceSel, lapNumber = None):
    session = fastf1.get_session(int(yearSel), raceSel, 'R')
    responsePacket = {}
    if lapNumber:
        print("Custom lap")
        session = st.session_state.get("sessionObj")
        driver1_lap = session.laps.pick_driver(driver1).pick_lap(int(lapNumber))
        for k,v in driver1_lap['Compound'].items():
            responsePacket['tyreCompound'] = v
        print(f"Done custom lap {v}")
        for k,v in driver1_lap['LapTime'].items():
            try:
                responsePacket['lapTime'] = str(v)[-12:-3]
                print(f"V is {responsePacket['LapTime']}")
            except Exception as e:
                print(e)
    else:
        print("Fastest Lap")
        session = st.session_state.get("sessionObj")
        driver1_lap = session.laps.pick_driver(driver1).pick_fastest()
        responsePacket['tyreCompound'] = driver1_lap['Compound']
        responsePacket['lapTime'] = str(driver1_lap.LapTime)[-12:-3]
        print("Done fastest lap")
    
    driver1_tel = driver1_lap.get_car_data().add_distance()
    print(str(driver1_lap.LapTime)[-12:-3])
    
    responsePacket['maxSpeed'] = driver1_tel.Speed.max()
    responsePacket['averageSpeed'] = round(driver1_tel.Speed.mean(),3)
    responsePacket['gridPosition'] = int(driver1_lap['Position'].item())
    responsePacket['lapNumber'] = int(driver1_lap['LapNumber'].item())
    responsePacket['chartType'] = "timeTrace"
    st.session_state['responsePacket'] = responsePacket
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(driver1_tel['Distance'], driver1_tel['Speed'], color = fastf1.plotting.driver_color(driver1), label = driver1)

    ax.set_ylabel('Speed in km/h')
    
    circuit_info = session.get_circuit_info()


    v_min = driver1_tel['Speed'].min()
    v_max = driver1_tel['Speed'].max()
    ax.vlines(x=circuit_info.corners['Distance'], ymin=v_min-20, ymax=v_max+20,
          linestyles='solid', colors='blue')
    
    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"
        ax.text(corner['Distance'], v_min-30, txt,
                va='center_baseline', ha='center', size='small')
    
    
    plt.suptitle(f"Speed Trace with Turn annotations")
    print("Plot built")
    responsePacket['plotShow'] = plt.show()
    return responsePacket


def scatterPlot(driverSel):
    session = st.session_state.get('sessionObj')
    
    driverLaps = session.laps.pick_driver(driverSel).reset_index()
    driverLaps = driverLaps[driverLaps['TrackStatus']=='1']

    averageSpeed = driverLaps.pick_quicklaps().get_car_data().add_distance().Speed.values.mean()
    print(f"driverLaps{driverLaps}")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data= driverLaps,
                    x = "LapNumber",
                    y = "LapTime",
                    ax = ax, 
                    hue = "Compound",
                    palette=fastf1.plotting.COMPOUND_COLORS,
                    legend = 'auto')
    print("done with seaborn ")
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    ax.invert_yaxis()
    responsePacket = {}
    
    responsePacket['chartType'] = "scatterplot"
    responsePacket['plotShow'] = plt.show()
    fastestLap = str(driverLaps.LapTime.min())[-12:-3]
    responsePacket['fastestLap'] = fastestLap
    responsePacket['averageSpeed'] = round(averageSpeed,3)
    st.session_state['responsePacket'] = responsePacket
    return responsePacket
