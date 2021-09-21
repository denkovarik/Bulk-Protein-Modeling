# Bulk-Protein-Modeling Version 1.0

## Introduction
Protein modeling is the process of attempting to determine a proteins 3D structure by using its amino acid sequence. Determining a proteins 3D structure manually through experimentation can take years and isn't even guaranteed to be successful. Luckily, there are software tools available to help researcheres predict the structure of a target protein within a reaonable amount of time. One such tool is [MODELLER](https://salilab.org/modeller/). This software uses a template protein to attempt to predict the structure of a target protein. In addition, the [NCBI BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi) software can be used to help choose a template protein for the protein being modeled. Software like these are of great value to researchers in Bioinformatics, but sometimes they may what to perform protein modeling on a large number of proteins. Doing this, researchers can spend alot of time doing redundant tasks that could be automated. 

This software was designed to automate the tasks for performing protein modeling using the MODELLER and NCBI BLAST softwares. This software will read a FASTA file (containing multiple sequences) and perform protein modeling on each one. For each sequence, it will automatically run the PSI BLAST algorithm on the protein's amino acid sequence to determine best template protein to use, download the template protein from PDB, and run the MODELLER software to predict the protein's structure. Future versions of this software will include steps to perform verification for the protein model and search online databases for other proteins having a similar structure.


## Setup
This project was developed for the Window's Operating System on a 64 bit machine.

### Dependencies
* Git
* Python 3
* PIP
* [Biopython](https://biopython.org/)
* [MODELLER](https://salilab.org/modeller/)
* [BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
* pillow
* pandas
* openpyxl
* PySimpleGUI
* xlrd

### Download and Install MODELLER
This software relies on the MODELLER software to model the proteins. You can download the software [here](https://salilab.org/modeller/download_installation.html), although you will need a license for it.

### Download and Install PyMOL
After you have successfully modeled a protein, you will need to download software to view it. I suggest install [PyMol](https://pymol.org/2/) or [Discovery Studio Visualizer](https://discover.3ds.com/discovery-studio-visualizer-download) for Windows. Discovery Studio Visualizer is free to download. For PyMOL, you can download and use the trial version of the software for free (although its functionality is limited).

### Install Git on Windows
The first thing you need to do is to make sure that Git is installed on your device. This will allow you to clone and download this repository on your device. If necessary, the tutorial [Install Git](https://github.com/git-guides/install-git) will walk you through how to do this.

### Install Python 3.9
This project relies on Python 3.9 to run and PIP to install other dependencies. You can download Python via this link, [Python 3.9 Download](https://www.python.org/downloads/). Once the download is complete, launch the installer. 

Make sure that you check the box 'Add Python 3.9 to PATH'.\

![Python Setup](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/Python_install.PNG)

Otherwise, use all the default parameters and just click through the setup wizard to install Python. Once the install is complete, you can verify if python was installed correctly by doing the following. Close out of the command prompt if open an then run it again. Then type 'py' and press Enter on the command prompt to invoke python. 

![Invoke Python](https://github.com/denkovarik/Annotate-KEGG-Pathway/blob/main/images/invoke_python.PNG)

If you get something like the above image, then python was installed correctly. Otherwise, something went wrong with your installation of Python. Try reinstalling it.

### Cloning This Repo with HTTPS
To download this repository on your device, you must clone this repo using either HTTPS or SSH. The easiest way to clone this repository on your local device is through HTTPS. If your SDK allows you to clone a repo through HTTPS, then do so. Otherwise, you can do it directly on the command prompt. To do so, open up the command prompt and move into the desired directory. Then simply run the following command and press Enter.

```
git clone https://github.com/denkovarik/Bulk-Protein-Modeling.git
```

Enter in your credentials if prompted to do so. After the repo has been cloned on your device, move into the Bulk-Protein-Modeling directory from the command line.

```
cd Bulk-Protein-Modeling
```

### Cloning This Repo with SSH
You can also clone this repo using SSH. Follow the instructions below to clone the repo using SSH. Please note that if you have already cloned the repo using HTTPS, then you can skip to the 'Install Dependencies' step. If you wish to clone this repo using SSH, then please note that you will need an account on Github or Gitlab.

#### Generate an SSH Key Pair
In order to clone this repository, you need to add your public SSH key to this repo. If you don't have one, then you would need to generate one. [How to Generate SSH key in Windows 10? Easy Methods!!](https://techpaal.com/how-to-generate-ssh-key-in-windows-10-easy-methods/) should help you generate an SSH key pair.

#### Add Your Public SSH Key to GitHub
Once you have an SSH Key Pair generated, you need to add your public SSH key to GitHub. Follow [How to view your SSH keys in Linux, macOS, and Windows](https://www.techrepublic.com/article/how-to-view-your-ssh-keys-in-linux-macos-and-windows/) to access you public key. Then follow [Adding a new SSH key to your GitHub account](https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account) to add your public SSH key to GitHub.

#### Clone the Repository
If your SDK allows for it, then clone this repository through your SDK. Otherwise, open up the command prompt, move into the directory of your choice, then run the following command.
```
git clone git@github.com:denkovarik/Bulk-Protein-Modeling.git
```
After the repo has been cloned on your device, move into the Bulk-Protein-Modeling directory from the command line.
```
cd Bulk-Protein-Modeling
```

### Install Dependencies
Next, install the dependencies needed for the project. This can be done by simply running 'setup.bat' by doulble clicking on it in the file explorer. Alternatively, you can run this script by executing the following command on the command line from within the project directory.
```
setup.bat
```
