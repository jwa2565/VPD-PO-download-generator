#version notes
#BETA v0.1: Initial attempt

print("Starting VPD's PO Download Generator!")
print("Importing data...")

import time
from datetime import date
today = str(date.today())

import pandas as pd
import os

df = pd.read_excel("VPD PO Download Spreadsheet V0.1.xlsx")


unSortedOrders = pd.DataFrame(columns = ["fullOrder#", "Component", "Length", "Position", "Color"])


print("Data import successful!")
print("Generating PO download files...")

def cleanDataFrame():
    
    #df["Order Number"] = df["Order Number"].fillna("empty") drop this one
    df["Type"] = df["Type"].fillna("VPD")
    #df["Frame Width"] = df["Frame Width"].fillna(12)
    #df["Frame Height"] = df["Frame Height"].fillna(12)
    #df["Color"] = df["Color"].fillna("WHWH")
    df["Customer"] = df["Customer"].fillna("###")
    df["Schedule Date"] = df["Schedule Date"].fillna("###")
    df["Destination"] = df["Destination"].fillna("###")
    df["Full Scannable Order Number"] = df["Full Scannable Order Number"].fillna("empty")
    
def calcPanelWidth(frameWidth):
    return (frameWidth/2.0) - .188

def calcPanelHeight(frameHeight):
    return frameHeight - 2.625

def addRows_VPD(fullOrderNum, frameWidth, frameHeight, color, position):
    panelWidth = calcPanelWidth(frameWidth)
    panelHeight = calcPanelHeight(frameHeight)
    
    newRow = [fullOrderNum, "Active Horizontal", panelWidth, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow
   
    
    newRow = [fullOrderNum, "Active Vertical", panelHeight, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow
    
    newRow = [fullOrderNum, "Inactive Horizontal", panelWidth, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow
    
    newRow = [fullOrderNum, "Inactive Vertical", panelHeight, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow
    
def addRows_VPDTransom():
    hi = "hihi"
    
def addRows_VPDFrameOnly():
    hi = "hihi"
    
def addRows_VPDActPanOnly(fullOrderNum, frameWidth, frameHeight, color, position):
    panelWidth = calcPanelWidth(frameWidth)
    panelHeight = calcPanelHeight(frameHeight)
    
    newRow = [fullOrderNum, "Active Horizontal", panelWidth, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow
   
    
    newRow = [fullOrderNum, "Active Vertical", panelHeight, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow 
    
def addRows_VPDInaPanOnly(fullOrderNum, frameWidth, frameHeight, color, position):
    panelWidth = calcPanelWidth(frameWidth)
    panelHeight = calcPanelHeight(frameHeight)
    
    newRow = [fullOrderNum, "Inactive Horizontal", panelWidth, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow
    
    newRow = [fullOrderNum, "Inactive Vertical", panelHeight, position, color]
    unSortedOrders.loc[len(unSortedOrders)] = newRow 

def fillUnsortedOrders():
    for i, rows in df.iterrows():
        if df.iloc[i]["Type"] == "VPD":
            addRows_VPD(df.iloc[i]["Full Scannable Order Number"], df.iloc[i]["Frame Width"], df.iloc[i]["Frame Height"], df.iloc[i]["Color"], i+1)
        
        if df.iloc[i]["Type"] == "VPD Transom":
            addRows_VPD(df.iloc[i]["Full Scannable Order Number"], df.iloc[i]["Frame Width"], df.iloc[i]["Frame Height"], df.iloc[i]["Color"], i+1)
        
        if df.iloc[i]["Type"] == "VPD FrameOnly":
            addRows_VPD(df.iloc[i]["Full Scannable Order Number"], df.iloc[i]["Frame Width"], df.iloc[i]["Frame Height"], df.iloc[i]["Color"], i+1)
        
        if df.iloc[i]["Type"] == "VPD ActivePanelOnly":
            addRows_VPD(df.iloc[i]["Full Scannable Order Number"], df.iloc[i]["Frame Width"], df.iloc[i]["Frame Height"], df.iloc[i]["Color"], i+1)
        
        if df.iloc[i]["Type"] == "VPD InactivePanelOnly":
            addRows_VPD(df.iloc[i]["Full Scannable Order Number"], df.iloc[i]["Frame Width"], df.iloc[i]["Frame Height"], df.iloc[i]["Color"], i+1)
    

cleanDataFrame()
fillUnsortedOrders()

colorsInOrder = unSortedOrders["Color"].unique()

#print(colorsInOrder)
for i, rows in unSortedOrders.iterrows():
    print("fullOrder#:", unSortedOrders.iloc[i]["fullOrder#"], 
          "Component:", unSortedOrders.iloc[i]["Component"],
          "Length:", unSortedOrders.iloc[i]["Length"],
          "Position:", unSortedOrders.iloc[i]["Position"],
          "Color:", unSortedOrders.iloc[i]["Color"],)


print(type(colorsInOrder))




#print(df)
#print(unSortedOrders) 
        

