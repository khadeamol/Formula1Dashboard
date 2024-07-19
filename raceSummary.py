from time import time
import matplotlib.pyplot as plt
import fastf1 as ff
import fastf1.plotting
import pandas as pd
import seaborn as sns 
import streamlit as st


fastf1.plotting.setup_mpl(misc_mpl_mods=False)


def lapTimeViolinPlot():
    fig, ax = plt.subplots(figsize=(12,6))
    sessionObj = st.session_state.get('sessionObj')
    top10finishers = sessionObj.results[:10]['Abbreviation']
    driverLaps = sessionObj.laps.pick_drivers(top10finishers).pick_quicklaps()
    # print(f"driverLaps {driverLaps}")
    # Seaborn doesn't have proper timedelta support
    # so we have to convert timedelta to float (in seconds)
    driverLaps["LapTime(s)"] = driverLaps["LapTime"].dt.total_seconds()
    # print(driverLaps["LapTime(s)"] )
    sns.violinplot(data=driverLaps,
                   x="Driver",
                   y="LapTime(s)",
                   hue = None,
                   inner=None,
                   density_norm="area",
                   order=top10finishers,
                   gap = 1
                   )
    
    sns.swarmplot(data=driverLaps,
                  x="Driver",
                  y="LapTime(s)",
                  order=top10finishers,
                  hue="Compound",
                  palette=fastf1.plotting.COMPOUND_COLORS,
                  hue_order=["SOFT", "MEDIUM", "HARD"],
                  linewidth=0,
                  size=4)
    
    ax.set_xlabel("Driver")
    ax.set_ylabel("Lap Time (s)")
    plt.suptitle("2023 Azerbaijan Grand Prix Lap Time Distributions")
    sns.despine(left=True, bottom=True)
    
    plt.tight_layout()
    return plt.show()

# plotTraces()
