#This is a basic starter script for figuring out salvaging calculations in GW2
"""Basic salvage cost calculating in GW2

1)Buy salvage items
2)Salvage
3)Compare cost of raw or refined material
4)Sell material

You only want to do this if profitable


To determine if it is profitable:

salvage item + cost to salvage < value of goods after TP fees


To calculate the value of the goods after TP fees, I need:
Salvage rates
Value of raw salvage materials
Value of refined salvage materials
TP fees on items (fixed percentage)
Cost to salvage (fixed value per method)
"""

"""Program Flow

This first attempt is very fixed so it will be very stupid
Do not worry about what happens if you reduce the cost by 1c here and there


Call function to get get TP values
Call function to get list of materials to refine for better profit
Call function to determine average value of salvage item 
Call function to compare cost vs value of item
Call function to output final report
"""

"""API item and number

Salvage items:
    21690=Brittle Clump of Ore
    21678=Bit of Metal Scrap
    21691=Weak Clump of Ore
    
    safd

Direct output material:
    19697=Copper Ore
    19703=Silver Ore
    19699=Iron Ore

"""

"""Salvage results

    Brittle Clump of Ore = (1-3) Copper Ore
    Bit of Metal Scrap = (1-3) Copper Ore
    Weak Clump of Ore = (1-3) Copper Ore + (1-3) Iron Ore + (1-3) Silver Ore
    

"""

"""Refinement

    Copper Ingot = 2x Copper Ore
    5x Bronze Ingot = 10x Copper + Lump of Tin
    
2 mithril ore = 1 mithril ingot
sdfgjhfgdhdfgh

"""

# Requires the Python GW2 API wrapper library 

def getPrices:
    #Call GW2 API wrapper to get the prices of all items
    #Organize the TP values somehow

def compareRefined:
    #compare prices of raw vs refined
    #separate buy and sell listings for reference because time is also money

def calculateSalvage:
    #calculate the average value of the salvage item - buy and sell 

def getProfit:
    #calculate the profit of each salvage item using refined/unrefined options

def printReport:
##not sure if lumping all the material values at once is better or repeat per item

    #CLEARLY state if item is profitable to cost
    #state profit or lack thereof
    #state cost of salvage item and average value of salvage output
    #state material values
    #state if refined is more profitable, and by how much
