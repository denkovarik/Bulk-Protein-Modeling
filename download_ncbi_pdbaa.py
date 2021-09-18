import PySimpleGUI as sg
import requests
import tarfile
import os


def dwnl_db(path):
    """
    Downloads the NCBI pdbaa database and stores it in the directory specified 
    by 'path'.
    
    :param path: The path to the directory to store the database in.
    """
    url = 'https://ftp.ncbi.nlm.nih.gov/blast/db/pdbaa.tar.gz'
    db_compressed = path + 'pdbaa.tar.gz'
    msg = "Please note that downloading the database may take a while.\n\n"
    msg += "Click OK to start downloading the database."
    sg.popup(msg)
    # Download the Database
    r = requests.get(url, allow_redirects=True)
    # Write compressed file to the specified path
    open(db_compressed, 'wb').write(r.content)  
    # Extract the database files
    db = tarfile.open(db_compressed)   
    # extracting file
    db.extractall(path)
    db.close()
    os.remove(db_compressed)
    

def main():
    """
    This is the main program that runs the program.
    """
    layout = [[sg.Text('Choose Location to Store NCBI PDB Database', size=(36, 1), \
                    justification='center', font=("Helvetica", 25), \
                    relief=sg.RELIEF_RIDGE)], 
              [sg.Text('Select Location to Store Database'), \
                    sg.InputText(key='--src'), sg.FolderBrowse()],
              [sg.Button("Go", key="dwnl")]]
                    
    window = sg.Window('Choose Location to Store NCBI PDB Database', layout, \
                    resizable=True, finalize=True)
    
    # Loop for the main window
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == 'Configure':
            if window.TKroot.state() == 'zoomed':
                status.update(value='Window zoomed and maximized !')
            else:
                status.update(value='Window normal')
        elif event == 'dwnl':
            if values['Browse'] == "":
                sg.popup("Please select a location to store the database.")
            else:
                path = values['Browse'] + '/'
                dwnl_db(path)
                window.close()
        
    window.close()
    
    
if __name__ == "__main__":
    main()