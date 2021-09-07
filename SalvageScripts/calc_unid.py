#This is a basic scrip for calculating the value of unidentified gear TO Sell
#SAVINGS not currently calculated
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

def sort_allAPI(allAPI):
    #Fill with api values
    unid_prices= {}
    unrefined_prices = {}
    refined_prices = {}
    other_prices = {}

    testcount = 0
    #assemble the dictionaries
    for entryAPI in allAPI:
        testcount= testcount + 1
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

def generate_multiplier(unrefined_prices,refined_prices,other_prices):
    #Compare and finalize values of material
    decision = {}
    multiplier_prices = {}

    #TP cut to be added in later
    if(unrefined_prices['Orichalcum Ore'][1] > refined_prices['Orichalcum Ingot'][1]/2):
        decision['Orichalcum Ore'] = 'raw'
        multiplier_prices['Orichalcum Ore']=unrefined_prices['Orichalcum Ore'][1]
    else:
        decision['Orichalcum Ore'] = 'refined'
        multiplier_prices['Orichalcum Ore']=refined_prices['Orichalcum Ingot'][1]/2

    if(unrefined_prices['Ancient Wood Log'][1] > refined_prices['Ancient Wood Plank'][1]/3):
        decision['Ancient Wood Log'] = 'raw'
        multiplier_prices['Ancient Wood Log']=unrefined_prices['Ancient Wood Log'][1]
    else:
        decision['Ancient Wood Log'] = 'refined'
        multiplier_prices['Ancient Wood Log']=refined_prices['Ancient Wood Plank'][1]/3

    if(unrefined_prices['Gossamer Scrap'][1] > refined_prices['Bolt of Gossamer'][1]/2):
        decision['Gossamer Scrap'] = 'raw'
        multiplier_prices['Gossamer Scrap']=unrefined_prices['Gossamer Scrap'][1]
    else:
        decision['Gossamer Scrap'] = 'refined'
        multiplier_prices['Gossamer Scrap']=refined_prices['Bolt of Gossamer'][1]/2

    if(unrefined_prices['Hardened Leather Section'][1] > refined_prices['Cured Hardened Leather Square'][1]/3):
        decision['Hardened Leather Section'] = 'raw'
        multiplier_prices['Hardened Leather Section']=unrefined_prices['Hardened Leather Section'][1]
    else:
        decision['Hardened Leather Section'] = 'refined'
        multiplier_prices['Hardened Leather Section']=refined_prices['Cured Hardened Leather Square'][1]/3

    if(unrefined_prices['Mithril Ore'][1] > refined_prices['Mithril Ingot'][1]/2):
        decision['Mithril Ore'] = 'raw'
        multiplier_prices['Mithril Ore']=unrefined_prices['Mithril Ore'][1]
    else:
        decision['Mithril Ore'] = 'refined'
        multiplier_prices['Mithril Ore']=refined_prices['Mithril Ingot'][1]/2

    if(unrefined_prices['Elder Wood Log'][1] > refined_prices['Elder Wood Plank'][1]/3):
        decision['Elder Wood Log'] = 'raw'
        multiplier_prices['Elder Wood Log']=unrefined_prices['Elder Wood Log'][1]
    else:
        decision['Elder Wood Log'] = 'refined'
        multiplier_prices['Elder Wood Log']=refined_prices['Elder Wood Plank'][1]/3

    if(unrefined_prices['Silk Scrap'][1] > refined_prices['Bolt of Silk'][1]/3):
        decision['Silk Scrap'] = 'raw'
        multiplier_prices['Silk Scrap']=unrefined_prices['Silk Scrap'][1]
    else:
        decision['Silk Scrap'] = 'refined'
        multiplier_prices['Silk Scrap']=refined_prices['Bolt of Silk'][1]/3

    if(unrefined_prices['Thick Leather Square'][1] > refined_prices['Cured Thick Leather Square'][1]/4):
        decision['Thick Leather Square'] = 'raw'
        multiplier_prices['Thick Leather Square']=unrefined_prices['Thick Leather Square'][1]
    else:
        decision['Thick Leather Square'] = 'refined'
        multiplier_prices['Thick Leather Square']=refined_prices['Cured Thick Leather Square'][1]/4

    if(unrefined_prices['Lucent Mote'][1] > refined_prices['Pile of Lucent Crystal'][1]/10):
        decision['Lucent Mote'] = 'raw'
        multiplier_prices['Lucent Mote']=unrefined_prices['Lucent Mote'][1]
    else:
        decision['Lucent Mote'] = 'refined'
        multiplier_prices['Lucent Mote']=refined_prices['Pile of Lucent Crystal'][1]/10
    #refine vs raw done. Include the other stuff now to finish multiplier_prices dict
    for key in other_prices:
        multiplier_prices[key] = other_prices[key][1]
    return multiplier_prices,decision


from gw2api import GuildWars2Client
gw2_client = GuildWars2Client()

#charm and symbol values I have are low data so using wiki values
unidFine_droprate = {'Orichalcum Ore':0.0397,'Ancient Wood Log':0.0311,'Gossamer Scrap':0.0148,'Hardened Leather Section':0.0173,'Mithril Ore':0.4310,'Elder Wood Log':0.3877,'Silk Scrap':0.3069,'Thick Leather Square':0.2473,'Ectoplasm':0.0068,'Lucent Mote':0.1018,'Symbol of Control':0.0004,'Symbol of Enhancement':0.0004,'Symbol of Pain':0.0004,'Charm of Brilliance':0.0003,'Charm of Potence':0.0003,'Charm of Skill':0.0003}

#My data 19500
unidMasterwork_droprate = {'Orichalcum Ore':0.0395,'Ancient Wood Log':0.0274,'Gossamer Scrap':0.0183,'Hardened Leather Section':0.0176,'Mithril Ore':0.4430,'Elder Wood Log':0.3658,'Silk Scrap':0.3476,'Thick Leather Square':0.2813,'Ectoplasm':0.0294,'Lucent Mote':1.0711,'Symbol of Control':0.0013,'Symbol of Enhancement':0.0047,'Symbol of Pain':0.0037,'Charm of Brilliance':0.0046,'Charm of Potence':0.0026,'Charm of Skill':0.0031}

#pure wiki
unidRare_droprate = {'Orichalcum Ore':0.0407,'Ancient Wood Log':0.0295,'Gossamer Scrap':0.0165,'Hardened Leather Section':0.0153,'Mithril Ore':0.4611,'Elder Wood Log':0.3837,'Silk Scrap':0.3239,'Thick Leather Square':0.2556,'Ectoplasm':0.8751,'Lucent Mote':1.3881,'Symbol of Control':0.0035,'Symbol of Enhancement':0.0065,'Symbol of Pain':0.0029,'Charm of Brilliance':0.0056,'Charm of Potence':0.0033,'Charm of Skill':0.0034}
#,'Luck':-1 is out because I don't have value for this yet

#Never salvage with just one kit becuase better gear will come out
#Exotics are so rare that they will generate far more than the salvage + I may use BLKit
salvageCost = {'Mystic':10.5, 'Copper':5 , 'Runecrafter':30, 'Silver':60}
unidFine_salvageCost = salvageCost['Mystic']*0.0127 + salvageCost['Runecrafter']*0.0887 + salvageCost['Copper']*0.8974
unidMasterwork_salvageCost = salvageCost['Mystic']*0.0351 + salvageCost['Runecrafter']*0.9623
unidRare_salvageCost = salvageCost['Silver']*1


#Fill with api values
unid_prices= {}
unrefined_prices = {}
refined_prices = {}
other_prices = {}


#Compare and finalize values of material
decision = {}
multiplier_prices = {}

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

"""
print('Prices')
print('unrefined: ',unrefined_prices)
print('refined: ',refined_prices)
print('other: ',other_prices)
print('unid: ',unid_prices)
"""

#Go through materials to see which are more profitable to be refined
#check math though because placing a raw material 1c higher may blow the refined material out of the water cause current unrefined may just have a few listings left
#value per RAW MATERIAL goes into the multiplier dict, decision of raw/refined goes into decision dict

#Right now, only care about buy low and sell high
#There is an issue where if the refined item is not 1c/raw higher than the raw item, it's better to just increase the raw item by 1 if it's not too high/will hit a massive wall

multiplier_prices,decision = generate_multiplier(unrefined_prices,refined_prices,other_prices)
"""
#DECIDE WHEN TO ADD IN TP CUT
if(unrefined_prices['Orichalcum Ore'][1] > refined_prices['Orichalcum Ingot'][1]/2):
    decision['Orichalcum Ore'] = 'raw'
    multiplier_prices['Orichalcum Ore']=unrefined_prices['Orichalcum Ore'][1]
else:
    decision['Orichalcum Ore'] = 'refined'
    multiplier_prices['Orichalcum Ore']=refined_prices['Orichalcum Ingot'][1]/2

if(unrefined_prices['Ancient Wood Log'][1] > refined_prices['Ancient Wood Plank'][1]/3):
    decision['Ancient Wood Log'] = 'raw'
    multiplier_prices['Ancient Wood Log']=unrefined_prices['Ancient Wood Log'][1]
else:
    decision['Ancient Wood Log'] = 'refined'
    multiplier_prices['Ancient Wood Log']=refined_prices['Ancient Wood Plank'][1]/3

if(unrefined_prices['Gossamer Scrap'][1] > refined_prices['Bolt of Gossamer'][1]/2):
    decision['Gossamer Scrap'] = 'raw'
    multiplier_prices['Gossamer Scrap']=unrefined_prices['Gossamer Scrap'][1]
else:
    decision['Gossamer Scrap'] = 'refined'
    multiplier_prices['Gossamer Scrap']=refined_prices['Bolt of Gossamer'][1]/2

if(unrefined_prices['Hardened Leather Section'][1] > refined_prices['Cured Hardened Leather Square'][1]/3):
    decision['Hardened Leather Section'] = 'raw'
    multiplier_prices['Hardened Leather Section']=unrefined_prices['Hardened Leather Section'][1]
else:
    decision['Hardened Leather Section'] = 'refined'
    multiplier_prices['Hardened Leather Section']=refined_prices['Cured Hardened Leather Square'][1]/3

if(unrefined_prices['Mithril Ore'][1] > refined_prices['Mithril Ingot'][1]/2):
    decision['Mithril Ore'] = 'raw'
    multiplier_prices['Mithril Ore']=unrefined_prices['Mithril Ore'][1]
else:
    decision['Mithril Ore'] = 'refined'
    multiplier_prices['Mithril Ore']=refined_prices['Mithril Ingot'][1]/2

if(unrefined_prices['Elder Wood Log'][1] > refined_prices['Elder Wood Plank'][1]/3):
    decision['Elder Wood Log'] = 'raw'
    multiplier_prices['Elder Wood Log']=unrefined_prices['Elder Wood Log'][1]
else:
    decision['Elder Wood Log'] = 'refined'
    multiplier_prices['Elder Wood Log']=refined_prices['Elder Wood Plank'][1]/3

if(unrefined_prices['Silk Scrap'][1] > refined_prices['Bolt of Silk'][1]/3):
    decision['Silk Scrap'] = 'raw'
    multiplier_prices['Silk Scrap']=unrefined_prices['Silk Scrap'][1]
else:
    decision['Silk Scrap'] = 'refined'
    multiplier_prices['Silk Scrap']=refined_prices['Bolt of Silk'][1]/3

if(unrefined_prices['Thick Leather Square'][1] > refined_prices['Cured Thick Leather Square'][1]/4):
    decision['Thick Leather Square'] = 'raw'
    multiplier_prices['Thick Leather Square']=unrefined_prices['Thick Leather Square'][1]
else:
    decision['Thick Leather Square'] = 'refined'
    multiplier_prices['Thick Leather Square']=refined_prices['Cured Thick Leather Square'][1]/4

if(unrefined_prices['Lucent Mote'][1] > refined_prices['Pile of Lucent Crystal'][1]/10):
    decision['Lucent Mote'] = 'raw'
    multiplier_prices['Lucent Mote']=unrefined_prices['Lucent Mote'][1]
else:
    decision['Lucent Mote'] = 'refined'
    multiplier_prices['Lucent Mote']=refined_prices['Pile of Lucent Crystal'][1]/10

#refine vs raw done. Include the other stuff now to finish
for key in other_prices:
    multiplier_prices[key] = other_prices[key][1]

"""
print("Decision prices:")#, decision)
for key,value in decision.items():
    print(key,':',value)

print("\nMultiplier_prices:")#, multiplier_prices)
for key, value in multiplier_prices.items():
    print(key,':',value)

#Calculation phase
#salvage value = drop rate * multiplier_prices
#Now I add in TP cut. Adding to salvage value is fine because the TP prices are on

#Fine
for key in unidFine_droprate:
    unidFine_salvageValue[key] = 0.85*unidFine_droprate[key]*multiplier_prices[key]
    unidFine_sum = unidFine_sum + unidFine_salvageValue[key]

#Masterwork
for key in unidMasterwork_droprate:
    unidMasterwork_salvageValue[key] = 0.85*unidMasterwork_droprate[key]*multiplier_prices[key]
    unidMasterwork_sum = unidMasterwork_sum + unidMasterwork_salvageValue[key]

#Rare
for key in unidRare_droprate:
    unidRare_salvageValue[key] = 0.85*unidRare_droprate[key]*multiplier_prices[key]
    unidRare_sum = unidRare_sum + unidRare_salvageValue[key]


#Report time
print()
print('Fine unid gear costs {cost} to buy order, has an average value of {salvageCost} to salvage, and will salvage into a total value of {salvageValue} resulting in {profit} profit per salvage'.format(cost=unid_prices['Fine'][0], salvageValue=unidFine_sum, profit=unidFine_sum-unid_prices['Fine'][0]-unidFine_salvageCost, salvageCost=unidFine_salvageCost))
print('Masterwork unid gear costs {cost} to buy order, has an average value of {salvageCost} to salvage, and will salvage into a total value of {salvageValue} resulting in {profit} profit per salvage'.format(cost=unid_prices['Masterwork'][0], salvageValue=unidMasterwork_sum, profit=unidMasterwork_sum-unid_prices['Masterwork'][0]-unidMasterwork_salvageCost, salvageCost=unidMasterwork_salvageCost))
print('Rare unid gear costs {cost} to buy order, has an average value of {salvageCost} to salvage, and will salvage into a total value of {salvageValue} resulting in {profit} profit per salvage'.format(cost=unid_prices['Rare'][0], salvageValue=unidRare_sum, profit=unidRare_sum-unid_prices['Rare'][0]-unidRare_salvageCost, salvageCost=unidRare_salvageCost))

print("The end")
