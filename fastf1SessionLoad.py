import streamlit as st 
import pandas as pd

import fastf1 as ff
from time import time


def loadSession(yearSel, raceSel):
    session = ff.get_session(yearSel, raceSel, "R")
    st.session_state['sessionObj'] = session
    session.load()
    print("Session object loaded.")
    print(session)
    return session

