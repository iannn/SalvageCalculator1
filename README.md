# SalvageCalculator1
First pass of salvage calculator scripts

Main files:
calc_salvage.py - to calculate the value and profits from salvaging salvage items for profit
calc_unid.py - to calculate the value and profits from salvaging unids
calc_helpers.py - common functions between salvage and unid
calc_ecto.py - a quick check on the potential profits and savings when dealing with ectos and crystalline dust

Tests:
pytest tests can be run from this root directory or from the SalvageScripts folder using "pytest" or "pytest -v"

Tests are located in the SalvageScripts folder because these are little helper scripts to be run, not a package to install. The recommended structure for this case is apparently putting a "tests" folder inside the folder the scripts to be tested are in. Pytest and the official Python foundation packaging tutorials have other suggestions.

Project notes:
calc_salvage is looking really good and pretty much done. Can calculate the sell values of every salvage item (minus the special garments that aren't on the chart) and the expected profits. Savings from salvaging not done yet. Forge promotions not included yet either

calc_unid needs a complete rework. Needs drop rate data on greatswords because they apparently drop enough where it's worth including them. Crystalline dust should also be used instead of Ectoplasm because that all adds up. Precursors drop every ?374k? (has been mentioned before in discussions) so that kinda needs to be included. Some way to calculate the value of exotics from unids as well needs to be done too. All those add up. Also note that as long as unids are about the equivalent price of crystalline dust, you're saving gold.

calc_ecto is simple and basically done/doesn't need any work.

Pytest work in progress.
