import streamlit as st 
import pandas as pd

import fastf1 as ff
from time import time


def loadSession(yearSel, raceSel):
    session = ff.get_session(yearSel, raceSel, "R")
    session.load()
    return session