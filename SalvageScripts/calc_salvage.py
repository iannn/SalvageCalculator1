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

"""
THIS IS EVERYTHING I WOULD LIKE TO DO BUT IS TOO MUCH FOR PASS ONE UPON FINISHING Unidentified GEAR SCRIPT

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

END VERY NICE TO HAVE SECTION"""

#Organize API entries
def sort_allAPI(allAPI):
    salvageLeather = {}
    unrefined_prices = {}
    refined_prices = {}

    for entryAPI in allAPI:
        if(entryAPI['id']==79213):
            salvageLeather['Unstable Hide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==80681):
            salvageLeather['BloodstoneWarpedHide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==21689):
            salvageLeather['HardLeatherStrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19719):
            unrefined_prices['Rawhide Leather Section'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19728):
            unrefined_prices['Thin Leather Section'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19730):
            unrefined_prices['Coarse Leather Section'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19731):
            unrefined_prices['Rugged Leather Section'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19729):
            unrefined_prices['Thick Leather Section'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19732):
            unrefined_prices['Hardened Leather Section'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19738):
            refined_prices['Stretched Rawhide Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19733):
            refined_prices['Cured Thin Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19734):
            refined_prices['Cured Coarse Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19736):
            refined_prices['Cured Rugged Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19735):
            refined_prices['Cured Thick Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19737):
            refined_prices['Cured Hardened Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        else:
            print("Unexpected API return")
            print(entryAPI)

    return salvageLeather, unrefined_prices, refined_prices

"""
Main Program
"""

#Import new common helper file
#from calc_helpers import *
#Python GW2 API wrapper library
from gw2api import GuildWars2Client
gw2_client = GuildWars2Client()

"""Drop rates"""

"""
Drop rates: Metals
"""


"""
Drop rates: Leathers
"""
##Unstable Hide
#My data
droprateCopper_UnstableHide = {'Rawhide Leather Section':0.162189054726368,'Thin Leather Section':0.507462686567164,'Coarse Leather Section':0.464676616915423,'Rugged Leather Section':0.511442786069652,'Thick Leather Section':0.154228855721393,'Hardened Leather Section':0.276616915422886}
droprateRunecrafter_UnstableHide = {'Rawhide Leather Section':0.188764829030007,'Thin Leather Section':0.464061409630147,'Coarse Leather Section':0.469295184926727,'Rugged Leather Section':0.469644103279833,'Thick Leather Section':0.186322400558269,'Hardened Leather Section':0.321702721563154}
#pure peu
droprateRare_UnstableHide = {'Rawhide Leather Section':0.196,'Thin Leather Section':0.424,'Coarse Leather Section':0.412,'Rugged Leather Section':0.444,'Thick Leather Section':0.236,'Hardened Leather Section':0.372}

##Bloodstone-Warped Hide
#wiki
droprateCopper_BloodstoneWarpedHide = {'Rawhide Leather Section':0.0443,'Thin Leather Section':0.0471,'Coarse Leather Section':0.0393,'Rugged Leather Section':0.0385,'Thick Leather Section':0.4453,'Hardened Leather Section':0.5020}
#my data only
droprateRunecrafter_BloodstoneWarpedHide = {'Rawhide Leather Section':0.0444758206847864,'Thin Leather Section':0.0476526650194141,'Coarse Leather Section':0.0501235439463466,'Rugged Leather Section':0.0458877515001765,'Thick Leather Section':0.502294387575009,'Hardened Leather Section':0.521708436286622}
#wiki
droprateRare_BloodstoneWarpedHide = {'Rawhide Leather Section':0.0557,'Thin Leather Section':.0581,'Coarse Leather Section':0.0521,'Rugged Leather Section':0.0508,'Thick Leather Section':0.4758,'Hardened Leather Section':0.5541}

#Hard Leather Strap
droprateCopper_HardLeatherStrap = {'Thick Leather Section':1.32,'Hardened Leather Section':0.073}
droprateRunecrafter_HardLeatherStrap = {'Thick Leather Section':1.352,'Hardened Leather Section':0.092}
droprateRare_HardLeatherStrap = {'Thick Leather Section':1.232,'Hardened Leather Section':0.112}


"""
Drop rates: Cloth
"""


"""
Drop rates: Wood
"""
#Yes, there's only 1

"""
Helper stuff
"""
#Salvage options
salvageCost = {'Mystic':10.5, 'Copper':5 , 'Runecrafter':30, 'Silver':60}

#Containers
#defaulting to main ingots for refined to avoid problems. generate_multiplier will change as needed
unrefined_to_refined = {'Hardened Leather Section':'Cured Hardened Leather Square','Thick Leather Section':'Cured Thick Leather Square','Rugged Leather Section':'Cured Rugged Leather Square','Coarse Leather Section':'Cured Coarse Leather Square','Thin Leather Section':'Cured Thin Leather Square','Rawhide Leather Section':'Stretched Rawhide Leather Square',
                        'Copper Ore':'Copper Ingot','Silver Ore':'Silver Ingot','Iron Ore':'Iron Ingot','Gold Ore':'Gold Ingot','Platinum Ore':'Platinum Ingot','Mithril Ore':'Mithril Ingot','Orichalcum Ore':'Orichalcum Ingot',
                        'Jute Scrap':'Bolt of Jute','Wool Scrap':'Bolt of Wool','Cotton Scrap':'Bolt of Cotton','Linen Scrap':'Bolt of Linen','Silk Scrap':'Bolt of Silk','Gossamer Scrap':'Bolt of Gossamer',
                        'Green Wood Log':'Green Wood Plank','Soft Wood Log':'Soft Wood Plank','Seasoned Wood Log':'Seasoned Wood Plank','Hard Wood Log':'Hard Wood Plank','Elder Wood Log':'Elder Wood Plank','Ancient Wood Log':'Ancient Wood Plank'}

refined_scalar = {'Cured Thick Leather Square':4,'Cured Hardened Leather Square':3,
                'Mithril Ingot':2,'Orichalcum Ingot':2,
                'Elder Wood Plank':3,'Ancient Wood Plank':3,
                'Bolt of Silk':3,'Bolt of Gossamer':2,
                'Pile of Lucent Crystal':10}


multiplier_prices ={}
decision = {}

#Salvage Value containers
valueCopper_UnstableHide = {}
sumCopper_UnstableHide = 0
valueRunecrafter_UnstableHide = {}
sumRunecrafter_UnstableHide = 0
valueRare_UnstableHide = {}
sumRare_UnstableHide = 0

valueCopper_BloodstoneWarpedHide = {}
sumCopper_BloodstoneWarpedHide = 0
valueRunecrafter_BloodstoneWarpedHide = {}
sumRunecrafter_BloodstoneWarpedHide = 0
valueRare_BloodstoneWarpedHide = {}
sumRare_BloodstoneWarpedHide = 0

valueCopper_HardLeatherStrap = {}
sumCopper_HardLeatherStrap = 0
valueRunecrafter_HardLeatherStrap = {}
sumRunecrafter_HardLeatherStrap = 0
valueRare_HardLeatherStrap = {}
sumRare_HardLeatherStrap = 0

#Raw to refined lookup

#All relevant IDs
#Once salvage item at a time
allIDs =    [79213,80681,21689,#Leather salvage
            19719,19728,19730,19731,19729,19732,#raw leather
            19738,19733,19734,19736,19735,19737]#refined leather

allAPI=gw2_client.commerceprices.get(ids=allIDs)

salvageLeather, unrefined_prices, refined_prices = sort_allAPI(allAPI)

#Multiplier creation

#multiplier_prices,decision = generate_multiplier(unrefined_prices,refined_prices,refined_scalar,refined_lookup,buysell)


#Yes, big if-else
#replace this with generate multiplier
#Leather
if(unrefined_prices['Hardened Leather Section'][1] > refined_prices['Cured Hardened Leather Square'][1]/3):
    decision['Hardened Leather Section'] = 'raw'
    multiplier_prices['Hardened Leather Section']=round(unrefined_prices['Hardened Leather Section'][1],4)
else:
    decision['Hardened Leather Section'] = 'refined'
    multiplier_prices['Hardened Leather Section']=round(refined_prices['Cured Hardened Leather Square'][1]/3,4)
if(unrefined_prices['Thick Leather Section'][1] > refined_prices['Cured Thick Leather Square'][1]/4):
    decision['Thick Leather Section'] = 'raw'
    multiplier_prices['Thick Leather Section']=round(unrefined_prices['Thick Leather Section'][1],4)
else:
    decision['Thick Leather Section'] = 'refined'
    multiplier_prices['Thick Leather Section']=round(refined_prices['Cured Thick Leather Square'][1]/4,4)
if(unrefined_prices['Rugged Leather Section'][1] > refined_prices['Cured Rugged Leather Square'][1]/2):
    decision['Rugged Leather Section'] = 'raw'
    multiplier_prices['Rugged Leather Section']=round(unrefined_prices['Rugged Leather Section'][1],4)
else:
    decision['Rugged Leather Section'] = 'refined'
    multiplier_prices['Rugged Leather Section']=round(refined_prices['Cured Rugged Leather Square'][1]/2,4)
if(unrefined_prices['Coarse Leather Section'][1] > refined_prices['Cured Coarse Leather Square'][1]/2):
    decision['Coarse Leather Section'] = 'raw'
    multiplier_prices['Coarse Leather Section']=round(unrefined_prices['Coarse Leather Section'][1],4)
else:
    decision['Coarse Leather Section'] = 'refined'
    multiplier_prices['Coarse Leather Section']=round(refined_prices['Cured Coarse Leather Square'][1]/2,4)
if(unrefined_prices['Thin Leather Section'][1] > refined_prices['Cured Thin Leather Square'][1]/2):
    decision['Thin Leather Section'] = 'raw'
    multiplier_prices['Thin Leather Section']=round(unrefined_prices['Thin Leather Section'][1],4)
else:
    decision['Thin Leather Section'] = 'refined'
    multiplier_prices['Thin Leather Section']=round(refined_prices['Cured Thin Leather Square'][1]/2,4)
if(unrefined_prices['Rawhide Leather Section'][1] > refined_prices['Stretched Rawhide Leather Square'][1]/2):
    decision['Rawhide Leather Section'] = 'raw'
    multiplier_prices['Rawhide Leather Section']=round(unrefined_prices['Rawhide Leather Section'][1],4)
else:
    decision['Rawhide Leather Section'] = 'refined'
    multiplier_prices['Rawhide Leather Section']=round(refined_prices['Stretched Rawhide Leather Square'][1]/2,4)
#End multiplier and decision


#Price Chart
#The if is from the unid chart because there is no refinement on charm/symbol
print('{:<24} : {:>10}   {:<10}   {:<10}   {:<10}'.format('Material','Sell Price','State','Raw','Refined'))
print('-'*74)
for key, value in multiplier_prices.items():
    if key in decision:
        print('{:<24} : {:>10}   {:<10}   {:<10}   {:<10}'.format(key,value, decision[key],unrefined_prices[key][1],refined_prices[unrefined_to_refined[key]][1]))
    else:
        print('{:<24} : {:>10}'.format(key,value))

#Calculate salvaged values
#Different salvage rates with different kits. Each thing needs 3x reports then
for key in droprateCopper_UnstableHide:
    valueCopper_UnstableHide[key] = round(0.85*droprateCopper_UnstableHide[key]*multiplier_prices[key],4)
    sumCopper_UnstableHide = sumCopper_UnstableHide + valueCopper_UnstableHide[key]

for key in droprateRunecrafter_UnstableHide:
    valueRunecrafter_UnstableHide[key] = round(0.85*droprateRunecrafter_UnstableHide[key]*multiplier_prices[key],4)
    sumRunecrafter_UnstableHide = sumRunecrafter_UnstableHide + valueRunecrafter_UnstableHide[key]

for key in droprateRare_UnstableHide:
    valueRare_UnstableHide[key] = round(0.85*droprateRare_UnstableHide[key]*multiplier_prices[key],4)
    sumRare_UnstableHide = sumRare_UnstableHide + valueRare_UnstableHide[key]

print("unstable hide buy order: ",salvageLeather['Unstable Hide'][0])
print("unstable hide Copper      : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumCopper_UnstableHide,profit=sumCopper_UnstableHide - salvageCost['Copper']-salvageLeather['Unstable Hide'][0]))
print("unstable hide Runecrafter : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumRunecrafter_UnstableHide,profit=sumRunecrafter_UnstableHide - salvageCost['Runecrafter']-salvageLeather['Unstable Hide'][0]))
print("unstable hide Rare        : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumRare_UnstableHide,profit=sumRare_UnstableHide - salvageCost['Silver']-salvageLeather['Unstable Hide'][0]))


for key in droprateCopper_BloodstoneWarpedHide:
    valueCopper_BloodstoneWarpedHide[key] = round(0.85*droprateCopper_BloodstoneWarpedHide[key]*multiplier_prices[key],4)
    sumCopper_BloodstoneWarpedHide = sumCopper_BloodstoneWarpedHide + valueCopper_BloodstoneWarpedHide[key]

for key in droprateRunecrafter_BloodstoneWarpedHide:
    valueRunecrafter_BloodstoneWarpedHide[key] = round(0.85*droprateRunecrafter_BloodstoneWarpedHide[key]*multiplier_prices[key],4)
    sumRunecrafter_BloodstoneWarpedHide = sumRunecrafter_BloodstoneWarpedHide + valueRunecrafter_BloodstoneWarpedHide[key]

for key in droprateRare_BloodstoneWarpedHide:
    valueRare_BloodstoneWarpedHide[key] = round(0.85*droprateRare_BloodstoneWarpedHide[key]*multiplier_prices[key],4)
    sumRare_BloodstoneWarpedHide = sumRare_BloodstoneWarpedHide + valueRare_BloodstoneWarpedHide[key]

print("Bloodstone-Warped Hide buy order: ",salvageLeather['BloodstoneWarpedHide'][0])
print("BloodstoneWarpedHide Copper      : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumCopper_BloodstoneWarpedHide,profit=sumCopper_BloodstoneWarpedHide - salvageCost['Copper']-salvageLeather['BloodstoneWarpedHide'][0]))
print("BloodstoneWarpedHide Runecrafter : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumRunecrafter_BloodstoneWarpedHide,profit=sumRunecrafter_BloodstoneWarpedHide - salvageCost['Runecrafter']-salvageLeather['BloodstoneWarpedHide'][0]))
print("BloodstoneWarpedHide Rare        : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumRare_BloodstoneWarpedHide,profit=sumRare_BloodstoneWarpedHide - salvageCost['Silver']-salvageLeather['BloodstoneWarpedHide'][0]))

for key in droprateCopper_HardLeatherStrap:
    valueCopper_HardLeatherStrap[key] = round(0.85*droprateCopper_HardLeatherStrap[key]*multiplier_prices[key],4)
    sumCopper_HardLeatherStrap = sumCopper_HardLeatherStrap + valueCopper_HardLeatherStrap[key]

for key in droprateRunecrafter_HardLeatherStrap:
    valueRunecrafter_HardLeatherStrap[key] = round(0.85*droprateRunecrafter_HardLeatherStrap[key]*multiplier_prices[key],4)
    sumRunecrafter_HardLeatherStrap = sumRunecrafter_HardLeatherStrap + valueRunecrafter_HardLeatherStrap[key]

for key in droprateRare_HardLeatherStrap:
    valueRare_HardLeatherStrap[key] = round(0.85*droprateRare_HardLeatherStrap[key]*multiplier_prices[key],4)
    sumRare_HardLeatherStrap = sumRare_HardLeatherStrap + valueRare_HardLeatherStrap[key]

print("HardLeatherStrap buy order: ",salvageLeather['HardLeatherStrap'][0])
print("HardLeatherStrap Copper      : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumCopper_HardLeatherStrap,profit=sumCopper_HardLeatherStrap - salvageCost['Copper']-salvageLeather['HardLeatherStrap'][0]))
print("HardLeatherStrap Runecrafter : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumRunecrafter_HardLeatherStrap,profit=sumRunecrafter_HardLeatherStrap - salvageCost['Runecrafter']-salvageLeather['HardLeatherStrap'][0]))
print("HardLeatherStrap Rare        : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageValue=sumRare_HardLeatherStrap,profit=sumRare_HardLeatherStrap - salvageCost['Silver']-salvageLeather['HardLeatherStrap'][0]))
