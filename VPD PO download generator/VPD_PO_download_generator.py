
# version notes
# BETA v0.1: Initial attempt

print("Starting VPD's PO Download Generator!")
print("Importing data...")

import time
from datetime import date

today = str(date.today())

import pandas as pd
import os

df = pd.read_excel("VPD PO Download Spreadsheet V0.1.xlsx")


unSortedOrders = pd.DataFrame(
    columns=["fullOrder#", "Component", "Length", "Position", "Color"]
)
orderLists = pd.DataFrame(
    columns=["Color", "profileID", "orders", "highestUsedPosition"]
)

componentList = [
    "Active Horizontal",
    "Active Vertical",
    "Inactive Horizontal",
    "Inactive Vertical",
]

print("Data import successful!")
print("Generating PO download files...")


def cleanDataFrame():

    # df["Order Number"] = df["Order Number"].fillna("empty") drop this one
    df["Type"] = df["Type"].fillna("VPD")
    # df["Frame Width"] = df["Frame Width"].fillna(12)
    # df["Frame Height"] = df["Frame Height"].fillna(12)
    # df["Color"] = df["Color"].fillna("WHWH")
    df["Customer"] = df["Customer"].fillna("###")
    df["Schedule Date"] = df["Schedule Date"].fillna("###")
    df["Destination"] = df["Destination"].fillna("###")
    df["Full Scannable Order Number"] = df["Full Scannable Order Number"].fillna(
        "empty"
    )


def calcPanelWidth(frameWidth):
    return (frameWidth / 2.0) - 0.188


def calcPanelHeight(frameHeight):
    return frameHeight - 2.625


def addRows_VPD(fullOrderNum, frameWidth, frameHeight, color, position):

    panelWidth = calcPanelWidth(frameWidth)
    panelHeight = calcPanelHeight(frameHeight)

    for i in range(len(componentList)):
        newRow = [fullOrderNum, componentList[i], panelWidth, position, color]
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
            addRows_VPD(
                df.iloc[i]["Full Scannable Order Number"],
                df.iloc[i]["Frame Width"],
                df.iloc[i]["Frame Height"],
                df.iloc[i]["Color"],
                i + 1,
            )

        if df.iloc[i]["Type"] == "VPD Transom":
            addRows_VPD(
                df.iloc[i]["Full Scannable Order Number"],
                df.iloc[i]["Frame Width"],
                df.iloc[i]["Frame Height"],
                df.iloc[i]["Color"],
                i + 1,
            )

        if df.iloc[i]["Type"] == "VPD FrameOnly":
            addRows_VPD(
                df.iloc[i]["Full Scannable Order Number"],
                df.iloc[i]["Frame Width"],
                df.iloc[i]["Frame Height"],
                df.iloc[i]["Color"],
                i + 1,
            )

        if df.iloc[i]["Type"] == "VPD ActivePanelOnly":
            addRows_VPD(
                df.iloc[i]["Full Scannable Order Number"],
                df.iloc[i]["Frame Width"],
                df.iloc[i]["Frame Height"],
                df.iloc[i]["Color"],
                i + 1,
            )

        if df.iloc[i]["Type"] == "VPD InactivePanelOnly":
            addRows_VPD(
                df.iloc[i]["Full Scannable Order Number"],
                df.iloc[i]["Frame Width"],
                df.iloc[i]["Frame Height"],
                df.iloc[i]["Color"],
                i + 1,
            )


def generateOrderLists():  # makes all the lists needed, but its empty except the color
    colorsInOrders = unSortedOrders["Color"].unique()

    panelProfileIDList = [
        "VPDPAH1",  # VPD Active Panel, Horizontal pieces, 1 unit
        "VPDPAH2",  # VPD Active Panel, Horizontal pieces, 2 units
        "VPDPAV1",  # VPD Active Panel, Vertical pieces, 1 unit
        "VPDPAV2",  # VPD Active Panel, Vertical pieces, 2 units
        "VPDPSH1",  # VPD Stationary Panel, Horizontal pieces, 1 unit
        "VPDPSH2",  # VPD Stationary Panel, Horizontal pieces, 2 units
        "VPDPSV1",  # VPD Stationary Panel, Vertical pieces, 1 unit
        "VPDPSV2",  # VPD Stationary Panel, Vertical pieces, 2 units
        "VPDPBH2",  # VPD Both Active & Stationary Panels, Horizontal pieces, 2 units
        "VPDPBV2",  # VPD Both Active & Stationary Panels, Vertical pieces, 2 units
    ]

    for i in range(len(colorsInOrders)):
        for j in range(len(panelProfileIDList)):
            newList = [colorsInOrders[i], panelProfileIDList[j], [], 0]
            orderLists.loc[len(orderLists)] = newList

def initializeHighestUsedPosition():
    location = (
                    (orderLists["Color"] == unSortedOrders.iloc[0]["Color"]) & 
                    (orderLists["profileID"] == "VPDPAH2") 
                    )
    orderLists.loc[location, "highestUsedPosition"] = 1

def fillOrderLists():

    generateOrderLists()
    
    

    for i, rows in unSortedOrders.iterrows():

        pairFound = False
        searchPosition = i + 1
        searchEnd = len(unSortedOrders)
        matchPosition = -1

        while not pairFound and searchPosition < searchEnd:
            if (unSortedOrders.iloc[searchPosition]["Component"] == unSortedOrders.iloc[i]["Component"]
                and unSortedOrders.iloc[searchPosition]["Color"] == unSortedOrders.iloc[i]["Color"]
                and unSortedOrders.iloc[searchPosition]["Length"] == unSortedOrders.iloc[i]["Length"]
                ):

                pairFound = True
                matchPosition = searchPosition

            else:
                searchPosition = searchPosition + 1
                
        if unSortedOrders.iloc[i]["Component"] == componentList[0]: #    "Active Horizontal",
            if pairFound:
                location = (
                    (orderLists["Color"] == unSortedOrders.iloc[i]["Color"]) & 
                    (orderLists["profileID"] == "VPDPAH2") 
                    )
                newOrders = [ unSortedOrders.iloc[i],  unSortedOrders.iloc[matchPosition]   ]
                orderLists.loc[location, "orders"] = newOrders
                
            else:
                location = (
                    (orderLists["Color"] == unSortedOrders.iloc[i]["Color"]) & 
                    (orderLists["profileID"] == "VPDPAH1") 
                    )
                newOrder = [ unSortedOrders.iloc[i]]
                orderLists.loc[location, "orders"] = newOrder

                
            
        elif unSortedOrders.iloc[i]["Component"] == componentList[1]: #    "Active Vertical",
            jo1 = ""
            
        elif unSortedOrders.iloc[i]["Component"] == componentList[2]: #    "Inactive Horizontal",
            jo2 = ""
            
        elif unSortedOrders.iloc[i]["Component"] == componentList[3]: #    "Inactive Vertical",
            jo3 = ""
            
        
       


        

    # for i, rows in unSortedOrders.iterrows():
    #    print("fullOrder#", unSortedOrders.iloc[i]["fullOrder#"],
    #          "Component", unSortedOrders.iloc[i]["Component"],
    #          "Length", unSortedOrders.iloc[i]["Length"],
    #          "Position", unSortedOrders.iloc[i]["Position"],
    #         "Color", unSortedOrders.iloc[i]["Color"],
    #
    #     )

    # unSortedOrders = pd.DataFrame(columns = ["fullOrder#", "Component", "Length", "Position", "Color"])


    for i, rows in orderLists.iterrows():
        print("Color", orderLists.iloc[i]["Color"],
           "profileID", orderLists.iloc[i]["profileID"],
           "orders", orderLists.iloc[i]["orders"],
           "highestUsedPosition", orderLists.iloc[i]["highestUsedPosition"]
           )


# orderLists = pd.DataFrame(columns = ["Color","profileID","orders","highestUsedPosition"])


cleanDataFrame()
fillUnsortedOrders()
fillOrderLists()


# print(df)
# print(unSortedOrders)
