#Helper function file for GW2 salvaging for profit scripts
#Common functions only

def generate_multiplier(unrefined_dct,refined_dct,refined_scaler,refined_lookup,buysell):
    """Input:
        unrefined material prices dictionary
        refined material prices dictionary
        the scaler values to get value of raw material from refined
        lookup dictionary to get refined from unrefined
        buysell value. It is the array position 0=buy 1=sell"""

    """Output:
        multiplier for the best value/raw material
        the decision to refine or not"""

    #value per RAW MATERIAL goes into the multiplier dict, decision of raw/refined goes into decision dict
    #Compare and finalize values of material
    decision_dct = {}
    multiplier_dct = {}

    for material_key in unrefined_dct:
        if material_key in refined_scaler:
            if material_key == 'Copper Ore':
            elif unrefined_dct[material_key][buysell] >= refined_dct[refined_lookup[material_key]][buysell]/refined_scaler[material_key]:
                decision_dct[material_key] = 'raw'
                multiplier_dct[material_key] = round(unrefined_dct[material_key][buysell],4)
            else:
                decision_dct[material_key] = 'refined'
                multiplier_dct[material_key] = round(refined_dct[refined_lookup[material_key]][buysell]/refined_scaler[material_key],4)
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
