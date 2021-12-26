import pytest

""" last result sys hack
import sys
sys.path.append("../SalvageScripts")
"""

#I see a lot of fighting on what to do with proper importing and packaging of projects
import calc_helpers

@pytest.fixture
def refined_scalar():
    #Taken directly from calc_salvage. This DOES have Lucent Crystal though so maybe I should merge these into calc_helpers for completeness and consistency
    refined_scalar = {'Stretched Rawhide Leather Square':2,'Cured Thin Leather Square':2,'Cured Coarse Leather Square':2,'Cured Rugged Leather Square':2,'Cured Thick Leather Square':4,'Cured Hardened Leather Square':3,
                    'Copper Ingot':2,'Bronze Ingot':2,'Silver Ingot':2,'Iron Ingot':3,'Steel Ingot':3,'Gold Ingot':2,'Platinum Ingot':2,'Darksteel Ingot':2,'Mithril Ingot':2,'Orichalcum Ingot':2,
                    'Bolt of Jute':2,'Bolt of Wool':2,'Bolt of Cotton':2,'Bolt of Linen':2,'Bolt of Silk':3,'Bolt of Gossamer':2,
                    'Green Wood Plank':3,'Soft Wood Plank':2,'Seasoned Wood Plank':3,'Hard Wood Plank':3,'Elder Wood Plank':3,'Ancient Wood Plank':3,
                    'Pile of Lucent Crystal':10}
    return refined_scalar

@pytest.fixture
def refined_lookup():
    #taken directly from calc_salvage. No lucent mote though
    unrefined_to_refined = {'Hardened Leather Section':'Cured Hardened Leather Square','Thick Leather Section':'Cured Thick Leather Square','Rugged Leather Section':'Cured Rugged Leather Square','Coarse Leather Section':'Cured Coarse Leather Square','Thin Leather Section':'Cured Thin Leather Square','Rawhide Leather Section':'Stretched Rawhide Leather Square',
                            'Copper Ore':'Copper Ingot','Silver Ore':'Silver Ingot','Iron Ore':'Iron Ingot','Gold Ore':'Gold Ingot','Platinum Ore':'Platinum Ingot','Mithril Ore':'Mithril Ingot','Orichalcum Ore':'Orichalcum Ingot',
                            'Jute Scrap':'Bolt of Jute','Wool Scrap':'Bolt of Wool','Cotton Scrap':'Bolt of Cotton','Linen Scrap':'Bolt of Linen','Silk Scrap':'Bolt of Silk','Gossamer Scrap':'Bolt of Gossamer',
                            'Green Wood Log':'Green Wood Plank','Soft Wood Log':'Soft Wood Plank','Seasoned Wood Log':'Seasoned Wood Plank','Hard Wood Log':'Hard Wood Plank','Elder Wood Log':'Elder Wood Plank','Ancient Wood Log':'Ancient Wood Plank'}

    return unrefined_to_refined


"""
The purpose of testing generate_multiplier is to make sure that:
    the proper ingots are being selected with the metals
    regular unrefiend and refined materials are being evaluated correctly
    materials can be "passed" on being refined correctly by not having their
"""
"""
compute_data = [
    ()
]
"""
"""
@pytest.mark.parametrize("test_unrefined_dct,test_refined_dct,test_buysell,expected_multiplier_dct,expected_decision_dct,expected_refined_lookup")
def test_generatingMultiplier():
    generate_multiplier(unrefined_dct,refined_dct,refined_scalar,refined_lookup,buysell)
"""
"""
The purpose of testing is to check that the math of dictionary multiplication and summation is working correctly

Test cases:
    TP cut is True
    TP cut is False
"""
@pytest.mark.parametrize("test_droprate,test_multiplier,test_TPcut,expected_salvageValues,expected_salvageSum",[({"a":1},{"a":1},False,{"a":1},1),
                                                                                                                ({"a":2,"b":3},{"a":1,"b":1},False,{"a":2,"b":3},5)
                                                                                                                ])
def test_sell(test_droprate,test_multiplier,test_TPcut,expected_salvageValues,expected_salvageSum):
    salvageValue_dct,sum_val = calc_helpers.compute_result(test_droprate,test_multiplier,test_TPcut)
    assert salvageValue_dct == expected_salvageValues
    assert sum_val == expected_salvageSum
