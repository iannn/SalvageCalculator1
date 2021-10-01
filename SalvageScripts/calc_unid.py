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
    19722=Elder Wood
    19748=Silk Scrap
    19729=Thick Leather Section

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

#Main gw2 API call return list of dics that may not always be in the same order so filter and arrange data for unids here
def sort_allAPI(allAPI):
    #Fill with api values
    unid_prices= {}
    unrefined_prices = {}
    refined_prices = {}
    other_prices = {}

    #assemble the dictionaries
    for entryAPI in allAPI:
        if(entryAPI['id']==85016):
            unid_prices['Fine'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==84731):
            unid_prices['Masterwork'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==83008):
            unid_prices['Rare'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19701):
            unrefined_prices['Orichalcum Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19725):
            unrefined_prices['Ancient Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19745):
            unrefined_prices['Gossamer Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19732):
            unrefined_prices['Hardened Leather Section'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19700):
            unrefined_prices['Mithril Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19722):
            unrefined_prices['Elder Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19748):
            unrefined_prices['Silk Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19729):
            unrefined_prices['Thick Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89140):
            unrefined_prices['Lucent Mote'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19721):
            other_prices['Ectoplasm'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89098):
            other_prices['Symbol of Control'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89141):
            other_prices['Symbol of Enhancement'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89182):
            other_prices['Symbol of Pain'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89103):
            other_prices['Charm of Brilliance'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89258):
            other_prices['Charm of Potence'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89216):
            other_prices['Charm of Skill'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19685):
            refined_prices['Orichalcum Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19712):
            refined_prices['Ancient Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19746):
            refined_prices['Bolt of Gossamer'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19737):
            refined_prices['Cured Hardened Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19684):
            refined_prices['Mithril Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19709):
            refined_prices['Elder Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19747):
            refined_prices['Bolt of Silk'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==19735):
            refined_prices['Cured Thick Leather Square'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        elif(entryAPI['id']==89271):
            refined_prices['Pile of Lucent Crystal'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]

        else:
            print("Unexpected API return")
            print(entryAPI)

        #Decision all finished
    return unid_prices,unrefined_prices,refined_prices,other_prices
#End of sort_allAPI

def generate_multiplier(unrefined_prices,refined_prices,refined_scaler,refined_lookup):
    #Input: unrefined material prices, refined material prices, the scaler values to get value of raw material from refined, lookup to get refined from unrefined
    #Output: multiplier for the best prices, the decision to refine or not

    #value per RAW MATERIAL goes into the multiplier dict, decision of raw/refined goes into decision dict
    #Compare and finalize values of material
    decision = {}
    multiplier_prices = {}


    """

    #TP cut to be added in later
    if(unrefined_prices['Orichalcum Ore'][1] > refined_prices['Orichalcum Ingot'][1]/2):
        decision['Orichalcum Ore'] = 'raw'
        multiplier_prices['Orichalcum Ore']=round(unrefined_prices['Orichalcum Ore'][1],4)
    else:
        decision['Orichalcum Ore'] = 'refined'
        multiplier_prices['Orichalcum Ore']=round(refined_prices['Orichalcum Ingot'][1]/2,4)

    if(unrefined_prices['Ancient Wood Log'][1] > refined_prices['Ancient Wood Plank'][1]/3):
        decision['Ancient Wood Log'] = 'raw'
        multiplier_prices['Ancient Wood Log']=round(unrefined_prices['Ancient Wood Log'][1],4)
    else:
        decision['Ancient Wood Log'] = 'refined'
        multiplier_prices['Ancient Wood Log']=round(refined_prices['Ancient Wood Plank'][1]/3,4)

    if(unrefined_prices['Gossamer Scrap'][1] > refined_prices['Bolt of Gossamer'][1]/2):
        decision['Gossamer Scrap'] = 'raw'
        multiplier_prices['Gossamer Scrap']=round(unrefined_prices['Gossamer Scrap'][1],4)
    else:
        decision['Gossamer Scrap'] = 'refined'
        multiplier_prices['Gossamer Scrap']=round(refined_prices['Bolt of Gossamer'][1]/2,4)

    if(unrefined_prices['Hardened Leather Section'][1] > refined_prices['Cured Hardened Leather Square'][1]/3):
        decision['Hardened Leather Section'] = 'raw'
        multiplier_prices['Hardened Leather Section']=round(unrefined_prices['Hardened Leather Section'][1],4)
    else:
        decision['Hardened Leather Section'] = 'refined'
        multiplier_prices['Hardened Leather Section']=round(refined_prices['Cured Hardened Leather Square'][1]/3,4)

    if(unrefined_prices['Mithril Ore'][1] > refined_prices['Mithril Ingot'][1]/2):
        decision['Mithril Ore'] = 'raw'
        multiplier_prices['Mithril Ore']=round(unrefined_prices['Mithril Ore'][1],4)
    else:
        decision['Mithril Ore'] = 'refined'
        multiplier_prices['Mithril Ore']=round(refined_prices['Mithril Ingot'][1]/2,4)

    if(unrefined_prices['Elder Wood Log'][1] > refined_prices['Elder Wood Plank'][1]/3):
        decision['Elder Wood Log'] = 'raw'
        multiplier_prices['Elder Wood Log']=round(unrefined_prices['Elder Wood Log'][1],4)
    else:
        decision['Elder Wood Log'] = 'refined'
        multiplier_prices['Elder Wood Log']=round(refined_prices['Elder Wood Plank'][1]/3,4)

    if(unrefined_prices['Silk Scrap'][1] > refined_prices['Bolt of Silk'][1]/3):
        decision['Silk Scrap'] = 'raw'
        multiplier_prices['Silk Scrap']=round(unrefined_prices['Silk Scrap'][1],4)
    else:
        decision['Silk Scrap'] = 'refined'
        multiplier_prices['Silk Scrap']=round(refined_prices['Bolt of Silk'][1]/3,4)

    if(unrefined_prices['Thick Leather Square'][1] > refined_prices['Cured Thick Leather Square'][1]/4):
        decision['Thick Leather Square'] = 'raw'
        multiplier_prices['Thick Leather Square']=round(unrefined_prices['Thick Leather Square'][1],4)
    else:
        decision['Thick Leather Square'] = 'refined'
        multiplier_prices['Thick Leather Square']=round(refined_prices['Cured Thick Leather Square'][1]/4,4)

    if(unrefined_prices['Lucent Mote'][1] > refined_prices['Pile of Lucent Crystal'][1]/10):
        decision['Lucent Mote'] = 'raw'
        multiplier_prices['Lucent Mote']=round(unrefined_prices['Lucent Mote'][1],4)
    else:
        decision['Lucent Mote'] = 'refined'
        multiplier_prices['Lucent Mote']=round(refined_prices['Pile of Lucent Crystal'][1]/10,4)
    #refine vs raw done. Include the other stuff now to finish multiplier_prices dict
    for key in other_prices:
        multiplier_prices[key] = other_prices[key][1]
"""
    return multiplier_prices,decision
#end of generate_multiplier

def compute_result(droprate_dict,multiplier_dict,salvageCost_val,unid_name):
    unid_salvageValue = {}
    unid_sum = 0

    for key in droprate_dict:
        unid_salvageValue[key] = round(0.85*unidFine_droprate[key]*multiplier_prices[key],4)
        unid_sum = unidFine_sum + unid_salvageValue[key]


    print('{outname:<16}: Buy order = {cost}; Average salvage cost = {salvageCost}; Average salvage value = {salvageValue}; Estimated {profit} profit per salvage'.format(outname=unid_name,cost=unid_prices['Fine'][0], salvageValue=round(unidFine_sum,4), profit=round(unidFine_sum-unid_prices['Fine'][0]-unidFine_salvageCost,4), salvageCost=unidFine_salvageCost))


"""
Main Program start
"""

from gw2api import GuildWars2Client
gw2_client = GuildWars2Client()

#charm and symbol values I have are low data so using wiki values
unidFine_droprate = {'Orichalcum Ore':0.0396,'Ancient Wood Log':0.0324,'Gossamer Scrap':0.0141,'Hardened Leather Section':0.0161,'Mithril Ore':0.4351,'Elder Wood Log':0.3879,'Silk Scrap':0.2964,'Thick Leather Square':0.2464,'Ectoplasm':0.0063,'Lucent Mote':0.1038,'Symbol of Control':0.0006,'Symbol of Enhancement':0.0001,'Symbol of Pain':0.0006,'Charm of Brilliance':0.0003,'Charm of Potence':0.0005,'Charm of Skill':0.0003}

#My data 19500
unidMasterwork_droprate = {'Orichalcum Ore':0.0388,'Ancient Wood Log':0.0280,'Gossamer Scrap':0.0184,'Hardened Leather Section':0.0179,'Mithril Ore':0.4416,'Elder Wood Log':0.3651,'Silk Scrap':0.3483,'Thick Leather Square':0.2824,'Ectoplasm':0.0293,'Lucent Mote':1.0643,'Symbol of Control':0.0013,'Symbol of Enhancement':0.0048,'Symbol of Pain':0.0036,'Charm of Brilliance':0.0048,'Charm of Potence':0.0024,'Charm of Skill':0.0032}

#pure wiki
unidRare_droprate = {'Orichalcum Ore':0.0407,'Ancient Wood Log':0.0295,'Gossamer Scrap':0.0165,'Hardened Leather Section':0.0153,'Mithril Ore':0.4611,'Elder Wood Log':0.3837,'Silk Scrap':0.3239,'Thick Leather Square':0.2556,'Ectoplasm':0.8751,'Lucent Mote':1.3881,'Symbol of Control':0.0035,'Symbol of Enhancement':0.0065,'Symbol of Pain':0.0029,'Charm of Brilliance':0.0056,'Charm of Potence':0.0033,'Charm of Skill':0.0034}
#,'Luck':-1 is out because I don't have value for this yet

#Never salvage with just one kit becuase better gear will come out
#Exotics are so rare that they will generate far more than the salvage + I may use BLKit
salvageCost = {'Mystic':10.5, 'Copper':5 , 'Runecrafter':30, 'Silver':60}
unidFine_salvageCost = salvageCost['Mystic']*0.0102 + salvageCost['Runecrafter']*0.0938 + salvageCost['Copper']*0.8951
unidMasterwork_salvageCost = salvageCost['Mystic']*0.0343 + salvageCost['Runecrafter']*0.9628
unidRare_salvageCost = salvageCost['Silver']*1

#Helper dictionaries
unrefined_to_refined = {'Orichalcum Ore':'Orichalcum Ingot','Ancient Wood Log':'Ancient Wood Plank','Gossamer Scrap':'Bolt of Gossamer','Hardened Leather Section':'Cured Hardened Leather Square','Mithril Ore':'Mithril Ingot','Elder Wood Log':'Elder Wood Plank','Silk Scrap':'Bolt of Silk','Thick Leather Square':'Cured Thick Leather Square','Lucent Mote':'Pile of Lucent Crystal'}
refined_scaler = {'Orichalcum Ingot':-1,'Ancient Wood Plank':-1}


#Final value calculation
unidFine_salvageValue = {}
unidMasterwork_salvageValue = {}
unidRare_salvageValue = {}

unidFine_sum = 0
unidMasterwork_sum = 0
unidRare_sum = 0



allIDs = [85016,84731,83008,#unidentified gear
        19701,19725,19745,19732,#T6
        19700,19722,19748,19729,#T5
        19721,89140,#Ecto and Lucent mote
        89098,89141,89182,#Symbol
        89103,89258,89216,#Charm
        19685,19712,19746,19737,#T6 refined
        19684,19709,19747,19735,#T5 refined
        89271]#Lucent crystal


allAPI=gw2_client.commerceprices.get(ids=allIDs)

unid_prices,unrefined_prices,refined_prices,other_prices = sort_allAPI(allAPI)

#Go through materials to see which are more profitable to be refined
#Right now, only care about buy low and sell high

multiplier_prices,decision = generate_multiplier(unrefined_prices.update(other_prices),refined_prices,)

#make new table. Include decision description if decision present
print('{:<24} : {:>10}   {:<10}   {:<10}   {:<10}'.format('Material','Sell Price','State','Raw','Refined'))
print('-'*74)
for key, value in multiplier_prices.items():
    if key in decision:
        print('{:<24} : {:>10}   {:<10}   {:<10}   {:<10}'.format(key,value, decision[key],unrefined_prices[key][1],refined_prices[unrefined_to_refined[key]][1]))
    else:
        print('{:<24} : {:>10}'.format(key,value))


#Calculation phase
#salvage value = drop rate * multiplier_prices
#Now I add in TP cut. Adding to salvage value is fine because the TP prices are on

#Fine
for key in unidFine_droprate:
    unidFine_salvageValue[key] = round(0.85*unidFine_droprate[key]*multiplier_prices[key],4)
    unidFine_sum = unidFine_sum + unidFine_salvageValue[key]

#Masterwork
for key in unidMasterwork_droprate:
    unidMasterwork_salvageValue[key] = round(0.85*unidMasterwork_droprate[key]*multiplier_prices[key],4)
    unidMasterwork_sum = unidMasterwork_sum + unidMasterwork_salvageValue[key]

#Rare
for key in unidRare_droprate:
    unidRare_salvageValue[key] = round(0.85*unidRare_droprate[key]*multiplier_prices[key],4)
    unidRare_sum = unidRare_sum + unidRare_salvageValue[key]


#Report time
print('Fine gear       : Buy order = {cost}; Average salvage cost = {salvageCost}; Average salvage value = {salvageValue}; Estimated {profit} profit per salvage'.format(cost=unid_prices['Fine'][0], salvageValue=round(unidFine_sum,4), profit=round(unidFine_sum-unid_prices['Fine'][0]-unidFine_salvageCost,4), salvageCost=unidFine_salvageCost))
print('Masterwork gear : Buy order = {cost}; Average salvage cost = {salvageCost}; Average salvage value = {salvageValue}; Estimated {profit} profit per salvage'.format(cost=unid_prices['Masterwork'][0], salvageValue=round(unidMasterwork_sum,4), profit=round(unidMasterwork_sum-unid_prices['Masterwork'][0]-unidMasterwork_salvageCost,4), salvageCost=unidMasterwork_salvageCost))
print('Rare gear       : Buy order = {cost}; Average salvage cost = {salvageCost}; Average salvage value = {salvageValue}; Estimated {profit} profit per salvage'.format(cost=unid_prices['Rare'][0], salvageValue=round(unidRare_sum,4), profit=round(unidRare_sum-unid_prices['Rare'][0]-unidRare_salvageCost,4), salvageCost=unidRare_salvageCost))

print('\nResult function test')
compute_result(unidFine_droprate,multiplier_prices,unidFine_salvageCost,'Fine')


print("The end")
