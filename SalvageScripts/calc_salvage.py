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
        21681=Metal Scrap

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

        21675=Discarded Garment
        22330=Regurgitated Mass
        21666=Rag

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
Function Declarations
"""
#Organize API entries
def sort_allAPI(allAPI):
    """The purpose of this function is to sort the raw GW2 API wrapper return dictionaries (originally JSON objects) into the necessary dictionaries for use in this "calc_salvage" script"""

    """Input:
        bit list of commerceprices API objects. List, not dict
    """

    """Output:
        unrefined_prices = dictionary of all unrefined material prices. "Raw" and "unrefined" are used interchangeable when they probably shouldn't be
        refined_prices = dictionary of all refined material prices
        salvageLeather = dictionary of corresponding salvage item names and prices
        salvageWood = dictionary of corresponding salvage item names and prices
        salvageMetal = dictionary of corresponding salvage item names and prices
        salvageCloth = dictionary of corresponding salvage item names and prices

        All use the format of:
            "salvage item name" :[buy order price, sell listing price]
    """

    """Design Note:
    A dictionary with the key:value pair id:name  is needed for this to work because these are sorting commerceprices data from the API, and only returns the following:
    {'id': 79423, 'whitelisted': False, 'buys': {'quantity': 13684, 'unit_price': 114}, 'sells': {'quantity': 22649, 'unit_price': 119}}
    """

    #there is only 1 wood salvage item so it just needs a single case in the sorting loop

    api_salvageMetal = {21690:'Brittle Clump of Ore',21678:'Bit of Metal Scrap',#T1
                        21691:'Weak Clump of Ore',21679:'Pile of Metal Scrap',#T2
                        21692:'Clump of Ore',21680:'Jagged Metal Scrap',
                        21693:'Laden Clump of Ore',21681:'Metal Scrap',
                        21694:'Loaded Clump of Ore',21682:'Salvageable Metal Scrap',
                        21695:'Rich Clump of Ore',21683:'Valuable Metal Scrap',
                        79079:'Unstable Metal Chunk'}
    api_salvageLeather = {21661:'Tattered Hide',21684:'Rawhide Leather Strap',21653:'Tattered Pelt',
                        21664:'Ripped Hide',21685:'Thin Leather Strap',21654:'Ripped Pelt',
                        21667:'Torn Hide',21686:'Coarse Leather Strap',21655:'Torn Pelt',
                        21668:'Frayed Hide',21687:'Thick Leather Strap',21656:'Frayed Pelt',
                        21670:'Filthy Hide',21688:'Rugged Leather Strap',21657:'Filthy Pelt',
                        22331:'Salvageable Hide',21689:'Hard Leather Strap',21658:'Salvageable Pelt',
                        79213:'Unstable Hide',80681:'Bloodstone-Warped Hide'}
    api_salvageCloth = {21669:'Shredded Garment',22325:'Half-Eaten Mass',21659:'Shredded Rag',
                        21671:'Worn Garment',22326:'Decaying Mass',21660:'Worn Rag',
                        21672:'Ragged Garment',22327:'Fetid Mass',21662:'Soiled Rag',
                        21673:'Frayed Garment',22328:'Malodorous Mass',21663:'Frayed Rag',
                        21674:'Torn Garment',22329:'Half-Digested Mass',21665:'Torn Rag',
                        21675:'Discarded Garment',22330:'Regurgitated Mass',21666:'Rag',
                        21676:'Garment_28',21677:'Garment_32',
                        79138:'Unstable Rag'}
    api_unrefined_prices = {19697:'Copper Ore',19703:'Silver Ore',19699:'Iron Ore',19698:'Gold Ore',19702:'Platinum Ore',19700:'Mithril Ore',19701:'Orichalcum Ore',
                            19719:'Rawhide Leather Section',19728:'Thin Leather Section',19730:'Coarse Leather Section',19731:'Rugged Leather Section',19729:'Thick Leather Section',19732:'Hardened Leather Section',
                            19718:'Jute Scrap',19739:'Wool Scrap',19741:'Cotton Scrap',19743:'Linen Scrap',19748:'Silk Scrap',19745:'Gossamer Scrap',
                            19723:'Green Wood Log',19726:'Soft Wood Log',19727:'Seasoned Wood Log',19724:'Hard Wood Log',19722:'Elder Wood Log',19725:'Ancient Wood Log'}
    api_refined_prices = {19680:'Copper Ingot',19679:'Bronze Ingot',19687:'Silver Ingot',19683:'Iron Ingot',19688:'Steel Ingot',19682:'Gold Ingot',19686:'Platinum Ingot',19681:'Darksteel Ingot',19684:'Mithril Ingot',19685:'Orichalcum Ingot',
                        19738:'Stretched Rawhide Leather Square',19733:'Cured Thin Leather Square',19734:'Cured Coarse Leather Square',19736:'Cured Rugged Leather Square',19735:'Cured Thick Leather Square',19737:'Cured Hardened Leather Square',
                        19720:'Bolt of Jute',19740:'Bolt of Wool',19742:'Bolt of Cotton',19744:'Bolt of Linen',19747:'Bolt of Silk',19746:'Bolt of Gossamer',
                        19710:'Green Wood Plank',19713:'Soft Wood Plank',19714:'Seasoned Wood Plank',19711:'Hard Wood Plank',19709:'Elder Wood Plank',19712:'Ancient Wood Plank'}

    #Return dictionaries with 'item':[buy sell] key:value pairs
    salvageWood = {}#Yes it has one entry but dict is the required data type
    salvageMetal = {}
    salvageLeather = {}
    salvageCloth = {}
    unrefined_prices = {}
    refined_prices = {}

    #If the id exists in a specific api_{dict} then it is added into it's corresponding return dict. This replaces repetitive elif statements
    for entryAPI in allAPI:
        if(entryAPI['id']==79423):#special case because there's only 1
            salvageWood['Reclaimed Wood Chunk'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif entryAPI['id'] in api_salvageMetal:
            salvageMetal[api_salvageMetal[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif entryAPI['id'] in api_salvageLeather:
            salvageLeather[api_salvageLeather[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif entryAPI['id'] in api_salvageCloth:
            salvageCloth[api_salvageCloth[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif entryAPI['id'] in api_unrefined_prices:
            unrefined_prices[api_unrefined_prices[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif entryAPI['id'] in api_refined_prices:
            refined_prices[api_refined_prices[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        else:
            print("Unexpected API return")
            print(entryAPI)

    return unrefined_prices, refined_prices, salvageLeather, salvageWood, salvageMetal, salvageCloth

#General compute and print report
def salvagePrint(itemName_str,itemCost_dct,multiplier_dct,droprate_dict,salvageCost_dct,buysell):
    """ Input:
        itemName_str = string name of salvage item
        itemCost_dct = dictionary with salvage item costs. salvage item name : [buy order price, sell listing price]
        multiplier_dct = dictionary of all material values. raw material name : buy or sell value
        droprate_dict =
        salvageCost_dct
        buysell
    """



    """This is the goal

    Hard Leather Strap  : {cost}
    Salvage Kit             Profit  | Total Value   | item 1    item 2
    --------------------------------------------------------------------------------------
    Copper              : {profit}  | {sum right}   |
    Runecrafters        : {profit}  | {sum right}   |
    Rare                : {profit}  | {sum right}   |

    return value is some kind of profit metric [salvage item, salvage method, salvage profit %, profit]
        [7-20) "Consider" because profit is low and profit % may be terrible
        [20-50) "Good" enough profit per salvage and maybe decent profit %
        [50-100) "BUYBUYBUY" because this is a definitely good "can be bought, priced lower, and make good profit" with a probably good profit %
        [100:) "MEGA BUY" because the profit on this is close to the cost of some salvage items themselves

    """
    worthit_list = []


    orderedkeys = list(droprate_dict['Copper'].keys())
    #the "%" operator here is actually used as the indicator for "%d" to format strings, like with C
    formatline = "{:<14} : {:>10} | {:>12} | " + '  '.join(["{:>%d}" % len(l) for l in orderedkeys])
    print("\n{salvageName} : {salvagePrice}".format(salvageName=itemName_str, salvagePrice=itemCost_dct[itemName_str][buysell]))
    print("-"*(len(itemName_str)+8))
    print(formatline.format(*["Salvage Kit", "Profit","Total Value"]+orderedkeys))
    #print("-"*len(formatline)) maybe ad this in later. I don't really care to have the labels separated from the data

    #This is difficult to test separately without a lot of setup but was shown to be accurate
    #Checking for multiple items was the most difficult part to do properly but this expression is some kind of generator that will break as soon as a match is found "not any(x in ["MEGA BUY", "BUYBUYBUY", "Good"] for x in worthit_list)"
    for salvage_rarity,droprate_x in droprate_dict.items():
        itemValues_dct,itemSum_val = compute_result(droprate_x,multiplier_dct,True)
        methodprofit=round(itemSum_val - salvageCost_dct[salvage_rarity]-itemCost_dct[itemName_str][buysell],4)
        print(formatline.format(*[salvage_rarity,round(methodprofit,4),round(itemSum_val,4)]+[itemValues_dct[x] for x in orderedkeys]))
        "%d%%"%(100*(methodprofit/(salvageCost_dct[salvage_rarity]+itemCost_dct[itemName_str][buysell])))
        if (methodprofit >= 100):
            worthit_list = [itemName_str, "Check Kit", methodprofit, "%d%%"%(100*(methodprofit/(salvageCost_dct[salvage_rarity]+itemCost_dct[itemName_str][buysell]))), "MEGA BUY"]
        elif (methodprofit >=50) and ("MEGA BUY" not in worthit_list):
            worthit_list = [itemName_str, salvage_rarity, methodprofit, "%d%%"%(100*(methodprofit/(salvageCost_dct[salvage_rarity]+itemCost_dct[itemName_str][buysell]))), "BUYBUYBUY"]
        elif (methodprofit >=20) and not any(x in ["MEGA BUY", "BUYBUYBUY"] for x in worthit_list):
            worthit_list = [itemName_str, salvage_rarity, methodprofit, "%d%%"%(100*(methodprofit/(salvageCost_dct[salvage_rarity]+itemCost_dct[itemName_str][buysell]))), "Good"]
        elif (methodprofit >=7) and not any(x in ["MEGA BUY", "BUYBUYBUY", "Good"] for x in worthit_list):
            worthit_list = [itemName_str, salvage_rarity, methodprofit, "%d%%"%(100*(methodprofit/(salvageCost_dct[salvage_rarity]+itemCost_dct[itemName_str][buysell]))), "Consider"]

    return worthit_list
#End of salvagePrint function

"""************************************
  ************ DROP RATES ************
************************************"""

"""New case needs the following information:
    droprate dictionary
    material IDs added to allAPI list
    material IDs added to sort_allAPI function
    variable to allAPI output if needed
    salvagePrint function call
"""

"""
Drop rates: Metals
"""

""" T1 """
#Brittle Clump of Ore
droprate_BrittleClumpofOre={}
#All Peureki
droprate_BrittleClumpofOre['Copper']={'Copper Ore':1.896}
droprate_BrittleClumpofOre['Runecrafter']={'Copper Ore':1.86}
droprate_BrittleClumpofOre['Rare']={'Copper Ore':1.888}

#Bit of Metal Scrap
droprate_BitofMetalScrap = {}
#All Peureki
droprate_BitofMetalScrap['Copper']={'Copper Ore':1.796}
droprate_BitofMetalScrap['Runecrafter']={'Copper Ore':1.884}
droprate_BitofMetalScrap['Rare']={'Copper Ore':1.856}

""" T2 """
#Weak Clump of Ore
droprate_WeakClumpofOre = {}
#Peu
droprate_WeakClumpofOre['Copper']={'Copper Ore':0.37,'Silver Ore':0.65,'Iron Ore':0.81}
droprate_WeakClumpofOre['Runecrafter']={'Copper Ore':0.25,'Silver Ore':0.78,'Iron Ore':0.75}
droprate_WeakClumpofOre['Rare']={'Copper Ore':0.43,'Silver Ore':0.81,'Iron Ore':0.77}

#Pile of Metal Scrap
droprate_PileofMetalScrap = {}
#Peu
droprate_PileofMetalScrap['Copper']={'Copper Ore':0.608,'Silver Ore':0.748,'Iron Ore':0.504}
droprate_PileofMetalScrap['Runecrafter']={'Copper Ore':0.484,'Silver Ore':0.712,'Iron Ore':0.66}
droprate_PileofMetalScrap['Rare']={'Copper Ore':0.408,'Silver Ore':0.632,'Iron Ore':0.812}

""" T3 """
#Pile of Clump of Ore
droprate_ClumpofOre = {}
#Peu
droprate_ClumpofOre['Copper']={'Silver Ore':0.24,'Iron Ore':0.916,'Gold Ore':0.604}
droprate_ClumpofOre['Runecrafter']={'Silver Ore':0.148,'Iron Ore':1.008,'Gold Ore':0.728}
droprate_ClumpofOre['Rare']={'Silver Ore':0.2,'Iron Ore':0.924,'Gold Ore':0.792}

#Jagged Metal Scrap
droprate_JaggedMetalScrap = {}
#Peu
droprate_JaggedMetalScrap['Copper']={'Silver Ore':0.228,'Iron Ore':0.836,'Gold Ore':0.752}
droprate_JaggedMetalScrap['Runecrafter']={'Silver Ore':0.176,'Iron Ore':0.924,'Gold Ore':0.752}
droprate_JaggedMetalScrap['Rare']={'Silver Ore':0.212,'Iron Ore':1.012,'Gold Ore':0.704}

""" T4 """
#Laden Clump of Ore
droprate_LadenClumpofOre = {}
#Peu
droprate_LadenClumpofOre['Copper']={'Iron Ore':0.224,'Gold Ore':0.176,'Platinum Ore':1.484}
droprate_LadenClumpofOre['Runecrafter']={'Iron Ore':0.204,'Gold Ore':0.212,'Platinum Ore':1.436}
droprate_LadenClumpofOre['Rare']={'Iron Ore':0.22,'Gold Ore':0.16,'Platinum Ore':1.424}

#Metal Scrap
droprate_MetalScrap = {}
#Peu
droprate_MetalScrap['Copper']={'Iron Ore':0.212,'Gold Ore':0.276,'Platinum Ore':1.3}
droprate_MetalScrap['Runecrafter']={'Iron Ore':0.176,'Gold Ore':0.164,'Platinum Ore':1.476}
droprate_MetalScrap['Rare']={'Iron Ore':0.184,'Gold Ore':0.136,'Platinum Ore':1.488}

""" T5 """
#Loaded Clump of Ore
droprate_LoadedClumpofOre = {}
#Peu
droprate_LoadedClumpofOre['Copper']={'Platinum Ore':0.524,'Mithril Ore':1.088}
droprate_LoadedClumpofOre['Runecrafter']={'Platinum Ore':0.456,'Mithril Ore':1.312}
droprate_LoadedClumpofOre['Rare']={'Platinum Ore':0.392,'Mithril Ore':1.32}

#Salvageable Metal Scrap
droprate_SalvageableMetalScrap = {}
#Peu
droprate_SalvageableMetalScrap['Copper']={'Platinum Ore':0.53,'Mithril Ore':1.07}
droprate_SalvageableMetalScrap['Runecrafter']={'Platinum Ore':0.51,'Mithril Ore':1.1}
droprate_SalvageableMetalScrap['Rare']={'Platinum Ore':0.39,'Mithril Ore':1.32}

""" T6 """
#Rich Clump of Ore
droprate_RichClumpofOre = {}
#Peu
droprate_RichClumpofOre['Copper']={'Mithril Ore':1.172,'Orichalcum Ore':0.244}
droprate_RichClumpofOre['Runecrafter']={'Mithril Ore':1.472,'Orichalcum Ore':0.192}
droprate_RichClumpofOre['Rare']={'Mithril Ore':1.24,'Orichalcum Ore':0.212}

#Valuable Metal Scrap
droprate_ValuableMetalScrap = {}
#Peu
droprate_ValuableMetalScrap['Copper']={'Mithril Ore':1.216,'Orichalcum Ore':0.196}
droprate_ValuableMetalScrap['Runecrafter']={'Mithril Ore':1.276,'Orichalcum Ore':0.2}
droprate_ValuableMetalScrap['Rare']={'Mithril Ore':1.468,'Orichalcum Ore':0.204}

""" All Tiers """
#Unstable Metal Chunk
droprate_UnstableMetalChunk = {}
#Me
droprate_UnstableMetalChunk['Copper']={'Copper Ore':0.2035,'Iron Ore':0.9506,'Platinum Ore':0.5039,'Mithril Ore':0.1453,'Orichalcum Ore':0.2946}
droprate_UnstableMetalChunk['Runecrafter']={'Copper Ore':0.1531,'Iron Ore':0.911,'Platinum Ore':0.9593,'Mithril Ore':0.1966,'Orichalcum Ore':0.3427}
#Peu
droprate_UnstableMetalChunk['Rare']={'Copper Ore':0.136,'Iron Ore':1.004,'Platinum Ore':0.523,'Mithril Ore':0.151,'Orichalcum Ore':0.31}

"""
Drop rates: Leathers
"""

""" T1 """
#Tattered Hide
droprate_TatteredHide = {}
#Peureki
droprate_TatteredHide['Copper'] = {'Rawhide Leather Section':1.84}
droprate_TatteredHide['Runecrafter'] = {'Rawhide Leather Section':1.79}
droprate_TatteredHide['Rare'] = {'Rawhide Leather Section':1.87}

#Rawhide Leather Strap
droprate_RawhideLeatherStrap = {}
#Peureki
droprate_RawhideLeatherStrap['Copper'] = {'Rawhide Leather Section':1.788}
droprate_RawhideLeatherStrap['Runecrafter'] = {'Rawhide Leather Section':1.848}
droprate_RawhideLeatherStrap['Rare'] = {'Rawhide Leather Section':1.9}

#Tattered Pelt
droprate_TatteredPelt = {}
#Peureki
droprate_TatteredPelt['Copper'] = {'Rawhide Leather Section':1.9}
droprate_TatteredPelt['Runecrafter'] = {'Rawhide Leather Section':1.92}
droprate_TatteredPelt['Rare'] = {'Rawhide Leather Section':1.87}

""" T2 """
#Ripped Hide
droprate_RippedHide = {}
#Peureki
droprate_RippedHide['Copper'] = {'Rawhide Leather Section':0.46,'Thin Leather Section':1.33}
droprate_RippedHide['Runecrafter'] = {'Rawhide Leather Section':0.35,'Thin Leather Section':1.48}
droprate_RippedHide['Rare'] = {'Rawhide Leather Section':0.35,'Thin Leather Section':1.57}

#Thin Leather Strap
droprate_ThinLeatherStrap = {}
#Peureki
droprate_ThinLeatherStrap['Copper'] = {'Rawhide Leather Section':0.55,'Thin Leather Section':1.29}
droprate_ThinLeatherStrap['Runecrafter'] = {'Rawhide Leather Section':0.41,'Thin Leather Section':1.38}
droprate_ThinLeatherStrap['Rare'] = {'Rawhide Leather Section':0.35,'Thin Leather Section':1.59}

#Ripped Pelt
droprate_RippedPelt = {}
#Peureki
droprate_RippedPelt['Copper'] = {'Rawhide Leather Section':0.58,'Thin Leather Section':1.18}
droprate_RippedPelt['Runecrafter'] = {'Rawhide Leather Section':0.45,'Thin Leather Section':1.44}
droprate_RippedPelt['Rare'] = {'Rawhide Leather Section':0.35,'Thin Leather Section':1.56}


""" T3 """
#Torn Hide
droprate_TornHide = {}
#Peureki
droprate_TornHide['Copper'] = {'Thin Leather Section':0.48,'Coarse Leather Section':1.41}
droprate_TornHide['Runecrafter'] = {'Thin Leather Section':0.26,'Coarse Leather Section':1.6}
droprate_TornHide['Rare'] = {'Thin Leather Section':0.32,'Coarse Leather Section':1.6}

#Coarse Leather Strap
droprate_CoarseLeatherStrap = {}
#Peureki
droprate_CoarseLeatherStrap['Copper'] = {'Thin Leather Section':0.422,'Coarse Leather Section':1.38}
droprate_CoarseLeatherStrap['Runecrafter'] = {'Thin Leather Section':0.348,'Coarse Leather Section':1.44}
droprate_CoarseLeatherStrap['Rare'] = {'Thin Leather Section':0.456,'Coarse Leather Section':1.42}

#Torn Pelt
droprate_TornPelt = {}
#Peureki
droprate_TornPelt['Copper'] = {'Thin Leather Section':0.38,'Coarse Leather Section':1.48}
droprate_TornPelt['Runecrafter'] = {'Thin Leather Section':0.26,'Coarse Leather Section':1.6}
droprate_TornPelt['Rare'] = {'Thin Leather Section':0.32,'Coarse Leather Section':1.6}

""" T4 """
#Frayed Hide
droprate_FrayedHide={}
#Peu
droprate_FrayedHide['Copper']={'Coarse Leather Section':0.57,'Rugged Leather Section':1.16}
#mine
droprate_FrayedHide['Runecrafter']={'Coarse Leather Section':0.4167,'Rugged Leather Section':1.4132}
droprate_FrayedHide['Rare']={'Coarse Leather Section':0.3641,'Rugged Leather Section':1.5538}

#Thick Leather Strap
droprate_ThickLeatherStrap = {}
#Peureki
droprate_ThickLeatherStrap['Copper'] = {'Coarse Leather Section':0.52,'Rugged Leather Section':1.24}
droprate_ThickLeatherStrap['Runecrafter'] = {'Coarse Leather Section':0.29,'Rugged Leather Section':1.64}
droprate_ThickLeatherStrap['Rare'] = {'Coarse Leather Section':0.3,'Rugged Leather Section':1.53}

#Frayed Pelt
droprate_FrayedPelt = {}
#Peureki
droprate_FrayedPelt['Copper'] = {'Coarse Leather Section':0.52,'Rugged Leather Section':1.22}
droprate_FrayedPelt['Runecrafter'] = {'Coarse Leather Section':0.36,'Rugged Leather Section':1.4}
droprate_FrayedPelt['Rare'] = {'Coarse Leather Section':0.3,'Rugged Leather Section':1.62}

""" T5 """
#Filthy Hide
droprate_FilthyHIde = {}
#Peureki
droprate_FilthyHIde['Copper'] = {'Rugged Leather Section':1.36,'Thick Leather Section':0.4}
droprate_FilthyHIde['Runecrafter'] = {'Rugged Leather Section':0.7,'Thick Leather Section':0.96}
droprate_FilthyHIde['Rare'] = {'Rugged Leather Section':0.78,'Thick Leather Section':1.08}

#Rugged Leather Strap
droprate_RuggedLeatherStrap = {}
#Peureki
droprate_RuggedLeatherStrap['Copper'] = {'Rugged Leather Section':1.12,'Thick Leather Section':0.62}
droprate_RuggedLeatherStrap['Runecrafter'] = {'Rugged Leather Section':1.02,'Thick Leather Section':0.77}
droprate_RuggedLeatherStrap['Rare'] = {'Rugged Leather Section':0.83,'Thick Leather Section':0.9}

#Filthy Pelt
droprate_FilthyPelt = {}
#Peureki
droprate_FilthyPelt['Copper'] = {'Rugged Leather Section':1.28,'Thick Leather Section':0.48}
droprate_FilthyPelt['Runecrafter'] = {'Rugged Leather Section':1.24,'Thick Leather Section':0.58}
droprate_FilthyPelt['Rare'] = {'Rugged Leather Section':0.98,'Thick Leather Section':0.84}

""" T6 """
#Salvageable Hide
droprate_SalvageableHide = {}
#Peureki
droprate_SalvageableHide['Copper'] = {'Thick Leather Section':1.316,'Hardened Leather Section':0.064}
droprate_SalvageableHide['Runecrafter'] = {'Thick Leather Section':1.3,'Hardened Leather Section':0.076}
droprate_SalvageableHide['Rare'] = {'Thick Leather Section':1.236,'Hardened Leather Section':0.1}

#Hard Leather Strap
droprate_HardLeatherStrap={}
#Mine
droprate_HardLeatherStrap['Copper'] = {'Thick Leather Section':1.2844,'Hardened Leather Section':0.0791}
droprate_HardLeatherStrap['Runecrafter'] = {'Thick Leather Section':1.3045,'Hardened Leather Section':0.0813}
droprate_HardLeatherStrap['Rare'] = {'Thick Leather Section':1.2588,'Hardened Leather Section':0.0975}

#Salvageable Pelt
droprate_SalvageablePelt = {}
#Peureki
droprate_SalvageablePelt['Copper'] = {'Thick Leather Section':1.24,'Hardened Leather Section':0.100}
droprate_SalvageablePelt['Runecrafter'] = {'Thick Leather Section':1.21,'Hardened Leather Section':0.11}
droprate_SalvageablePelt['Rare'] = {'Thick Leather Section':1.22,'Hardened Leather Section':0.11}

""" All Tiers """
#Unstable Hide
droprate_UnstableHide = {}
#My data
droprate_UnstableHide['Copper'] = {'Rawhide Leather Section':0.1822,'Thin Leather Section':0.4846,'Coarse Leather Section':0.4884,'Rugged Leather Section':0.4612,'Thick Leather Section':0.1537,'Hardened Leather Section':0.3004}
droprate_UnstableHide['Runecrafter'] = {'Rawhide Leather Section':0.1746,'Thin Leather Section':0.4780,'Coarse Leather Section':0.4793,'Rugged Leather Section':0.4920,'Thick Leather Section':0.1646,'Hardened Leather Section':0.3170}
droprate_UnstableHide['Rare'] = {'Rawhide Leather Section':0.1747,'Thin Leather Section':0.4603,'Coarse Leather Section':0.4833,'Rugged Leather Section':0.5240,'Thick Leather Section':0.1606,'Hardened Leather Section':0.3366}

#Bloodstone-Warped Hide
droprate_BloodstoneWarpedHide={}
#my data only
droprate_BloodstoneWarpedHide['Copper'] = {'Rawhide Leather Section':0.0462,'Thin Leather Section':0.0533,'Coarse Leather Section':0.0445,'Rugged Leather Section':0.0467,'Thick Leather Section':0.4533,'Hardened Leather Section':0.4714}
droprate_BloodstoneWarpedHide['Runecrafter'] = {'Rawhide Leather Section':0.0483,'Thin Leather Section':0.0463,'Coarse Leather Section':0.0461,'Rugged Leather Section':0.0468,'Thick Leather Section':0.4820,'Hardened Leather Section':0.5337}
droprate_BloodstoneWarpedHide['Rare'] = {'Rawhide Leather Section':0.0534,'Thin Leather Section':0.0647,'Coarse Leather Section':0.0605,'Rugged Leather Section':0.0578,'Thick Leather Section':0.4863,'Hardened Leather Section':0.5581}


"""
Drop rates: Cloth
"""

""" T1 """
#Shredded Garment
droprate_ShreddedGarment = {}
#Peureki
droprate_ShreddedGarment['Copper']={'Jute Scrap':1.884}
droprate_ShreddedGarment['Runecrafter']={'Jute Scrap':1.836}
droprate_ShreddedGarment['Rare']={'Jute Scrap':2.016}

#Half-Eaten Mass
droprate_HalfEatenMass = {}
#Peureki
droprate_HalfEatenMass['Copper']={'Jute Scrap':1.73}
droprate_HalfEatenMass['Runecrafter']={'Jute Scrap':1.74}
droprate_HalfEatenMass['Rare']={'Jute Scrap':1.89}

#Shredded Rag
droprate_ShreddedRag = {}
#Peureki
droprate_ShreddedRag['Copper']={'Jute Scrap':1.784}
droprate_ShreddedRag['Runecrafter']={'Jute Scrap':1.844}
droprate_ShreddedRag['Rare']={'Jute Scrap':1.852}

""" T2 """
#Worn Garment
droprate_WornGarment = {}
#me
droprate_WornGarment['Copper']={'Jute Scrap':0.3560,'Wool Scrap':1.4320}
droprate_WornGarment['Runecrafter']={'Jute Scrap':0.4232,'Wool Scrap':1.4232}
droprate_WornGarment['Rare']={'Jute Scrap':0.3938,'Wool Scrap':1.4831}

#Decaying
droprate_DecayingMass = {}
#Peureki
droprate_DecayingMass['Copper']={'Jute Scrap':0.4,'Wool Scrap':1.42}
droprate_WornGarment['Runecrafter']={'Jute Scrap':0.68,'Wool Scrap':1.24}
droprate_WornGarment['Rare']={'Jute Scrap':0.38,'Wool Scrap':1.44}

#Worn Rag
droprate_WornRag = {}
#Me
droprate_WornRag['Copper']={'Jute Scrap':0.4772,'Wool Scrap':1.3423}
droprate_WornRag['Runecrafter']={'Jute Scrap':0.4283,'Wool Scrap':1.3811}
droprate_WornRag['Rare']={'Jute Scrap':0.3742,'Wool Scrap':1.5470}

""" T3 """
#Ragged Garment
droprate_RaggedGarment = {}
#Peu
droprate_RaggedGarment['Copper']={'Wool Scrap':00.492,'Cotton Scrap':1.372}
droprate_RaggedGarment['Runecrafter']={'Wool Scrap':00.416,'Cotton Scrap':1.424}
droprate_RaggedGarment['Rare']={'Wool Scrap':00.34,'Cotton Scrap':1.522}

#Fetid Mass
droprate_FetidMass = {}
#Peu
droprate_FetidMass['Copper']={'Wool Scrap':00.28,'Cotton Scrap':1.44}
droprate_FetidMass['Runecrafter']={'Wool Scrap':00.46,'Cotton Scrap':1.4}
droprate_FetidMass['Rare']={'Wool Scrap':00.26,'Cotton Scrap':1.54}

#Soiled Rag
droprate_SoiledRag = {}
#Peu
droprate_SoiledRag['Copper']={'Wool Scrap':00.36,'Cotton Scrap':1.54}
droprate_SoiledRag['Runecrafter']={'Wool Scrap':00.34,'Cotton Scrap':1.45}
droprate_SoiledRag['Rare']={'Wool Scrap':00.34,'Cotton Scrap':1.38}

""" T4 """
#Frayed Garment
droprate_FrayedGarment = {}
#wiki
droprate_FrayedGarment['Copper']={'Cotton Scrap':00.55,'Linen Scrap':1.25}
#Peu
droprate_FrayedGarment['Runecrafter']={'Cotton Scrap':00.484,'Linen Scrap':1.4}
droprate_FrayedGarment['Rare']={'Cotton Scrap':00.432,'Linen Scrap':0.976}

#Malodorous Mass
droprate_MalodorousMass = {}
#Peu
droprate_MalodorousMass['Copper']={'Cotton Scrap':00.43,'Linen Scrap':1.36}
droprate_MalodorousMass['Runecrafter']={'Cotton Scrap':00.45,'Linen Scrap':1.5}
droprate_MalodorousMass['Rare']={'Cotton Scrap':00.37,'Linen Scrap':1.46}

#Frayed Rag
droprate_FrayedRag = {}
#Peu
droprate_FrayedRag['Copper']={'Cotton Scrap':00.488,'Linen Scrap':1.308}
droprate_FrayedRag['Runecrafter']={'Cotton Scrap':00.424,'Linen Scrap':1.484}
droprate_FrayedRag['Rare']={'Cotton Scrap':00.324,'Linen Scrap':1.556}

""" T5 """
#Torn Garment
droprate_TornGarment = {}
#Peu
droprate_TornGarment['Copper']={'Linen Scrap':00.428,'Silk Scrap':1.4}
droprate_TornGarment['Runecrafter']={'Linen Scrap':00.436,'Silk Scrap':1.356}
droprate_TornGarment['Rare']={'Linen Scrap':00.448,'Silk Scrap':1.46}

#Half-Digested Mass
droprate_HalfDigestedMass = {}
#Peu
droprate_HalfDigestedMass['Copper']={'Linen Scrap':00.32,'Silk Scrap':1.42}
droprate_HalfDigestedMass['Runecrafter']={'Linen Scrap':00.53,'Silk Scrap':1.27}
droprate_HalfDigestedMass['Rare']={'Linen Scrap':00.35,'Silk Scrap':1.51}

#Torn Rag
droprate_TornRag = {}
#Peu
droprate_TornRag['Copper']={'Linen Scrap':00.35,'Silk Scrap':1.47}
droprate_TornRag['Runecrafter']={'Linen Scrap':00.43,'Silk Scrap':1.36}
#wiki
droprate_TornRag['Rare']={'Linen Scrap':00.324,'Silk Scrap':1.596}

""" T6 """
#Discarded Garment
droprate_DiscardedGarment = {}
#Peu
droprate_DiscardedGarment['Copper']={'Silk Scrap':1.31,'Gossamer Scrap':00.098}
droprate_DiscardedGarment['Runecrafter']={'Silk Scrap':1.366,'Gossamer Scrap':00.081}
droprate_DiscardedGarment['Rare']={'Silk Scrap':1.296,'Gossamer Scrap':00.121}

#Regurgitated Mass
droprate_RegurgitatedMass = {}
#Peu
droprate_RegurgitatedMass['Copper']={'Silk Scrap':1.61,'Gossamer Scrap':00.1}
droprate_RegurgitatedMass['Runecrafter']={'Silk Scrap':1.5,'Gossamer Scrap':00.13}
droprate_RegurgitatedMass['Rare']={'Silk Scrap':1.49,'Gossamer Scrap':00.08}

#Rag
droprate_Rag = {}
#Peu
droprate_Rag['Copper']={'Silk Scrap':1.596,'Gossamer Scrap':00.076}
droprate_Rag['Runecrafter']={'Silk Scrap':1.53,'Gossamer Scrap':00.124}
droprate_Rag['Rare']={'Silk Scrap':1.55,'Gossamer Scrap':00.104}

""" Additional Garments """
#Garment 28
droprate_Garment28 = {}
#No data anywhere. Placehoder for completeness
droprate_Garment28['Copper']={'Linen Scrap':00.00,'Silk Scrap':00.00}
droprate_Garment28['Runecrafter']={'Linen Scrap':00.00,'Silk Scrap':00.00}
droprate_Garment28['Rare']={'Linen Scrap':00.00,'Silk Scrap':00.00}

#Garment 32
droprate_Garment32 = {}
#No data anywhere. Placehoder for completeness
droprate_Garment32['Copper']={'Linen Scrap':00.00,'Silk Scrap':00.00}
droprate_Garment32['Runecrafter']={'Linen Scrap':00.00,'Silk Scrap':00.00}
droprate_Garment32['Rare']={'Linen Scrap':00.00,'Silk Scrap':00.00}

""" All Tiers """
#Unstable Cloth
droprate_UnstableRag = {}
#Peu
droprate_UnstableRag['Copper']={'Jute Scrap':0.1855,'Wool Scrap':0.5135,'Cotton Scrap':0.4850,'Linen Scrap':0.5166,'Silk Scrap':0.1855,'Gossamer Scrap':0.1917}
droprate_UnstableRag['Runecrafter']={'Jute Scrap':0.1746,'Wool Scrap':0.5373,'Cotton Scrap':0.5317,'Linen Scrap':0.4857,'Silk Scrap':0.1833,'Gossamer Scrap':0.1825}
droprate_UnstableRag['Rare']={'Jute Scrap':0.1604,'Wool Scrap':0.5076,'Cotton Scrap':0.5761,'Linen Scrap':0.4855,'Silk Scrap':0.2109,'Gossamer Scrap':0.1680}

"""
Drop rates: Wood
"""
#Yes, there's only 1
droprate_ReclaimedWoodChunk={}
#Wiki
droprate_ReclaimedWoodChunk['Copper']={'Green Wood Log':0.102,'Soft Wood Log':0.4703,'Seasoned Wood Log':0.504,'Hard Wood Log':0.5206,'Elder Wood Log':0.163,'Ancient Wood Log':0.277}
#Peu
droprate_ReclaimedWoodChunk['Runecrafter']={'Green Wood Log':0.109,'Soft Wood Log':0.523,'Seasoned Wood Log':0.546,'Hard Wood Log':0.436,'Elder Wood Log':0.178,'Ancient Wood Log':0.344}
droprate_ReclaimedWoodChunk['Rare']={'Green Wood Log':0.12,'Soft Wood Log':0.459,'Seasoned Wood Log':0.511,'Hard Wood Log':0.469,'Elder Wood Log':0.149,'Ancient Wood Log':0.331}


"""
Helper stuff
"""

#All relevant IDs
allIDs =    [79423,#Wood salvage
            21690,21678,21691,21679,21692,21680,21693,21681,21694,21682,21695,21683,79079,#Metal salvage
            21661,21684,21653,21664,21685,21654,21667,21686,21655,21668,21687,21656,21670,21688,21657,22331,21689,21658,79213,80681,#Leather salvage
            21669,22325,21659,21671,22326,21660,21672,22327,21662,21673,22328,21663,21674,22329,21665,21675,22330,21666,79138,#Cloth salvage
            21676,21677,#The random other Rags
            19723,19726,19727,19724,19722,19725,#raw wood
            19710,19713,19714,19711,19709,19712,#refined wood
            19697,19703,19699,19698,19702,19700,19701,#raw metal
            19680,19679,19687,19683,19688,19682,19686,19681,19684,19685,#refined metal
            19718,19739,19741,19743,19748,19745,#raw cloth
            19720,19740,19742,19744,19747,19746,#refined cloth
            19719,19728,19730,19731,19729,19732,#raw leather
            19738,19733,19734,19736,19735,19737]#refined leather

#Salvage options
#salvageOptions 'Mystic':10.5, 'Copper':5 , 'Runecrafter':30, 'Silver':60
salvageCost = {'Copper':5 , 'Runecrafter':30, 'Rare':60}

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
#I don't think I need this

"""
Main Program
"""
if __name__ == '__main__':
    #Import new common helper file
    from calc_helpers import *
    #Python GW2 API wrapper library
    from gw2api import GuildWars2Client
    gw2_client = GuildWars2Client()

    allAPI=gw2_client.commerceprices.get(ids=allIDs)

    unrefined_prices, refined_prices, salvageLeather, salvageWood, salvageMetal, salvageCloth = sort_allAPI(allAPI)

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
    worthbuyinglist=[]
    print('\n','#'*10,"Metal",'#'*10)

    #T1
    worthbuyinglist.append(salvagePrint('Bit of Metal Scrap',salvageMetal,multiplier_prices,droprate_BitofMetalScrap,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Brittle Clump of Ore',salvageMetal,multiplier_prices,droprate_BrittleClumpofOre,salvageCost,0))
    #T2
    worthbuyinglist.append(salvagePrint('Weak Clump of Ore',salvageMetal,multiplier_prices,droprate_WeakClumpofOre,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Pile of Metal Scrap',salvageMetal,multiplier_prices,droprate_PileofMetalScrap,salvageCost,0))
    #T3
    worthbuyinglist.append(salvagePrint('Clump of Ore',salvageMetal,multiplier_prices,droprate_ClumpofOre,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Jagged Metal Scrap',salvageMetal,multiplier_prices,droprate_JaggedMetalScrap,salvageCost,0))
    #T4
    worthbuyinglist.append(salvagePrint('Laden Clump of Ore',salvageMetal,multiplier_prices,droprate_LadenClumpofOre,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Metal Scrap',salvageMetal,multiplier_prices,droprate_MetalScrap,salvageCost,0))
    #T5
    worthbuyinglist.append(salvagePrint('Loaded Clump of Ore',salvageMetal,multiplier_prices,droprate_LoadedClumpofOre,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Salvageable Metal Scrap',salvageMetal,multiplier_prices,droprate_SalvageableMetalScrap,salvageCost,0))
    #T6
    worthbuyinglist.append(salvagePrint('Rich Clump of Ore',salvageMetal,multiplier_prices,droprate_RichClumpofOre,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Valuable Metal Scrap',salvageMetal,multiplier_prices,droprate_ValuableMetalScrap,salvageCost,0))
    #All
    worthbuyinglist.append(salvagePrint('Unstable Metal Chunk',salvageMetal,multiplier_prices,droprate_UnstableMetalChunk,salvageCost,0))


    print('\n','#'*10,"Metal / / / Leather",'#'*10)

    #T1
    worthbuyinglist.append(salvagePrint('Tattered Hide',salvageLeather,multiplier_prices,droprate_TatteredHide,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Rawhide Leather Strap',salvageLeather,multiplier_prices,droprate_RawhideLeatherStrap,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Tattered Pelt',salvageLeather,multiplier_prices,droprate_TatteredPelt,salvageCost,0))

    #T2
    worthbuyinglist.append(salvagePrint('Ripped Hide',salvageLeather,multiplier_prices,droprate_RippedHide,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Thin Leather Strap',salvageLeather,multiplier_prices,droprate_ThinLeatherStrap,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Ripped Pelt',salvageLeather,multiplier_prices,droprate_RippedPelt,salvageCost,0))

    #T3
    worthbuyinglist.append(salvagePrint('Torn Hide',salvageLeather,multiplier_prices,droprate_TornHide,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Coarse Leather Strap',salvageLeather,multiplier_prices,droprate_CoarseLeatherStrap,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Torn Pelt',salvageLeather,multiplier_prices,droprate_TornPelt,salvageCost,0))

    #T4
    worthbuyinglist.append(salvagePrint('Frayed Hide',salvageLeather,multiplier_prices,droprate_FrayedHide,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Thick Leather Strap',salvageLeather,multiplier_prices,droprate_ThickLeatherStrap,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Frayed Pelt',salvageLeather,multiplier_prices,droprate_FrayedPelt,salvageCost,0))

    #T5
    worthbuyinglist.append(salvagePrint('Filthy Hide',salvageLeather,multiplier_prices,droprate_FilthyHIde,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Rugged Leather Strap',salvageLeather,multiplier_prices,droprate_RuggedLeatherStrap,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Filthy Pelt',salvageLeather,multiplier_prices,droprate_FilthyPelt,salvageCost,0))

    #T6
    worthbuyinglist.append(salvagePrint('Salvageable Hide',salvageLeather,multiplier_prices,droprate_SalvageableHide,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Hard Leather Strap',salvageLeather,multiplier_prices,droprate_HardLeatherStrap,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Salvageable Pelt',salvageLeather,multiplier_prices,droprate_SalvageablePelt,salvageCost,0))

    #All
    worthbuyinglist.append(salvagePrint('Unstable Hide',salvageLeather,multiplier_prices,droprate_UnstableHide,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Bloodstone-Warped Hide',salvageLeather,multiplier_prices,droprate_BloodstoneWarpedHide,salvageCost,0))

    print('\n','#'*10,"Leather / / / Cloth",'#'*10)

    #T1
    worthbuyinglist.append(salvagePrint('Shredded Garment',salvageCloth,multiplier_prices,droprate_ShreddedGarment,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Half-Eaten Mass',salvageCloth,multiplier_prices,droprate_HalfEatenMass,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Shredded Rag',salvageCloth,multiplier_prices,droprate_ShreddedRag,salvageCost,0))

    #T2
    worthbuyinglist.append(salvagePrint('Worn Garment',salvageCloth,multiplier_prices,droprate_WornGarment,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Decaying Mass',salvageCloth,multiplier_prices,droprate_DecayingMass,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Worn Rag',salvageCloth,multiplier_prices,droprate_WornRag,salvageCost,0))

    #T3
    worthbuyinglist.append(salvagePrint('Ragged Garment',salvageCloth,multiplier_prices,droprate_RaggedGarment,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Fetid Mass',salvageCloth,multiplier_prices,droprate_FetidMass,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Soiled Rag',salvageCloth,multiplier_prices,droprate_SoiledRag,salvageCost,0))

    #T4
    worthbuyinglist.append(salvagePrint('Frayed Garment',salvageCloth,multiplier_prices,droprate_FrayedGarment,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Malodorous Mass',salvageCloth,multiplier_prices,droprate_MalodorousMass,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Frayed Rag',salvageCloth,multiplier_prices,droprate_FrayedRag,salvageCost,0))

    #T5
    worthbuyinglist.append(salvagePrint('Torn Garment',salvageCloth,multiplier_prices,droprate_TornGarment,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Half-Digested Mass',salvageCloth,multiplier_prices,droprate_HalfDigestedMass,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Torn Rag',salvageCloth,multiplier_prices,droprate_TornRag,salvageCost,0))

    #T6
    worthbuyinglist.append(salvagePrint('Discarded Garment',salvageCloth,multiplier_prices,droprate_DiscardedGarment,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Regurgitated Mass',salvageCloth,multiplier_prices,droprate_RegurgitatedMass,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Rag',salvageCloth,multiplier_prices,droprate_Rag,salvageCost,0))

    #Extra Garments
    worthbuyinglist.append(salvagePrint('Garment_28',salvageCloth,multiplier_prices,droprate_Garment28,salvageCost,0))
    worthbuyinglist.append(salvagePrint('Garment_32',salvageCloth,multiplier_prices,droprate_Garment32,salvageCost,0))

    #All
    worthbuyinglist.append(salvagePrint('Unstable Rag',salvageCloth,multiplier_prices,droprate_UnstableRag,salvageCost,0))

    print('\n','#'*10,"Cloth / / / Wood",'#'*10)

    worthbuyinglist.append(salvagePrint('Reclaimed Wood Chunk',salvageWood,multiplier_prices,droprate_ReclaimedWoodChunk,salvageCost,0))

    print('\n','#'*10,"Wood / / / Summary ",'#'*10)
    #Filter and sort the levels of "buy" using sorted and list comprehension. Don't care if swapping to a generator would be faster and more memory efficient
    #x[2] is called in key because I want to sort based on profit amount, not profit percent at this moment
    #Reverse gives me hightest first
    #list of lists prints on a single line and I want 1 list per line so this is asssembled in a for loop
    #This is Good candidate for refactoring into a function
    #I am fine with the list formatting rather than a table
    for x in sorted( [x for x in worthbuyinglist if 'MEGA BUY' in x ],key=lambda x:x[2], reverse=True):
        print(x)
    for x in sorted( [x for x in worthbuyinglist if 'BUYBUYBUY' in x ],key=lambda x:x[2], reverse=True):
        print(x)
    for x in sorted( [x for x in worthbuyinglist if 'Good' in x ],key=lambda x:x[2], reverse=True):
        print(x)
    for x in sorted( [x for x in worthbuyinglist if 'Consider' in x ],key=lambda x:x[2], reverse=True):
        print(x)
