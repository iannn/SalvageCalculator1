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
    salvageWood = {}
    salvageMetal = {}
    salvageCloth = {}
    unrefined_prices = {}
    refined_prices = {}

    for entryAPI in allAPI:
        if(entryAPI['id']==79423):
            salvageWood['Reclaimed Wood Chunk'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==79079):
            salvageMetal['Unstable Metal Chunk'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==79138):
            salvageCloth['Unstable Rag'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==21671):
            salvageCloth['Worn Garment'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==21660):
            salvageCloth['Worn Rag'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==80681):
            salvageLeather['Bloodstone-Warped Hide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==79213):
            salvageLeather['Unstable Hide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==80681):
            salvageLeather['Bloodstone-Warped Hide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==21689):
            salvageLeather['Hard Leather Strap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==21668):
            salvageLeather['Frayed Hide'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
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
        elif(entryAPI['id']==19697):
            unrefined_prices['Copper Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19703):
            unrefined_prices['Silver Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19699):
            unrefined_prices['Iron Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19698):
            unrefined_prices['Gold Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19702):
            unrefined_prices['Platinum Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19700):
            unrefined_prices['Mithril Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19701):
            unrefined_prices['Orichalcum Ore'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19718):
            unrefined_prices['Jute Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19739):
            unrefined_prices['Wool Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19741):
            unrefined_prices['Cotton Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19743):
            unrefined_prices['Linen Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19748):
            unrefined_prices['Silk Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19745):
            unrefined_prices['Gossamer Scrap'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19723):
            unrefined_prices['Green Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19726):
            unrefined_prices['Soft Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19727):
            unrefined_prices['Seasoned Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19724):
            unrefined_prices['Hard Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19722):
            unrefined_prices['Elder Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19725):
            unrefined_prices['Ancient Wood Log'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
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
        elif(entryAPI['id']==19680):
            refined_prices['Copper Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19679):
            refined_prices['Bronze Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19687):
            refined_prices['Silver Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19683):
            refined_prices['Iron Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19688):
            refined_prices['Steel Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19682):
            refined_prices['Gold Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19686):
            refined_prices['Platinum Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19681):
            refined_prices['Darksteel Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19684):
            refined_prices['Mithril Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19685):
            refined_prices['Orichalcum Ingot'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19720):
            refined_prices['Bolt of Jute'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19740):
            refined_prices['Bolt of Wool'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19742):
            refined_prices['Bolt of Cotton'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19744):
            refined_prices['Bolt of Linen'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19747):
            refined_prices['Bolt of Silk'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19746):
            refined_prices['Bolt of Gossamer'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19710):
            refined_prices['Green Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19713):
            refined_prices['Soft Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19714):
            refined_prices['Seasoned Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19711):
            refined_prices['Hard Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19709):
            refined_prices['Elder Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        elif(entryAPI['id']==19712):
            refined_prices['Ancient Wood Plank'] = [entryAPI['buys']['unit_price'], entryAPI['sells']['unit_price']]
        else:
            print("Unexpected API return")
            print(entryAPI)

    return unrefined_prices, refined_prices, salvageLeather, salvageWood, salvageMetal, salvageCloth

#General compute and print report
def salvagePrint(itemName_str,itemCost_dct,multiplier_dct,droprate_dict,salvageCost_dct,buysell):
    """This is the goal

    Hard Leather Strap  : {cost}
    Salvage Kit             Profit  | Total Value   | item 1    item 2
    --------------------------------------------------------------------------------------
    Copper              : {profit}  | {sum right}   |
    Runecrafters        : {profit}  | {sum right}   |
    Rare                : {profit}  | {sum right}   |

    return value is some kind of profit metric [salvage item, salvage method, profit]
    [0-10) is meh
    [10-25) is good
    25 and above is BUYBUYBUY

    print('{:<24} : {:>10}   {:<10}   {:<5}   {:>10}   {:>10}   {:>10}   {:>10}'.format('Material','Sell Price','State','Raw','Refined','Fine','Masterwork','Rare'))
    """
    worthit_list = []

    #These really short columns are throwing me off so try and make them custom length
    formatline = "{:<14} : {:>10} | {:>12} | " + '  '.join(["{:>24}"]*len(droprate_dict['Copper'].keys()))
    orderedkeys = list(droprate_dict['Copper'].keys())
    print(formatline.format(*["Salvage Kit", "Profit","Total Value"]+orderedkeys))
    for salvage_rarity,droprate_x in droprate_dict.items():
        itemValues_dct,itemSum_dct = compute_result(droprate_x,multiplier_dct,True)
        methodprofit=round(itemSum_dct - salvageCost_dct[salvage_rarity]-itemCost_dct[itemName_str][buysell],4)
        print(formatline.format(*[salvage_rarity,round(methodprofit,4),round(itemSum_dct,4)]+[itemValues_dct[x] for x in orderedkeys]))

    print("\n{salvageName} : {salvagePrice}".format(salvageName=itemName_str, salvagePrice=itemCost_dct[itemName_str][buysell]))
    for salvage_rarity,droprate_x in droprate_dict.items():
        itemValues_dct,itemSum_dct = compute_result(droprate_x,multiplier_dct,True)
        methodprofit=round(itemSum_dct - salvageCost_dct[salvage_rarity]-itemCost_dct[itemName_str][buysell],4)
        print("{salvageName} {salvageMethod:<11} : Average Salvage Value = {salvageValue}; Estimated {profit} profit per salvage".format(salvageName=itemName_str,salvageMethod=salvage_rarity,salvageValue=itemSum_dct,profit=methodprofit))

    return worthit_list
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
droprate_BitofMetalScrap = {}

#Unstable Metal Chunk
droprate_UnstableMetalChunk = {}
#Peu
droprate_UnstableMetalChunk['Copper']={'Copper Ore':0.1613691932,'Iron Ore':0.9160554197,'Platinum Ore':0.4686226569,'Mithril Ore':0.1597392013,'Orichalcum Ore':0.3276283619}
droprate_UnstableMetalChunk['Runecrafter']={'Copper Ore':0.184,'Iron Ore':0.911,'Platinum Ore':0.502,'Mithril Ore':0.186,'Orichalcum Ore':0.328}
droprate_UnstableMetalChunk['Rare']={'Copper Ore':0.136,'Iron Ore':1.004,'Platinum Ore':0.523,'Mithril Ore':0.151,'Orichalcum Ore':0.31}


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
droprate_BloodstoneWarpedHide['Rare'] = {'Rawhide Leather Section':0.0557,'Thin Leather Section':0.0581,'Coarse Leather Section':0.0521,'Rugged Leather Section':0.0508,'Thick Leather Section':0.4758,'Hardened Leather Section':0.5541}

#Hard Leather Strap
droprate_HardLeatherStrap={}
#Mine
droprate_HardLeatherStrap['Copper'] = {'Thick Leather Section':1.2865,'Hardened Leather Section':0.0770}
droprate_HardLeatherStrap['Runecrafter'] = {'Thick Leather Section':1.352,'Hardened Leather Section':0.092}
droprate_HardLeatherStrap['Rare'] = {'Thick Leather Section':1.1973,'Hardened Leather Section':0.1067}

#Frayed Hide
droprate_FrayedHide={}
#Peu
droprate_FrayedHide['Copper']={'Coarse Leather Section':0.57,'Rugged Leather Section':1.16}
droprate_FrayedHide['Runecrafter']={'Coarse Leather Section':0.32,'Rugged Leather Section':1.53}
droprate_FrayedHide['Rare']={'Coarse Leather Section':0.43,'Rugged Leather Section':1.38}

"""
Drop rates: Cloth
"""
#Unstable Cloth
droprate_UnstableRag = {}
#Peu
droprate_UnstableRag['Copper']={'Jute Scrap':0.1516626115,'Wool Scrap':0.5587996756,'Cotton Scrap':0.5052716951,'Linen Scrap':0.502027575,'Silk Scrap':0.1549067315,'Gossamer Scrap':0.1662611517}
droprate_UnstableRag['Runecrafter']={'Jute Scrap':0.164,'Wool Scrap':0.527,'Cotton Scrap':0.491,'Linen Scrap':0.568,'Silk Scrap':0.22,'Gossamer Scrap':0.2513}
droprate_UnstableRag['Rare']={'Jute Scrap':0.158,'Wool Scrap':0.471,'Cotton Scrap':0.585,'Linen Scrap':0.544,'Silk Scrap':0.21,'Gossamer Scrap':0.165}

#Worn Garment
droprate_WornGarment = {}
#Peu
droprate_WornGarment['Copper']={'Jute Scrap':0.57,'Wool Scrap':1.24}
droprate_WornGarment['Runecrafter']={'Jute Scrap':0.41,'Wool Scrap':1.44}
droprate_WornGarment['Rare']={'Jute Scrap':0.29,'Wool Scrap':1.54}

#Worn Rag
droprate_WornRag = {}
#Peu
droprate_WornRag['Copper']={'Jute Scrap':0.56,'Wool Scrap':1.35}
droprate_WornRag['Runecrafter']={'Jute Scrap':0.29,'Wool Scrap':1.58}
droprate_WornRag['Rare']={'Jute Scrap':0.29,'Wool Scrap':1.67}

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
allIDs =    [79423,#Wood salvage
            79079,#Metal salvage
            79138,21671,21660,#Cloth salvage
            79213,80681,21689,21668,#Leather salvage
            19723,19726,19727,19724,19722,19725,#raw wood
            19710,19713,19714,19711,19709,19712,#refined wood
            19697,19703,19699,19698,19702,19700,19701,#raw metal
            19680,19679,19687,19683,19688,19682,19686,19681,19684,19685,#refined metal
            19718,19739,19741,19743,19748,19745,#raw cloth
            19720,19740,19742,19744,19747,19746,#refined cloth
            19719,19728,19730,19731,19729,19732,#raw leather
            19738,19733,19734,19736,19735,19737]#refined leather

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
print('\n','-'*10,"Leather",'-'*10)
salvagePrint('Unstable Hide',salvageLeather,multiplier_prices,droprate_UnstableHide,salvageCost,0)
salvagePrint('Bloodstone-Warped Hide',salvageLeather,multiplier_prices,droprate_BloodstoneWarpedHide,salvageCost,0)
salvagePrint('Hard Leather Strap',salvageLeather,multiplier_prices,droprate_HardLeatherStrap,salvageCost,0)
salvagePrint('Frayed Hide',salvageLeather,multiplier_prices,droprate_FrayedHide,salvageCost,0)

print('\n','-'*10,"Leather / / / Metal",'-'*10)

salvagePrint('Unstable Metal Chunk',salvageMetal,multiplier_prices,droprate_UnstableMetalChunk,salvageCost,0)

print('\n','-'*10,"Metal / / / Cloth",'-'*10)

salvagePrint('Unstable Rag',salvageCloth,multiplier_prices,droprate_UnstableRag,salvageCost,0)
salvagePrint('Worn Garment',salvageCloth,multiplier_prices,droprate_WornGarment,salvageCost,0)
salvagePrint('Worn Rag',salvageCloth,multiplier_prices,droprate_WornRag,salvageCost,0)

print('\n','-'*10,"Cloth / / / Wood",'-'*10)

salvagePrint('Reclaimed Wood Chunk',salvageWood,multiplier_prices,droprate_ReclaimedWoodChunk,salvageCost,0)
