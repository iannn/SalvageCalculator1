#Helper function file for GW2 salvaging for profit scripts
#Common functions only

def generate_multiplier(unrefined_dct,refined_dct,refined_scalar,refined_lookup,buysell):
    """Input:
        unrefined material prices dictionary
        refined material prices dictionary
        the scalar values to get value of raw material from refined
        lookup dictionary to get refined from unrefined
        buysell value. It is the array position 0=buy 1=sell"""

    """Output:
        multiplier for the best value/raw material
        the decision to refine or not"""

    """Application note:
            raw values only can be forced if "refined_scalar" is an empty dict
            dictionaries passed are passed by reference so altering refined_lookup with the Tin/Coal/Primordium variants can be done inside here fine"""""

    #value per RAW MATERIAL goes into the multiplier dict, decision of raw/refined goes into decision dict
    #Compare and finalize values of material
    decision_dct = {}
    multiplier_dct = {}

    for material_key in unrefined_dct:
        if material_key in refined_lookup:
            if material_key == 'Copper Ore':
                #copper ore is largest price
                #5 bronze per lump of tin. Tin bought 10 for 80c
                if (unrefined_dct['Copper Ore'][buysell] >= refined_dct['Copper Ingot'][buysell])/refined_scalar['Copper Ingot'] and (unrefined_dct['Copper Ore'][buysell] >= (refined_dct['Bronze Ingot'][buysell]-8/5)/refined_scalar['Bronze Ingot']):
                    decision_dct['Copper Ore'] = 'raw'
                    multiplier_dct['Copper Ore'] = round(unrefined_dct['Copper Ore'][buysell],4)
                #Bronze > Copper Ingot
                elif (refined_dct['Bronze Ingot'][buysell]-8/5)/refined_scalar['Bronze Ingot'] > refined_dct['Copper Ingot'][buysell]/refined_scalar['Copper Ingot']:
                    decision_dct['Copper Ore'] = 'B Ingot'
                    multiplier_dct['Copper Ore'] = round(refined_dct['Bronze Ingot'][buysell],4)
                    unrefined_to_refined['Copper Ore']='Bronze Ingot'#Passed by reference so update persists
                #Regular copper ingot is therefore the best option
                else:
                    decision_dct['Copper Ore'] = 'C Ingot'
                    multiplier_dct['Copper Ore'] = round(refined_dct['Copper Ingot'][buysell],4)
            elif material_key == 'Iron Ore':
                #Iron ore is largest price
                #1 lump of coal per Steel Ingot. Coal bought 10 for 160c
                if (unrefined_dct['Iron Ore'][buysell] >= refined_dct['Iron Ingot'][buysell])/refined_scalar['Iron Ingot'] and (unrefined_dct['Iron Ore'][buysell] >= (refined_dct['Steel Ingot'][buysell]-16)/refined_scalar['Steel Ingot']):
                    decision_dct['Iron Ore'] = 'raw'
                    multiplier_dct['Iron Ore'] = round(unrefined_dct['Iron Ore'][buysell],4)
                #Steel > Iron Ingot
                elif (refined_dct['Steel Ingot'][buysell]-16)/refined_scalar['Steel Ingot'] > refined_dct['Iron Ingot'][buysell]/refined_scalar['Iron Ingot']:
                    decision_dct['Iron Ore'] = 'S Ingot'
                    multiplier_dct['Iron Ore'] = round(refined_dct['Steel Ingot'][buysell],4)
                    unrefined_to_refined['Iron Ore']='Bronze Ingot'#Passed by reference so update persists
                #Regular Iron Ingot is therefore the best option
                else:
                    decision_dct['Iron Ore'] = 'I Ingot'
                    multiplier_dct['Iron Ore'] = round(refined_dct['Iron Ingot'][buysell],4)
            elif material_key == 'Platinum Ore':
                #Platinum ore is largest price
                #1 lump of Primordium per Darksteel Ingot. Primordium bought 10 for 480c
                if (unrefined_dct['Platinum Ore'][buysell] >= refined_dct['Platinum Ingot'][buysell])/refined_scalar['Platinum Ingot'] and (unrefined_dct['Platinum Ore'][buysell] >= (refined_dct['Darksteel Ingot'][buysell]-48)/refined_scalar['Darksteel Ingot']):
                    decision_dct['Platinum Ore'] = 'raw'
                    multiplier_dct['Platinum Ore'] = round(unrefined_dct['Platinum Ore'][buysell],4)
                #Darksteel > Platinum Ingot
                elif (refined_dct['Darksteel Ingot'][buysell]-48)/refined_scalar['Darksteel Ingot'] > refined_dct['Platinum Ingot'][buysell]/refined_scalar['Platinum Ingot']:
                    decision_dct['Platinum Ore'] = 'D Ingot'
                    multiplier_dct['Platinum Ore'] = round(refined_dct['Darksteel Ingot'][buysell],4)
                    unrefined_to_refined['Platinum Ore']='Darksteel Ingot'#Passed by reference so update persists
                #Regular Platinum Ingot is therefore the best option
                else:
                    decision_dct['Platinum Ore'] = 'P Ingot'
                    multiplier_dct['Platinum Ore'] = round(refined_dct['Platinum Ingot'][buysell],4)
            elif unrefined_dct[material_key][buysell] >= refined_dct[refined_lookup[material_key]][buysell]/refined_scalar[refined_lookup[material_key]]:
                decision_dct[material_key] = 'raw'
                multiplier_dct[material_key] = round(unrefined_dct[material_key][buysell],4)
            else:
                decision_dct[material_key] = 'refined'
                multiplier_dct[material_key] = round(refined_dct[refined_lookup[material_key]][buysell]/refined_scalar[refined_lookup[material_key]],4)
        else:#This assumes that this was part of the "other materials" dict ie charm, symbol, ecto
            decision_dct[material_key]='none'
            multiplier_dct[material_key]=unrefined_dct[material_key][buysell]

    return multiplier_dct,decision_dct
#end of generate_multiplier


def compute_result(droprate_dict,multiplier_dict,TPCut):
    salvageValue_dct = {}
    sum_val = 0
    if TPCut == True:
        TPValue = 0.85
    else:
        TPValue = 1

    for key in droprate_dict:
        salvageValue_dct[key] = round(TPValue*droprate_dict[key]*multiplier_dict[key],4)
        sum_val = sum_val + salvageValue_dct[key]

    return salvageValue_dct,sum_val
#End of compute_result
