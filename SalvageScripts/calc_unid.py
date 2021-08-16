#This is a basic scrip for calculating the value of unidentified gear
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

Call function to get get TP values
Call function to get list of materials to refine for better profit
Decide which unidentified gear to process
Call function to calculate selected unidentified gear with best profit materials
Call function to generate report

"""

"""API items and numbers

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
    19722=Elder Wood Plank
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
