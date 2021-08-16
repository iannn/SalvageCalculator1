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
Call function to output final report - profit y/n
"""

"""API item and number

Salvage items:
    Metal Salvage
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


    Leather Salvage
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

        79213=Unstable Hide
        80681=Bloodstone-Warped Hide


    Cloth Salvage
        21669=Shredded Garment
        22325=Half-Eaten Mass
        21659=Shredded Rag

        21671=Worn Garment
        22326=Decaying Mass
        21660=Worn Rag

        21672=Ragged Garment
        22327=Fetid Mass
        21662=Soiled Rag

        21673=Frayed Garment
        22328=Malodorous Mass
        21663=Frayed Rag

        21674=Torn Garment
        22329=Half-Digested Mass
        21665=Torn Rag

        79138=Unstable Rag


    Wood Salvage
        79423=Reclaimed Wood Chunk


    Rare Metal Salvage
        43552=Bit of Aetherized Metal Scrap
        41733=Bit of Fused Metal Scrap
        45039=Bit of Twisted Watchwork Scrap

        43553=Pile of Aetherized Metal Scrap
        41734=Pile of Fused Metal Scrap
        45040=Pile of Twisted Watchwork Scrap

        43554=Jagged Aetherized Metal Scrap
        41735=Jagged Fused Metal Scrap
        45041=Jagged Twisted Watchwork Scrap

        43555=Aetherized Metal Scrap
        41736=Fused Metal Scrap
        45042=Twisted Watchwork Scrap

        43556=Salvageable Aetherized Metal Scrap
        41737=Salvageable Fused Metal Scrap

    Other
        82488=Salvageable Intact Forged Scrap


Direct salvage output material:
    Metal Material
        19697=Copper Ore
        19703=Silver Ore
        19699=Iron Ore
        19698=Gold Ore
        19702=Platinum Ore
        19700=Mithril Ore
        19701=Orichalcum Ore

    Leather Material
        19719=Rawhide Leather Section
        19728=Thin Leather Section
        19730=Coarse Leather Section
        19731=Rugged Leather Section
        19729=Thick Leather Section
        19732=Hardened Leather Section

    Cloth Material
        19718=Jute Scrap
        19739=Wool Scrap
        19741=Cotton Scrap
        19743=Linen Scrap
        19748=Silk Scrap
        19745=Gossamer Scrap

    Wood Material
        19723=Green Wood Log
        19726=Soft Wood Log
        19727=Seasoned Wood Log
        19724=Hard Wood Log
        19722=Elder Wood Log
        19725=Ancient Wood Log

    Rare Materials
        24301=Charged Sliver
        24302=Charged Fragment
        24303=Charged Shard
        24304=Charged Core
        24305=Charged Lodestone

        24311=Molten Sliver
        24312=Molten Fragment
        24313=Molten Shard
        24314=Molten Core
        24315=Molten Lodestone

        24316=Glacial Sliver
        24317=Glacial Fragment
        24318=Glacial Shard
        24319=Glacial Core
        24320=Glacial Lodestone

        24307=Onyx Fragment
        24308=Onyx Shard
        24309=Onyx Core

        44941=Watchwork Sprocket


Refinement materials:
    Metal Refinement
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

    Leather Refinement
        19738=Stretched Rawhide Leather Square
        19733=Cured Thin Leather Square
        19734=Cured Coarse Leather Square
        19736=Cured Rugged Leather Square
        19735=Cured Thick Leather Square
        19737=Cured Hardened Leather Square

    Cloth Refinement
        19720=Bolt of Jute
        19740=Bolt of Wool
        19742=Bolt of Cotton
        19744=Bolt of Linen
        19747=Bolt of Silk
        19746=Bolt of Gossamer

    Wood Refinement
        19710=Green Wood Plank
        19713=Soft Wood Plank
        19714=Seasoned Wood Plank
        19711=Hard Wood Plank
        19709=Elder Wood Plank
        19712=Ancient Wood Plank

Additional refinement materials:
    19704=Lump of Tin (Bronze Ingots)
    19750=Lump of Coal (Steel Ingot)
    19924=Lump of Primordium (Darksteel)

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
    1x Bolt of Jute = 2x Jute Scrap
    1x Bolt of Wool = 2x Wool Scrap
    1x Bolt of Cotton = 2x Cotton Scrap
    1x Bolt of Linen = 2x Linen Scrap
    1x Bolt of Silk = 3x Silk Scrap
    1x Bolt of Gossamer = 2x Gossamer Scrap

Wood
    1x Green Wood Plank = 3x Green Wood Log
    1x Soft Wood Plank = 2x Soft Wood Log
    1x Seasoned Wood Plank = 3x Seasoned Wood Plank
    1x Hard Wood Plank = 3x Hard Wood Log
    1x Elder Wood Plank = 3x Elder Wood Log
    1x Ancient Wood Plank = 3x Ancient Wood Log

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
        Shredded Garment = (1-3) Jute Scrap
        Half-Eaten Mass = (1-3) Jute Scrap
        Shredded Rag = (1-3) Jute Scrap
        Worn Garment = (1-3) Jute Scrap + (1-3) Wool Scrap
        Decaying Mass = (1-3) Jute Scrap + (1-3) Wool Scrap
        Worn Rag = (1-3) Jute Scrap + (1-3) Wool Scrap
        Ragged Garment = (1-3) Wool Scrap + (1-3) Cotton Scrap
        Fetid Mass = (1-3) Wool Scrap + (1-3) Cotton Scrap
        Soiled Rag = (1-3) Wool Scrap + (1-3) Cotton Scrap
        Frayed Garment = (1-3) Cotton Scrap + (1-3) Linen Scrap
        Malodorous Mass = (1-3) Cotton Scrap + (1-3) Linen Scrap
        Frayed Rag = (1-3) Cotton Scrap + (1-3) Linen Scrap
        Torn Garment = (1-3) Linen Scrap + (1-3) Silk Scrap
        Half-Digested Mass = (1-3) Linen Scrap + (1-3) Silk Scrap
        Torn Rag = (1-3) Linen Scrap + (1-3) Silk Scrap
        Discarded Garment = (1-3) Silk Scrap + Gossamer Scrap
        Regurgitated Mass = (1-3) Silk Scrap + Gossamer Scrap
        Rag = (1-3) Silk Scrap + Gossamer Scrap
        Unstable Rag = Jute, Woll, Cotton, Linen, Silk, Gossamer

    Wood
        Reglaimed Wood Chunk = Green, Soft, Seasoned, Hard, Elder, Ancient

    Rare Metal Salvage
        Bit or Aetherized Metal = Copper, Silver, Iron, Gold, Mithril, Charged Sliver
        Bit of Fused Metal Scrap = Copper, Silver, Iron, Mithril, Molten Sliver, Glacial Sliver
        Bit of Twisted Watchwork Scrap = Copper, Silver, Iron, Charged Sliver, Watchwork Sprocket
        Pile of Aetherized Metal Scrap = Silver, Iron, Gold, Charged Fragment
        Pile of Fused Metal Scrap = Silver, Iron, Gold, Molten Fragment, Glacial Fragment
        Pile of Twisted Watchwork Scrap = Silver, Iron, Gold, Onyx Fragment, Watchwork Sprocket
        Jagged Aetherized Metal Scrap = Iron, Gold, Platinum, Charged Shard
        Jagged Fused Metal Scrap = Iron, Gold, Platinum, Molten Shard, Glaciak Shard
        Jagged Twisted Watchwork Scrap = Iron, Gold, Platinum, Charged Shard, Onyx Shard, Watchwork Sprocket
        Aetherized Metal Scrap = Silver, Iron, Gold, Platinum, Mithril, Orichalcum, Charged Sliver, Charged Fragment, Charged Core
        Fused Metal Scrap = Copper, Iron, Platinum, Mithril, Orichalcum, Molten Sliver, Molten Core, Glacial Core
        Twisted Watchwork Scrap = Gold, Platinum, Mithril, Charged Core, Onyx Core, Watchwork Sprocket
        Salvageable Aetherized Metal Scrap = Mithril, Orichalcum, Charged Core, Charge Lodestone
        Salvageable Fused Metal Scrap = Mithril, Orichalcum, Molten Core, Molten Lodestone, Glacial Core, Glacial Lodestone
        Salvageable Twisted Watchwork Scrap = Mithril, Orichalcum, Watchwork Sprocket, Charged Core, Charged Lodestone, Onyx Core, Onyx Lodestone

    Other
        Salvageable Intact Forged Scrap = (3-9) Mithril xor (3) Orichalcum xor (1,5) Forgemetal + (1-3) 10 luck xor (1-3) 50 luck xor 100 luck xor 200 luck
        Don't care about Ambrite
        Ectoplasm use cases deserve their own script since the drop rate is so well understood already
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
    #api call for all leather TP prices
    #separate into base and refined
    #return format is a dict
    return


def getCloth():
    #api call for all cloth TP prices
    #separate into base and refined
    #return format is a dict
    return


def getWood():
    #api call for all wood TP prices
    #separate into base and refined
    #return format is a dict
    return


def compareMetal():
    #compare prices of raw vs refined metal
    #return dict with key metal and TP price values
    #return another dict with key metal and something indicating processing
    #metal-value will be used to calculate profits
    #metal-processing is the all important instructions for me
    return


def compareLeather():
    #compare prices of raw vs refined leather
    #return dict with key leather and TP price values
    #return another dict with key leather and something indicating processing
    #leather-value will be used to calculate profits
    #leather-processing is the all important instructions for me
    return


def compareCloth():
    #compare prices of raw vs refined cloth
    #return dict with key cloth and TP price values
    #return another dict with key cloth and something indicating processing
    #cloth-value will be used to calculate profits
    #cloth-processing is the all important instructions for me
    return


def compareWood():
    #compare prices of raw vs refined wood
    #return dict with key wood and TP price values
    #return another dict with key wood and something indicating processing
    #wood-value will be used to calculate profits
    #wood-processing is the all important instructions for me
    return


def calculateSalvage():
    #calculate the average value of the salvage item - buy and sell
    return


def printReport():
##not sure if lumping all the material values at once is better or repeat per item

    #CLEARLY state if item is profitable to cost
    #state profit or lack thereof
    #state cost of salvage item and average value of salvage output
    #state material values
    #state if refined is more profitable, and by how much
    return
