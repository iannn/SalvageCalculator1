#This is a basic scrip for calculating the value of unidentified gear TO Sell
#SAVINGS not currently calculated
#This only looks at current prices. Price walls, fractional differences between raw cost/material and refined cost/material, and very low offers aren't considered
"""Unidentified Gear Overview

There are 3 types of unidentified gear:
    Common Unidentified Gear = Blue = fine gear
    Unidentified Gear = Green = Masterwork
    Rare Unidentified Gear = Yellow = Rare


This script should show the following:
    Buy and Sell prices for each type of gear
    Buy and Sell prices for each of the outputs
    Buy low - process - sell high profits
    Savings from processing gear instead of buying from TP

Eventually:
    Compute the 4 combinations of buy-sell profits for unid and outputs
    How many unids I'd need to salvage to get X amount of material

"""

"""Program Flow

This first attempt is very fixed so it will be very stupid
Do not worry about what happens if you reduce the cost by 1c here and there

Get get TP values
Get list of materials to refine for better profit
Calculate unidentified gear salvage value with best profit material option (raw vs refined)
Generate report

To add/deal with more granular stuff eventually:
Decide which unidentified gear to process
Savings of salvaging vs buying

"""

"""API items and numbers

Unidentified Gear:
    85016=Piece of Common Unidentified Gear (Fine, Blue)
    84731=Piece of Unidentified Gear (Masterwork, Green)
    83008=Piece of Rare Unidentified Gear (Rare, Yellow)

Salvage Materials:
    19701=Orichalcum Ore
    19725=Ancient Wood Log
    19745=Gossamer Scrap
    19732=Hardened Leather Section

    19700=Mithril Ore
    19722=Elder Wood Log
    19748=Silk Scrap
    19729=Thick Leather Square

    19721=Ectoplasm
    89140=Lucent Mote

    89098=Symbol of Control
    89141=Symbol of Enhancement
    89182=Symbol of Pain

    89103=Charm of Brilliance
    89258=Charm of Potence
    89216=Charm of Skill

    Luck (there are multiple lucks so no API calls for this)


Refinement Materials:
    19685=Orichalcum Ingot
    19712=Ancient Wood Plank
    19746=Bolt of Gossamer
    19737=Cured Hardened Leather Square

    19684=Mithril Ingot
    19709=Elder Wood Plank
    19747=Bolt of Silk
    19735=Cured Thick Leather Square

    89271=Pile of Lucent Crystal


Refinement Equations:
    1x Orichalcum Ingot = 2x Orichalcum Ore
    1x Ancient Wood Plank = 3x Ancient Wood Log
    1x Bolt of Gossamer = 2x Gossamer Scrap
    1x Cured Hardened Leather Square = 3x Hardened Leather Section

    1x Mithril Ingot = 2x Mithril Ore
    1x Elder Wood Plank = 3x Elder Wood Log
    1x Bolt of Silk = 3x Silk Scrap
    1x Cured Thick Leather Square = 4x Thick Leather Square

    1x Pile of Lucent Crystal = 10x Lucent Mote


"""

"""Processing notes

With a Masters/Mystic salvage kit, it's about 0.85 ecto per rare
https://wiki.guildwars2.com/wiki/Silver-Fed_Salvage-o-Matic


"""

"""
Function Declarations
"""

#Main gw2 API call return list of dics that may not always be in the same order so filter and arrange data for unids here
def sort_allAPI(allAPI):

    """Design Note:
    A dictionary with the key:value pair id:name  is needed for this to work because these are sorting commerceprices data from the API, and only returns the following:
    {'id': 79423, 'whitelisted': False, 'buys': {'quantity': 13684, 'unit_price': 114}, 'sells': {'quantity': 22649, 'unit_price': 119}}
    """
    api_unid_prices = {85016:'Fine',84731:'Masterwork',83008:'Rare'}
    api_unrefined_prices = {19701:'Orichalcum Ore',19725:'Ancient Wood Log',19745:'Gossamer Scrap',19732:'Hardened Leather Section',
                            19700:'Mithril Ore',19722:'Elder Wood Log',19748:'Silk Scrap',19729:'Thick Leather Square',
                            19721:'Ectoplasm',
                            89140:'Lucent Mote',
                            89098:'Symbol of Control',89141:'Symbol of Enhancement',89182:'Symbol of Pain',
                            89103:'Charm of Brilliance',89258:'Charm of Potence',89216:'Charm of Skill'}
    api_refined_prices = {19685:'Orichalcum Ingot',19712:'Ancient Wood Plank',19746:'Bolt of Gossamer',19737:'Cured Hardened Leather Square',
                        19684:'Mithril Ingot',19709:'Elder Wood Plank',19747:'Bolt of Silk',19735:'Cured Thick Leather Square',
                        89271:'Pile of Lucent Crystal'}

    #Return dictionaries with 'item':[buy sell] key:value pairs
    unid_prices= {}
    unrefined_prices = {}
    refined_prices = {}

    for entryAPI in allAPI:
        if entryAPI['id'] in api_unid_prices:#special case because there's only 1
            unid_prices[api_unid_prices[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif entryAPI['id'] in api_unrefined_prices:
            unrefined_prices[api_unrefined_prices[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif entryAPI['id'] in api_refined_prices:
            refined_prices[api_refined_prices[entryAPI['id']]] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        else:
            print("Unexpected API return")
            print(entryAPI)

    return unid_prices,unrefined_prices,refined_prices
#End of sort_allAPI

#Formatted print function
def unidPrint(droprate_dict,salvageCost_val,unid_name,unid_price,sum_val):
    print('{print_outname:<16}: Buy order = {print_cost}; Average salvage cost = {print_salvageCost}; Average salvage value = {print_salvageValue}; Estimated {print_profit} profit per salvage'.format(print_outname=unid_name,print_cost=unid_price, print_salvageValue=round(sum_val,4), print_profit=round(sum_val-unid_price-salvageCost_val,4), print_salvageCost=salvageCost_val))
#End of unidPrint

"""
Drop Rates
"""

#charm and symbol values I have are low data so using wiki values
unidFine_droprate = {'Orichalcum Ore':0.0399,'Ancient Wood Log':0.0339,'Gossamer Scrap':0.0155,'Hardened Leather Section':0.0152,'Mithril Ore':0.4281,'Elder Wood Log':0.3869,'Silk Scrap':0.3013,'Thick Leather Square':0.2473,'Ectoplasm':0.0076,'Lucent Mote':0.1058,'Symbol of Control':0.0003,'Symbol of Enhancement':0.0002,'Symbol of Pain':0.0004,'Charm of Brilliance':0.0008,'Charm of Potence':0.0003,'Charm of Skill':0.0003}

#My data 19500
unidMasterwork_droprate = {'Orichalcum Ore':0.0390,'Ancient Wood Log':0.0280,'Gossamer Scrap':0.0185,'Hardened Leather Section':0.0180,'Mithril Ore':0.4434,'Elder Wood Log':0.3636,'Silk Scrap':0.3493,'Thick Leather Square':0.2782,'Ectoplasm':0.0287,'Lucent Mote':1.0483,'Symbol of Control':0.0015,'Symbol of Enhancement':0.0047,'Symbol of Pain':0.0035,'Charm of Brilliance':0.0049,'Charm of Potence':0.0027,'Charm of Skill':0.0031}

#pure wiki
unidRare_droprate = {'Orichalcum Ore':0.0407,'Ancient Wood Log':0.0295,'Gossamer Scrap':0.0165,'Hardened Leather Section':0.0153,'Mithril Ore':0.4611,'Elder Wood Log':0.3837,'Silk Scrap':0.3239,'Thick Leather Square':0.2556,'Ectoplasm':0.8751,'Lucent Mote':1.3881,'Symbol of Control':0.0035,'Symbol of Enhancement':0.0065,'Symbol of Pain':0.0029,'Charm of Brilliance':0.0056,'Charm of Potence':0.0033,'Charm of Skill':0.0034}
#,'Luck':-1 is out because I don't have value for this yet

#Never salvage with just one kit becuase better gear will come out
#Exotics are so rare that they will generate far more than the salvage + I may use BLKit
salvageCost = {'Mystic':10.5, 'Copper':5 , 'Runecrafter':30, 'Silver':60}
unidFine_salvageCost = round(salvageCost['Mystic']*0.0100 + salvageCost['Runecrafter']*0.0940 + salvageCost['Copper']*0.8950,4)
unidMasterwork_salvageCost = round(salvageCost['Mystic']*0.0336 + salvageCost['Runecrafter']*0.9638,4)
unidRare_salvageCost = round(salvageCost['Silver']*0.9840,4)


"""
Helper Stuff
"""

allIDs = [85016,84731,83008,#unidentified gear
        19701,19725,19745,19732,#T6
        19700,19722,19748,19729,#T5
        19721,89140,#Ecto and Lucent mote
        89098,89141,89182,#Symbol
        89103,89258,89216,#Charm
        19685,19712,19746,19737,#T6 refined
        19684,19709,19747,19735,#T5 refined
        89271]#Lucent crystal

#lookup unrefined to get refined
unrefined_to_refined = {'Orichalcum Ore':'Orichalcum Ingot','Ancient Wood Log':'Ancient Wood Plank','Gossamer Scrap':'Bolt of Gossamer','Hardened Leather Section':'Cured Hardened Leather Square','Mithril Ore':'Mithril Ingot','Elder Wood Log':'Elder Wood Plank','Silk Scrap':'Bolt of Silk','Thick Leather Square':'Cured Thick Leather Square','Lucent Mote':'Pile of Lucent Crystal'}
#Everything is based off of the raw material so use raw material as lookup.
refined_scalar = {'Orichalcum Ingot':2,'Ancient Wood Plank':3,'Bolt of Gossamer':2,'Cured Hardened Leather Square':3,'Mithril Ingot':2,'Elder Wood Plank':3,'Bolt of Silk':3,'Cured Thick Leather Square':4,'Pile of Lucent Crystal':10}

"""
Main Program start
"""
if __name__ == '__main__':
    #Common helper file
    from calc_helpers import *
    #Python GW2 API wrapper library
    from gw2api import GuildWars2Client
    gw2_client = GuildWars2Client()

    allAPI=gw2_client.commerceprices.get(ids=allIDs)

    unid_prices,unrefined_prices,refined_prices = sort_allAPI(allAPI)

    #sell value prices and decisions. No TP cut yet
    multiplier_prices,decision = generate_multiplier(unrefined_prices,refined_prices,refined_scalar,unrefined_to_refined,1)

    #TP cut included here
    unidFine_SalvageValue, unidFine_sum = compute_result(unidFine_droprate,multiplier_prices,True)
    unidMasterwork_salvageValue, unidMasterwork_sum = compute_result(unidMasterwork_droprate,multiplier_prices,True)
    unidRare_salvageValue, unidRare_sum = compute_result(unidRare_droprate,multiplier_prices,True)

    #Table. All columns fixed because same material/options for each unid. Except luck. Luck doesn't drop from rares apparently
    print('{:<24} : {:>10}   {:<10}   {:<5}   {:>10}   {:>10}   {:>10}   {:>10}'.format('Material','Sell Price','State','Raw','Refined','Fine','Masterwork','Rare'))
    print('-'*113)
    for key, value in multiplier_prices.items():
        if key in unrefined_to_refined:
            print('{:<24} : {:>10}   {:<10}   {:>5}   {:>10}   {:>10}   {:>10}   {:>10}'.format(key,value, decision[key],unrefined_prices[key][1],refined_prices[unrefined_to_refined[key]][1],unidFine_SalvageValue[key],unidMasterwork_salvageValue[key],unidRare_salvageValue[key]))
        else:
            print('{:<24} : {:>10}   {:<10}   {:>5}   {:>10}   {:>10}   {:>10}   {:>10}'.format(key,value, decision[key],'-','-',unidFine_SalvageValue[key],unidMasterwork_salvageValue[key],unidRare_salvageValue[key]))

    print('\nResult function: Sell')


    unidPrint(unidFine_droprate,unidFine_salvageCost,'Fine',unid_prices['Fine'][0],unidFine_sum)
    unidPrint(unidMasterwork_droprate,unidMasterwork_salvageCost,'Masterwork',unid_prices['Masterwork'][0],unidMasterwork_sum)
    unidPrint(unidRare_droprate,unidRare_salvageCost,'Rare',unid_prices['Rare'][0],unidRare_sum)

    #print('\nBuy testing')
    #buymultiplier,buydecisions = generate_multiplier(unrefined_prices,refined_prices,refined_scalar,unrefined_to_refined,1)
    #compute_result(unidFine_droprate,multiplier_prices,unidFine_salvageCost,'Fine',unid_prices['Fine'][0])

    print("The end")
