#version notes
#BETA v0.1: Initial attempt

print("Starting VPD's PO Download Generator!")
print("Importing data...")

import time
from datetime import date
today = str(date.today())

import pandas as pd
import os