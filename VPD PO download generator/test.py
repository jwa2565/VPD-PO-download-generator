
#ok this is me testing how to split code into different files. 
#This was a test but ima just go ahead and use this file tor printing stuff lol



def printOrderList(orderLists):
    print("Printing orderLists")
    for i in range(len(orderLists)):
        print("color", orderLists[i].color,
              "profileID", orderLists[i].profileID,
              "highestUsedPosition", orderLists[i].highestUsedPosition)
        for j in range(len(orderLists[i].orders)):
            print(j,
                  "Order1:", orderLists[i].orders[j].order1.fullOrderNum,
                  "Order2:", orderLists[i].orders[j].order2.fullOrderNum)
            
def printCutList(cutList):
    print("Printing cutList")
    for i in range(len(cutList)):
        print("color", cutList[i].color,
              "profileID", cutList[i].profileID,
              "highestUsedPosition", cutList[i].highestUsedPosition)
        for j in range(len(cutList[i].orders)):
            print(j,
                  "Order1:", cutList[i].orders[j].order1.fullOrderNum,
                  "Order2:", cutList[i].orders[j].order2.fullOrderNum)

def printUnsortedOrders(unsortedOrders):
    print("Printing unsortedOrders")
    for i in range(len(unsortedOrders)):
        print("fullOrderNum", unsortedOrders[i].fullOrderNum,
              "component", unsortedOrders[i].component,
              "length", unsortedOrders[i].length,
              "position", unsortedOrders[i].position,
              "color", unsortedOrders[i].color)