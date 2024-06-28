from time import time
import matplotlib.pyplot as plt
import fastf1 as ff
import fastf1.plotting
import pandas as pd


fastf1.plotting.setup_mpl(misc_mpl_mods=False)
ff.Cache.enable_cache("Cache")


def fastestLapTrace(yearSel, raceSel, sessionSel, driver1, driver2):
    # Load session
    session = ff.get_session(yearSel, raceSel, sessionSel)
    session.load()
    driver1_lap = session.laps.pick_driver(driver1).pick_fastest()
    driver2_lap = session.laps.pick_driver(driver2).pick_fastest()
    
    driver1_tel = driver1_lap.get_car_data().add_distance()
    driver2_tel = driver2_lap.get_car_data().add_distance()
    
    fig, ax = plt.subplots(3, figsize=(12, 10))

    ax[0].plot(driver1_tel['Distance'], driver1_tel['Speed'], color = fastf1.plotting.driver_color(driver1), label = driver1)
    ax[0].plot(driver2_tel['Distance'], driver2_tel['Speed'], color = fastf1.plotting.driver_color(driver2), label = driver2)
    # ax.set_xlabel('Distance in m')
    ax[0].set_ylabel('Speed in km/h')

    ax[1].plot(driver1_tel['Distance'], driver1_tel['Throttle'], color = fastf1.plotting.driver_color(driver1), label = driver1)
    ax[1].plot(driver2_tel['Distance'], driver2_tel['Throttle'], color = fastf1.plotting.driver_color(driver2), label = driver2)
    # ax.set_xlabel('Distance in m')
    ax[1].set_ylabel('Throttle')

    ax[2].plot(driver1_tel['Distance'], driver1_tel['Brake'], color = fastf1.plotting.driver_color(driver1), label = driver1)
    ax[2].plot(driver2_tel['Distance'], driver2_tel['Brake'], color = fastf1.plotting.driver_color(driver2), label = driver2)
    ax[2].set_xlabel('Distance in m')
    # ax.set_ylabel('Brake')

    fig.legend(labels=[driver1, driver2])

    plt.suptitle(f"Lap traces")
    return plt.show()
    
    # driver1_lap = pd.DataFrame(driver1_lap)
    # return driver1_lap


# print(plot_traces(2024, 'Miami', 'Q', 'VER', 10))