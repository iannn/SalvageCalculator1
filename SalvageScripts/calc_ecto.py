"""Ectoplasm Salvaging Math

Ectoplasm can be used or salvaged into Crystalline Dust
Dust can be used for upgrading materials
Ecto salvaging can also be done for profit

"""

"""Permutations to calculate

Have ecto - use dust
Have ecto - sell dust
Buy ecto - use dust
Buy ecto - sell dust

ASSUME 1.85 Crystalline dust per ecto with Master/Mystic/Silver-fed

Cost per salvage of Mystic kit is 10.5c if mystic stones are free
Silver-fed is 60c per salvage
https://wiki.guildwars2.com/wiki/Silver-Fed_Salvage-o-Matic

"""

"""Ecto IDs

    19721=Ectoplasm
    24277=Pile of Crystalline Dust

"""

#It's simple enough where all 4 can be calculated at once as a single pass

#Import GW2 API
from gw2api import GuildWars2Client
gw2_client = GuildWars2Client()

salvageCost = 10.5

apivalues=gw2_client.commerceprices.get(ids=[19721,24277])#this is very dangerous because if I change the order, this messes up. Should switch to some kind if for x in apivalues: if ... else if ...

ecto_price={}
dust_price={}
#For loop

for entryAPI in apivalues:
    if(entryAPI['id']==19721):
        ecto_price['buy']=entryAPI['buys']['unit_price']
        ecto_price['sell']=entryAPI['sells']['unit_price']
    elif(entryAPI['id']==24277):
        dust_price['buy']=entryAPI['buys']['unit_price']
        dust_price['sell']=entryAPI['sells']['unit_price']
    else:
        print("Unexpected API return")
        print(entryAPI)

#ecto salvages into 1.85 dust/ecto
dust_salvage={}
dust_salvage['buy']=round((ecto_price['buy']+salvageCost)/1.85,4)
dust_salvage['sell']=round((ecto_price['sell']+salvageCost)/1.85,4)

#reference information
print('Reference numbers:\nEcto - buy={ebuy}; sell={esell}\nDust - buy={dbuy}; sell={dsell}\nSalvaged dust at 1.85 dust/ecto - buy={sbuy}; sell={ssell}'.format(ebuy=ecto_price['buy'],esell=ecto_price['sell'],dbuy=dust_price['buy'],dsell=dust_price['sell'],sbuy=dust_salvage['buy'],ssell=dust_salvage['sell']))

#begin cases
#Have ecto - use dust
print('\nHave ectos - use dust')
print('Instead of selling ectos and buying dust, ecto is salvaged for 1.85 dust at {sCost} per salvage.\nSavings compared to buying is {diff}'.format(diff=dust_price['buy']*1.85 - ecto_price['sell']*0.85 - salvageCost, sCost=salvageCost))

#Buy ecto - use dust
print('\nBuy ecto - use dust')
print('Instead of buying dust, buy and salvage ecto for 1.85 dust at {sCost} per salvage.\nSavings compared to buying is {diff}'.format(sCost=salvageCost, diff=dust_price['buy']*1.85 - ecto_price['buy'] - salvageCost))

#Have ecto - sell dust
print('\nHave ecto - sell dust')
print('Instead of selling ecto, salvage ecto for 1.85 dust at {sCost} per salvage and sell dust.\nProfit compared to selling ecto is {diff}'.format(sCost=salvageCost, diff=dust_price['sell']*1.85*.85 - ecto_price['sell']*.85 - salvageCost))

#Buy ecto - sell dust
print('\nBuy ecto - sell dust')
print('Salvage ecto at {sCost} per salvage for 1.85 dust and sell dust.\nSell for profit of {profit}'.format(sCost=salvageCost, profit=dust_price['sell']*1.85*0.85 - ecto_price['buy'] - salvageCost))
