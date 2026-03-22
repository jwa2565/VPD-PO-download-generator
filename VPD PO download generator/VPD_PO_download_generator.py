# version notes
# BETA v0.1: Initial attempt

# BETA v1.1: Working prototype!!!!!!!!! If anybody besides me reviews this - know that this might be messy because it had to be developed rapidly to be ready for FATs
#            I made this keeping in mind I might have to use this as an emergency plan B for production launch, 
#            so I've taken adequate measures aread of time to streamline this process more. I've taken 1500-5's 
#            quality of life improvements and implemented them here.... because the I still cry about the overwhelm 
#            during the 1500-5 launch :') XD jk no but really. 
#
#            Note to self: If I could figure out a better way to input the data from Atlas into the program, that would 
#            be a game changer. Future research should involve accessing SQL databases through my programs

print("Starting VPD's PO Download Generator!")
print("Importing data...")
import pandas as pd
import random
import time
import os

from datetime import date
today = str(date.today())

from PanelGenerator import PanelGenerator
from FrameGenerator import FrameGenerator

excelFileName = "VPD PO Download Spreadsheet v1.1.xlsx"

df = pd.read_excel(excelFileName)

cartID = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
cartBin = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Data import successful!")
print("Generating PO download files...") 


def cleanDataFrame():
    
    df["Full Scannable Order Number"] = df["Full Scannable Order Number"].fillna("empty")
    df["Type"] = df["Type"].fillna("VPD (P2)")
    df["Frame Width"] = df["Frame Width"].fillna("2-6")
    df["Frame Height"] = df["Frame Height"].fillna("1-2")
    df["Color"] = df["Color"].fillna("WHWH")
    df["Customer"] = df["Customer"].fillna("###")
    df["Schedule Date"] = df["Schedule Date"].fillna("###")
    df["Destination"] = df["Destination"].fillna("###")
    df["Handing"] = df["Handing"].fillna("RH")
    
def detFileNameParameters():
    fileNameDate = ""
    counter = "1"
    
    #####################stuff for filename
    if df.iloc[0]["Schedule Date"] == "###":
        fileNameDate = today
    
    else:
        fileNameDate = df.iloc[0]["Schedule Date"].strftime("%Y-%m-%d")
        
    #######################stuff for counter
    countConfig = "countConf.jo"

    if not os.path.exists(countConfig): #make config file if not there
        countConfigFile = open("countConf.jo", "w")
        countConfigFile.write("Date: " + today + "\n")
        countConfigFile.write("Count: " + "1" + "\n")
        countConfigFile.close()
        

    #get current values from config file
    countConfigFile = open("countConf.jo", "r")
    currentDateInConfig = countConfigFile.readline()
    currentCountInConfig = countConfigFile.readline()

    currentDateInConfig = currentDateInConfig.replace("Date: ", "")
    currentCountInConfig = currentCountInConfig.replace("Count: ", "")
    currentDateInConfig = currentDateInConfig.replace("\n", "")
    currentCountInConfig = currentCountInConfig.replace("\n", "")

    countConfigFile.close()
    

    #Update parameters in config file
    if currentDateInConfig != fileNameDate:
        currentDateInConfig = fileNameDate
        currentCountInConfig = "1"
        
    counter = currentCountInConfig
    currentCountInConfig = str(int(currentCountInConfig)+1)

    countConfigFile = open("countConf.jo", "w")
    countConfigFile.write("Date: " + currentDateInConfig + "\n")
    countConfigFile.write("Count: " + currentCountInConfig + "\n")
    countConfigFile.close()


    return fileNameDate, counter
    
def insertColumn_BIN(): #Ok not actually a bin, but stuff to generate bin
    df["cartID"] = "###"
    df["cartBin"] = 0
    
    currentCartIDIndex = 0
    currentCartBinIndex = 0
    
    for i, rows in df.iterrows():
        
        df.loc[i, "cartID"] = cartID[currentCartIDIndex]
        df.loc[i, "cartBin"] = cartBin[currentCartBinIndex]

        currentCartBinIndex = currentCartBinIndex + 1
        if (currentCartBinIndex/len(cartBin)) >= 1: #Move to the next WIP cart
            currentCartBinIndex = currentCartBinIndex % len(cartBin)
            currentCartIDIndex = (currentCartIDIndex + 1) % len(cartID)
            
def insertColumn_panelComponents(): 
    df["panelComponentsNeeded"] = 0
    df["panelComponentsCut"] = 0
    
def insertColumn_frameWelderQRCode():
    df["frameWelderQRCode"] = "###"
    
def insertColumn_panelWelderQRCode():
    df["panelWelderQRCode"] = "###"
        
def randomCustomerGenerator(): ##nvm probs don't use

    randomCustomerList = []
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")
    randomCustomerList.append("Joseph Amaya")

    randIndex = random.randint(0,len(randomCustomerList))
    randCustomer = randomCustomerList[randIndex]

    return randCustomer

cleanDataFrame()
insertColumn_BIN()
insertColumn_panelComponents()

fileNameDate, fileCounter = detFileNameParameters()

PanelGenerator(df, fileNameDate, fileCounter)
FrameGenerator(df, fileNameDate, fileCounter)

print("PO download files generated! You're welcome")
time.sleep(3)
print("Byeee")
time.sleep(1)