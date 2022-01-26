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
calc_salvage is looking really good and pretty much done. Can calculate the sell values of every salvage item (minus the special garments that aren't on the chart) and the expected profits.

Savings from salvaging not done yet.
Forge promotions not included yet either.
Refactor to merge item drop rates into a mega dictionary for salvage type should also be done.

calc_unid needs a complete rework.

Greatswords drop enough with high enough value where it's worth including them. Other rares like daggers have high precursor values so tracking on them/all weapons might be warranted. This might mean that all rare weapon types need to be tracked but that's a lot of data to manually log. Very gross. I don't track forging though so hmmm.
Crystalline dust should also be used instead of Ectoplasm because that all adds to the value of an unid.
Precursors drop every ?374k? (has been mentioned before in discussions) so that needs to be included in math somehow.
Value of exotics from unids needs to be calculated too (average tp price of all 76-80 exotics but possibly check for higher values from salvaging e.g. inscriptions, insignia, upgrades, ecto->dust value, other material).
When rare unids are about the equivalent price of crystalline dust, you're saving gold in the long run if you're using said dust too but I don't use it for much.

calc_ecto is simple and basically done/doesn't need any work.

Pytest Initial cases finished.
