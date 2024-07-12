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
        print(session)
        driver1_lap = session.laps.pick_driver(driver1).pick_lap(int(lapNumber))

    else:
        print("Fastest Lap")
        session = st.session_state.get("sessionObj")
        driver1_lap = session.laps.pick_driver(driver1).pick_fastest()
        
    
    driver1_tel = driver1_lap.get_car_data().add_distance()
    print(f"{driver1_lap} driver's lap")
    responsePacket['maxSpeed'] = driver1_tel.Speed.max()
    responsePacket['tyreCompound'] = driver1_lap['Compound'].item()
    responsePacket['gridPosition'] = int(driver1_lap['Position'].item())
    responsePacket['lapNumber'] = int(driver1_lap['LapNumber'].item())
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
    
    
    # ax[1].plot(driver1_tel['Distance'], driver1_tel['Throttle'], color = fastf1.plotting.driver_color(driver1), label = driver1)
    # ax[1].set_ylabel('Throttle')
    # ax[2].plot(driver1_tel['Distance'], driver1_tel['Brake'], color = fastf1.plotting.driver_color(driver1), label = driver1)
    # ax[2].set_ylabel('Brake')
    # ax[2].set_xlabel('Distance in m')
    
    plt.suptitle(f"Speed Trace with Turn annotations")
    print("Plot built")
    responsePacket['plotShow'] = plt.show()
    return responsePacket


def scatterPlot(session,driverSel):
    session.load()
    driverLaps = session.laps.pick_driver(driverSel).pick_quicklaps().reset_index()
    print(f"driverLaps{driverLaps}")
    fig, ax = plt.subplots(figsize = (8,8))

    sns.scatterplot(data= driverLaps,
                    x = "LapNumber",
                    y = "LapTime",
                    ax = ax, 
                    hue = "Compound",
                    palette=fastf1.plotting.COMPOUND_COLORS,
                    linewitdh = 0,
                    legend = 'auto')

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    ax.invert_yaxis()
    print("Generated scatterplot")


    return plt.show()