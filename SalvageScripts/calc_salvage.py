#This is a basic starter script for figuring out salvaging calculations in GW2
"""Basic salvage cost calculating in GW2

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


Steps are currently:
    Get and sort values from GW2 API
    Generate optimal values of material price + decision for selling
    Print chart of values and decision for selling with profit
    Calculate value of salvage item with the 3 types of salvage methods
    Print result

Ideal steps:
    Get and sort values from GW2 API
    Generate optimal values of material price + decision for selling
    Calculate all salvage values and sums for selling with profit
    Print everything in a chart per material type
    Have a summary at the end about what is profitable to salvage and by how much

Additional work:
    Instead of salvaging to sell, calculate the cost savings of buying and salvaging vs buying
    Computing the 4 combinations of buy-sell profits
    Computing how many items I'd need to salvage to get x amount of material

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

#Organize API entries
def sort_allAPI(allAPI):
    salvageLeather = {}
    unrefined_prices = {}
    refined_prices = {}

    for entryAPI in allAPI:
        if(entryAPI['id']==79213):
            salvageLeather['Unstable Hide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==80681):
            salvageLeather['Bloodstone-Warped Hide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==21689):
            salvageLeather['Hard Leather Strap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
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

    return unrefined_prices, refined_prices, salvageLeather

#General compute and print report
def salvagePrint(itemName_str,itemCost_dct,multiplier_dct,droprate_dict,salvageCost_dct,buysell):
    print("\n{salvageName} buy order: {salvagePrice}".format(salvageName=itemName_str, salvagePrice=itemCost_dct[itemName_str][buysell]))
    for rarity,droprate_x in droprate_dict.items():
        itemValues_dct,itemSum_dct = compute_result(droprate_x,multiplier_dct,True)
        print("{salvageName} {salvageMethod:<11} : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageName=itemName_str,salvageMethod=rarity,salvageValue=itemSum_dct,profit=itemSum_dct - salvageCost_dct[rarity]-itemCost_dct[itemName_str][buysell]))


"""
Main Program
"""

"""New case needs the following information:
    droprate dictionary
    material IDs added to allAPI list
    material IDs added to sort_allAPI function
    variable to allAPI output if needed
    salvagePrint function call
"""



#Import new common helper file
#from calc_helpers import *
#Python GW2 API wrapper library
from calc_helpers import *
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
droprate_UnstableHide = {}
#My data
droprate_UnstableHide['Copper'] = {'Rawhide Leather Section':0.1621,'Thin Leather Section':0.5152,'Coarse Leather Section':0.4758,'Rugged Leather Section':0.4798,'Thick Leather Section':0.1516,'Hardened Leather Section':0.2813}
droprate_UnstableHide['Runecrafter'] = {'Rawhide Leather Section':0.1730,'Thin Leather Section':0.4786,'Coarse Leather Section':0.4877,'Rugged Leather Section':0.4779,'Thick Leather Section':0.1680,'Hardened Leather Section':0.3152}
#pure peu
droprate_UnstableHide['Rare'] = {'Rawhide Leather Section':0.196,'Thin Leather Section':0.424,'Coarse Leather Section':0.412,'Rugged Leather Section':0.444,'Thick Leather Section':0.236,'Hardened Leather Section':0.372}

##Bloodstone-Warped Hide
droprate_BloodstoneWarpedHide={}
#my data only
droprate_BloodstoneWarpedHide['Copper'] = {'Rawhide Leather Section':0.0462,'Thin Leather Section':0.0533,'Coarse Leather Section':0.0445,'Rugged Leather Section':0.0467,'Thick Leather Section':0.4533,'Hardened Leather Section':0.4714}
droprate_BloodstoneWarpedHide['Runecrafter'] = {'Rawhide Leather Section':0.0451,'Thin Leather Section':0.0459,'Coarse Leather Section':0.0471,'Rugged Leather Section':0.0445,'Thick Leather Section':0.5016,'Hardened Leather Section':0.5249}
#wiki
droprate_BloodstoneWarpedHide['Rare'] = {'Rawhide Leather Section':0.0557,'Thin Leather Section':.0581,'Coarse Leather Section':0.0521,'Rugged Leather Section':0.0508,'Thick Leather Section':0.4758,'Hardened Leather Section':0.5541}

#Hard Leather Strap
droprate_HardLeatherStrap={}
#Mine
droprate_HardLeatherStrap['Copper'] = {'Thick Leather Section':1.2865,'Hardened Leather Section':0.0770}
droprate_HardLeatherStrap['Runecrafter'] = {'Thick Leather Section':1.352,'Hardened Leather Section':0.092}
droprate_HardLeatherStrap['Rare'] = {'Thick Leather Section':1.232,'Hardened Leather Section':0.112}


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
#salvageOptions 'Mystic':10.5, 'Copper':5 , 'Runecrafter':30, 'Silver':60
salvageCost = {'Copper':5 , 'Runecrafter':30, 'Rare':10.5}
#Containers
#defaulting to main ingots for refined to avoid problems. generate_multiplier will change as needed
unrefined_to_refined = {'Hardened Leather Section':'Cured Hardened Leather Square','Thick Leather Section':'Cured Thick Leather Square','Rugged Leather Section':'Cured Rugged Leather Square','Coarse Leather Section':'Cured Coarse Leather Square','Thin Leather Section':'Cured Thin Leather Square','Rawhide Leather Section':'Stretched Rawhide Leather Square',
                        'Copper Ore':'Copper Ingot','Silver Ore':'Silver Ingot','Iron Ore':'Iron Ingot','Gold Ore':'Gold Ingot','Platinum Ore':'Platinum Ingot','Mithril Ore':'Mithril Ingot','Orichalcum Ore':'Orichalcum Ingot',
                        'Jute Scrap':'Bolt of Jute','Wool Scrap':'Bolt of Wool','Cotton Scrap':'Bolt of Cotton','Linen Scrap':'Bolt of Linen','Silk Scrap':'Bolt of Silk','Gossamer Scrap':'Bolt of Gossamer',
                        'Green Wood Log':'Green Wood Plank','Soft Wood Log':'Soft Wood Plank','Seasoned Wood Log':'Seasoned Wood Plank','Hard Wood Log':'Hard Wood Plank','Elder Wood Log':'Elder Wood Plank','Ancient Wood Log':'Ancient Wood Plank'}

refined_scalar = {'Stretched Rawhide Leather Square':2,'Cured Thin Leather Square':2,'Cured Coarse Leather Square':2,'Cured Rugged Leather Square':2,'Cured Thick Leather Square':4,'Cured Hardened Leather Square':3,
                'Copper Ingot':2,'Bronze Ingot':2,'Silver Ingot':2,'Iron Ingot':3,'Steel Ingot':3,'Gold Ingot':2,'Platinum Ingot':2,'Darksteel Ingot':2,'Mithril Ingot':2,'Orichalcum Ingot':2,
                'Bolt of Jute':2,'Bolt of Wool':2,'Bolt of Cotton':2,'Bolt of Linen':2,'Bolt of Silk':3,'Bolt of Gossamer':2,
                'Green Wood Plank':3,'Soft Wood Plank':2,'Seasoned Wood Plank':3,'Hard Wood Plank':3,'Elder Wood Plank':3,'Ancient Wood Plank':3,
                'Pile of Lucent Crystal':10}

#Raw to refined lookup

#All relevant IDs
#Once salvage item at a time
allIDs =    [79213,80681,21689,#Leather salvage
            19719,19728,19730,19731,19729,19732,#raw leather
            19738,19733,19734,19736,19735,19737]#refined leather

allAPI=gw2_client.commerceprices.get(ids=allIDs)

unrefined_prices, refined_prices, salvageLeather = sort_allAPI(allAPI)

#Multiplier creation
#Multiplier and decision are based off of sell prices
multiplier_prices,decision = generate_multiplier(unrefined_prices,refined_prices,refined_scalar,unrefined_to_refined,1)

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
salvagePrint('Unstable Hide',salvageLeather,multiplier_prices,droprate_UnstableHide,salvageCost,0)
salvagePrint('Bloodstone-Warped Hide',salvageLeather,multiplier_prices,droprate_BloodstoneWarpedHide,salvageCost,0)
salvagePrint('Hard Leather Strap',salvageLeather,multiplier_prices,droprate_HardLeatherStrap,salvageCost,0)
