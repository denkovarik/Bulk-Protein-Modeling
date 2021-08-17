@echo off
call cd ..\
call curl https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.12.0/ncbi-blast-2.12.0+-x64-win64.tar.gz > ncbi_blast.tar.gz 
call tar -xf ncbi_blast.tar.gz 
call del ncbi_blast.tar.gz 
call cd setup\