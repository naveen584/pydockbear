'''
Created on Mon Jul 15 2017

@author: james

'''
import logging
import sys
from glob import glob
from os import chdir, path, makedirs, system
from shutil import copyfileobj

from Dock_pgms import load_database, antechamber

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

USERNAME = "james"
DESKTOP = "/home/{}/Desktop/work/DHFR".format(USERNAME)
DOWNLOADS = DESKTOP + '/input_files'
DOCK = "{}/DHFR/Dock_pgms".format(DESKTOP)
sys.path.append(DOCK)
CURRENT_DIR = path.dirname(path.realpath(__file__))
MAYACHEMTOOL = path.join(CURRENT_DIR, 'mayachemtools', 'bin')
FOLDERNAME = antechamber.FOLDER
RESULT_FOLDER = antechamber.RESULT_FOLDER
MMPBSA_result = antechamber.MMPBSA_result
MMPBSA_result_dir = path.join(DESKTOP, MMPBSA_result)
decoys_mmpbsa_dir = path.join(MMPBSA_result_dir, 'decoys_mmpbsa')
ligand_mmpbsa_dir = path.join(MMPBSA_result_dir, 'ligand_mmpbsa')
if not path.exists(MMPBSA_result_dir):
    makedirs(MMPBSA_result_dir)
    makedirs(decoys_mmpbsa_dir)
    makedirs(ligand_mmpbsa_dir)


def moving():
    """
    f1_count = 0
    #print('#####' *30+ '\n')
    #print("no of ligands selected for Docking & MMPBSA= ")
    #print("no of decoys selected for Docking  & MMPBSA = ")
    #print('#####' * 30 + '\n')
    f2_count = 0
    #print('#####' *30+ '\n')
    """
    f1_count = input(
        'How many files you want to run for Docking & MMPBSA of %s? \n Enter an integer: ' %
        FOLDERNAME[0])
    #print('______+' * 30 + '\n')
    f2_count = input(
        'How many files you want to run for Docking  & MMPBSA of %s? \n Enter an integer: ' %
        FOLDERNAME[1])
        
    #print('#####' *30+ '\n')

    chdir('{}/databases'.format(DOWNLOADS))
    load_database.upload_data()
    lig_path1 = path.join(DESKTOP, FOLDERNAME[0])
    lig_path2 = path.join(DESKTOP, FOLDERNAME[1])

    #mayachemtool(lig_path1, 'dhfr_ligands.sdf')
    #mayachemtool(lig_path2, 'dhfr_decoys.sdf')
    babel_start(lig_path1, FOLDERNAME[0])
    babel_start(lig_path2, FOLDERNAME[1])
    if not path.exists(path.join(DESKTOP, RESULT_FOLDER[0], 'ligand')):
        makedirs(path.join(DESKTOP, RESULT_FOLDER[0], 'ligand'))
    if not path.exists(path.join(DESKTOP, RESULT_FOLDER[1], 'ligand')):
        makedirs(path.join(DESKTOP, RESULT_FOLDER[1], 'ligand'))
    # One time activity
    chdir(path.join(DESKTOP, FOLDERNAME[0]))
    files = glob('*.pdb')

    logging.info('Moving to ligand folder starting')
    try:
        f1_count = int(f1_count)
        f2_count = int(f2_count)
    except ValueError:
        logging.info('Incorrect input please try again!\n')
        moving()
    while f1_count > len(files):
        f1_count = int(input(
            'Error: Enter an integer between 0 to {} :'.format(
                len(files))))
        if f1_count <= len(files):
            break
    for i in sorted(files)[:f1_count]:
        with open('{}/{}/{}'.format(DESKTOP, FOLDERNAME[0], i),
                  'rb') as f_in, open(
            '{}/{}/{}'.format(DESKTOP,
                              path.join(RESULT_FOLDER[0], 'ligand'), i),
            'wb') as f_out: copyfileobj(f_in, f_out)

    chdir(path.join(DESKTOP, FOLDERNAME[1]))
    files = glob('*.pdb')
    logging.info('Moving to ligand folder starting')
    while f2_count > len(files):
        f2_count = int(input(
            'Error: Enter an integer between 0 to {} :'.format(
                len(files))))
        if f2_count <= len(files):
            break
    for i in sorted(files)[:f2_count]:
        with open('{}/{}/{}'.format(DESKTOP, FOLDERNAME[1], i),
                  'rb') as f_in, open(
            '{}/{}/{}'.format(DESKTOP,
                              path.join(RESULT_FOLDER[1], 'ligand'),
                              i), 'wb') as f_out:
            copyfileobj(f_in, f_out)

def babel_start(path, filename):
    chdir(path)
    logging.info("Babel command start for %s!" % filename)
    system(
        "babel -isdf *.sdf -opdb *.pdb -h --partialcharge gasteiger --gen3")
    logging.info("Babel command completed!")


def mayachemtool(path, filename):
    chdir(path)
    logging.info("Mayachemtool command start for %s" % filename)
    system(
        "perl %s/SplitSDFiles.pl -m Cmpds --numcmpds 1 -c MolName -o %s > "
        "/dev/null" % (
            MAYACHEMTOOL, filename))
    logging.info("Mayachemtool command completed!")


if __name__ == "__main__":
    moving()
