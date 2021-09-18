:: This batch file installs the dependencies for the project
ECHO OFF
:: Update PIP
call py -m pip install --upgrade pip
:: Install Pandas
call py -m pip install pandas
:: Install Biopython
call py -m pip install biopython
:: Install xlrd
call py -m pip install xlrd
:: Install openpyxl
call py -m pip install openpyxl
:: Install PySimpleGUI
call py -m pip install PySimpleGUI
:: Install Progress Bar
call py -m pip install progress progressbar2 alive-progress tqdm
:: Install Requests
call py -m pip install requests
:: Download NCBI BLAST
call curl https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.12.0/ncbi-blast-2.12.0+-x64-win64.tar.gz > ncbi_blast.tar.gz 
call tar -xf ncbi_blast.tar.gz 
call del ncbi_blast.tar.gz 
:: Download the pdbaa database
call py download_ncbi_pdbaa.py