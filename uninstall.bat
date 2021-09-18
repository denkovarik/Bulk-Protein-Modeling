:: This batch file uninstalls the dependencies for the project
ECHO OFF
:: Uninstall Pandas
call py -m pip uninstall pandas
:: Uninstall Biopython
call py -m pip uninstall biopython
:: Uninstall xlrd
call py -m pip uninstall xlrd
:: Uninstall openpyxl
call py -m pip uninstall openpyxl
:: Uninstall PySimpleGUI
call py -m pip uninstall PySimpleGUI
:: Uninstall Progress Bar
call py -m pip uninstall progress progressbar2 alive-progress tqdm