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
    Metal
        21690=Brittle Clump of Ore
        21678=Bit of Metal Scrap
        21691=Weak Clump of Ore

        21679=Pile of Metal Scrap
        21692=Clump of Ore
        21680=Jagged Metal Scrap

        21693=Laden Clump of Ore
        21681="Metal Scrap
        21694=Loaded Clump of Ore

        21682=Salvageable Metal Scrap
        21695=Rich Clump of Ore
        21683=Valuable Metal Scrap

        79079=Unstable Metal Chunk


    Leather
        21661=Tattered Hide
        21684=Rawhide Leather Strap
        21653=Tattered Pelt

        21664=Ripped Hide
        21685=Thin Leather Strap
        21654=Ripped Pelt

        21667=Torn Hide
        21686=Coarse Leather Strap
        21655=Torn Pelt

        21668=Frayed Hide
        21687=Thick Leather Strap
        21656=Frayed Pelt

        21670=Filthy Hide
        21688=Rugged Leather Strap
        21657=Filthy Pelt

        22331=Salvageable Hide
        21689=Hard Leather Strap
        21658=Salvageable Pelt

    Cloth
        aaaaa


    Wood
        79423=Reclaimed Wood Chunk


Direct salvage output material:
    Metal
        19697=Copper Ore
        19703=Silver Ore
        19699=Iron Ore
        19698=Gold Ore
        19702=Platinum Ore
        19700=Mithril Ore
        19701=Orichalcum Ore

    Leather
        19719=Rawhide Leather Section
        19728=Thin Leather Section
        19730=Coarse Leather Section
        19731=Rugged Leather Section
        19729=Thick Leather Section
        19732=Hardened Leather Section

    Cloth
        aaaaaaaaaa

    Wood
        19723=Green Wood Log


Refinement materials:
    Metal
        19680=Copper Ingot
        19679=Bronze Ingot
        19687=Silver Ingot
        19683=Iron Ingot
        19688=Steel Ingot
        19682=Gold Ingot
        19686=Platinum Ingot
        19681=Darksteel Ingot
        19684=Mithril Ingot
        19685=Orichalcum Ingot

    Leather
        19738=Stretched Rawhide Leather Square
        19733=Cured Thin Leather Square
        19734=Cured Coarse Leather Square
        19736=Cured Rugged Leather Square
        19735=Cured Thick Leather Square
        19737=Cured Hardened Leather Square

    Cloth
        aaaaaaa

    Wood


Additional refinement materials:
    =Lump of Tin
    19750=Lump of Coal
    19924=Lump of Primordium

"""

"""Refinement Equations

Metal:
    1x Copper Ingot = 2x Copper Ore
    5x Bronze Ingot = 10x Copper + Lump of Tin
    1x Silver Ingot = 2x Silver Ore
    1x Iron Ingot = 3x Iron Ore
    1x Steel Ingot = 3x Iron Ore + 1x Lump of Coal
    1x Gold Ingot = 2x Gold Ore
    1x Platinum Ingot = 2x Platinum Ore
    1x Darksteel Ingot = 2x Platinum Ore + Lump of Primordium
    1x Mithril Ingot = 2x Mithril Ore
    1x Orichalcum Ingot = 2x Orichalcum Ore

Leather
    1x Stretched Rawhide Leather Square = 2x Rawhide Leather Section
    1x Cured Thin Leather Square = 2x Thin Leather Section
    1x Cured Coarse Leather Square = 2x Coarse Leather Square
    1x Cured Rugged Leather Square = 2x Rugged Leather Square
    1x Cured Thick Leather Square = 4x Thick Leather Section
    1x Cured Hardened Leather Square = 3x Hardened Leather Section

Cloth
    1x

Wood
    1x

"""

"""Salvage results

The wiki sometimes indicates a number for each possible salvage result
Specific numbers of salvage per salvage item doesn't really matter - want average value

Metal Salvage:
    Metal
        Brittle Clump of Ore = (1-3) Copper Ore
        Bit of Metal Scrap = (1-3) Copper Ore
        Weak Clump of Ore = (1-3) Copper Ore + (1-3) Silver Ore + (1-3) Iron Ore
        Pile of Metal Scrap = (1-3) Copper Ore + (1-3) Silver Ore + (1-3) Iron Ore
        Clump of Ore = (1-3) Silver Ore + (1-3) Iron Ore + (1-3) Gold Ore
        Jagged Metal Scrap = (1-3) Silver Ore + (1-3) Iron Ore + (1-3) Gold Ore
        Laden Clump of Ore = (1-3) Iron Ore + (1-3) Gold Ore + (1-3) Platinum Ore
        Metal Scrap = (1-3) Iron Ore + (1-3) Gold Ore + (1-3) Platinum Ore
        Loaded Clump of Ore = (1-3) Platinum Ore + (1-3) Mithril Ore
        Salvageable Metal Scrap = (1-3) Platinum Ore + (1-3) Mithril Ore
        Rich Clump of Ore = (1-3) Mithril Ore + (?0-1?) Orichalcum Ore
        Valuable Metal Scrap = (1-3) Mithril Ore + (?0-1?) Orichalcum Ore
        Unstable Metal Chunk = Copper, Iron, Platinum, Mithril, Orichalcum (no gold or silver apparently)

    Leather
        Tattered Hide = (1-3) Rawhide Leather Section
        Rawhide Leather Strap = (1-3) Rawhide Leather Section
        Tattered Pelt = (1-3) Rawhide Leather Section
        Ripped Hide = (1-3) Rawhide Leather Section + (1-3) Thin Leather Section
        Thin Leather Strap = (1-3) Rawhide Leather Section + (1-3) Thin Leather Section
        Ripped Pelt = (1-3) Rawhide Leather Section + (1-3) Thin Leather Section
        Torn Hide = (1-3) Thin Leather Section + (1-3) Coarse Leather Section
        Coarse Leather Strap = (1-3) Thin Leather Section + (1-3) Coarse Leather Section
        Torn Pelt = (1-3) Thin Leather Section + (1-3) Coarse Leather Section
        Frayed Hide = (1-3) Coarse Leather Section + (1-3) Rugged Leather Section
        Thick Leather Strap = (1-3) Coarse Leather Section + (1-3) Rugged Leather Section
        Frayed Pelt = (1-3) Coarse Leather Section + (1-3) Rugged Leather Section
        Filthy Hide = (1-3) Rugged Leather Section + (1-3) Thick Leather Section
        Rugged Leather Strap = (1-3) Rugged Leather Section + (1-3) Thick Leather Section
        Filthy Pelt = (1-3) Rugged Leather Section + (1-3) Thick Leather Section
        Salvageable Hide = (1-3) Thick Leather Section + Hardened Leather Section
        Hard Leather Strap = (1-3) Thick Leather Section + Hardened Leather Section
        Salvageable Pelt = (1-3) Thick Leather Section + Hardened Leather Section
        Unstable Hide = Rawhide, Thin Leather, Coarse, Rugged, Thick, Hardened
        Bloodstone-Warped Hide = Rawhide, Thin Leather, Coarse, Rugged, Thick, Hardened

    Cloth
        Shredded Garment
        Half-Eaten Mass
        Shredded Rag
        Worn Garment
        Decaying Mass
        Worn Rag
        Ragged Garment
        Fetid Mass
        Soiled Rag
        Frayed Garment
        Malodorous Mass
        Frayed Rag
        Torn Garment
        Half-Digested Mass
        Torn Rag
        Discarded Garment
        Regurgitated Mass
        Rag
        Unstable Rag

    Wood
        Reglaimed Wood Chunk = Green, Soft, Seasoned, Hard, Elder, Ancient

    Rare Metal Salvage
        Bit or Aetherized Metal
        Bit of Fused Metal Scrap
        Bit of Twisted Watchwork Scrap
        Pile of Aetherized Metal Scrap
        Pile of Fused Metal Scrap
        Pile of Twisted Watchwork Scrap
        Jagged Aetherized Metal Scrap
        Jagged Fused Metal Scrap
        Jagged Twisted Watchwork Scrap
        Aetherized Metal Scrap
        Fused Metal Scrap
        Twisted Watchwork Scrap
        Salvageable Aetherized Metal Scrap
        Salvageable Fused Metal Scrap
        Salvageable Twisted Watchwork Scrap

"""


# Requires the Python GW2 API wrapper library


#Get prices
    #Call GW2 API wrapper to get the prices of all items
    #Organize the TP values somehow
def getMetal():
    #api call for all metal TP prices
    #separate into base and refined
    #return format is a dict
    return


def getLeather():
    #api call for all metal TP prices
    #separate into base and refined
    #return format is a dict
    return


def getCloth():
    #api call for all metal TP prices
    #separate into base and refined
    #return format is a dict
    return


def getWood():
    #api call for all metal TP prices
    #separate into base and refined
    #return format is a dict
    return


def compareRefined():
    #compare prices of raw vs refined
    #separate buy and sell listings for reference because time is also money
    return


def calculateSalvage():
    #calculate the average value of the salvage item - buy and sell
    return


def getProfit():
    #calculate the profit of each salvage item using refined/unrefined options
    return


def printReport():
##not sure if lumping all the material values at once is better or repeat per item

    #CLEARLY state if item is profitable to cost
    #state profit or lack thereof
    #state cost of salvage item and average value of salvage output
    #state material values
    #state if refined is more profitable, and by how much
    return
