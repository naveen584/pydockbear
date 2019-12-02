#!/usr/bin/python
import logging
import subprocess
from glob import glob
from os import chdir, makedirs, system, path, rmdir, getcwd
from shutil import copy2
from subprocess import check_output as run
from Dock_pgms import copy_database, antechamber
import sys

logging.basicConfig(format='%(message)s', level=logging.INFO)
AICII_START = '''\033[95m
# #######################################################################################################
#        / \  _   _| |_ ___  _ __ ___   __ _| |_(_) ___  _ __   / ___|  ___ _ __(_)_ __ | |_
#       / _ \| | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \  \___ \ / __| '__| | '_ \| __|
#      / ___ \ |_| | || (_) | | | | | | (_| | |_| | (_) | | | |  ___) | (__| |  | | |_) | |_
#     /_/   \_\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_| |____/ \___|_|  |_| .__/ \__|
#                                                                                 |_|for pydockbear
\033[0m'''
print(AICII_START)

USERNAME = "naveen"
DOWNLOADS = "/home/{}/Downloads".format(USERNAME)
DESKTOP = "/home/{}/Desktop/work".format(USERNAME)
VINABIN = "/usr/local/bin"
DOCK = "{}/DHFR/Dock_pgms".format(DESKTOP)
#script2 = "{}/script2.py".format(DOCK)
sys.path.append(DOCK)
FOLDER = antechamber.FOLDER
RESULT_FOLDER = antechamber.RESULT_FOLDER
KEY = 'ZINC' # Command string in the ligand name

def cleanup():
    if path.exists('{}/DHFR/%s'.format(DESKTOP, RESULT_FOLDER[0])):
        rmdir("{}/DHFR/%s/ligand".format(DESKTOP, RESULT_FOLDER[0]))
    if path.exists('{}/DHFR/%s'.format(DESKTOP, RESULT_FOLDER[1])):
        rmdir("{}/DHFR/%s/ligand".format(DESKTOP, RESULT_FOLDER[1]))
    chdir("{}/DHFR/".format(DESKTOP))


def list_dir(path, outfile=None, nl=True):
    files = glob(path)
    if files == '':
        print('WARNING! NO file in ligand!')
    if outfile:
        with open(outfile, "w") as f:
            for i in files:
                if i == '.':
                    f.write("")
                elif nl:
                    f.write(i + "\n")
                else:
                    f.write(i + " ")
    else:
        return files


def processing():
    result_folders = RESULT_FOLDER
    for rfolder in result_folders:
        rfolder = path.join(DESKTOP, 'DHFR', rfolder)
        chdir(rfolder)
        print("we are using X,Y and Z for receptor transformation:27.658 -24.638 9.756")
        print(run(
            "{}/mgltools_x86_64Linux2_1.5.6/bin/pythonsh {}/DHFR/Dock_pgms/transform-receptor.py ../receptor.pdb  27.658  -24.638 "
            "9.756".format(DOWNLOADS, DESKTOP), shell=True))

        # Was required to move selected ligands
        rfolder_ligand = path.join(rfolder, 'ligand')
        if not path.exists(rfolder_ligand):
            makedirs(rfolder_ligand)

        ###### Pre_Processing ######
        print("Starting AutoDock Vina Framework ...\n")
        # Transforming the Receptor

        print("Transforming the ligands...")
        chdir(rfolder)
        list_dir("%s*.pdb" % KEY, "lig_list")
        run("perl {}/DHFR/Dock_pgms/transform-ligand.pl lig_list".format(
            DESKTOP),
            shell=True)
        # chdir(DESKTOP)
        # chdir('..')
        print("Transforming the ligands .. Completed!\n")

        print("Preparing the receptor..")
        print(run(
            "{}/mgltools_x86_64Linux2_1.5.6/bin/pythonsh {}/DHFR/Dock_pgms/prepare_receptor4.py -r receptor_transformed.pdb "
            "-U '' -A 'checkhydrogens'".format(
                DOWNLOADS, DESKTOP, rfolder), shell=True))
        print("Preparing the receptor.. Completed!\n")
        print("Preparing the ligands..")
        chdir(rfolder_ligand)
        list_dir("%s*.pdb" % KEY, path.join(rfolder_ligand, "trans_list"))
        # list_dir("lig*_transformed.pdb", path.join(rfolder_ligand, "trans_list"))
        run("perl {}/prepare_ligand.pl".format(DOCK), shell=True)
        list_dir("*transformed.pdbqt", path.join(rfolder, "pdbqt_list"))
        chdir("..")
        print("Preparing the ligand.. Completed!\n")

        #### Post_Processing ####
        # Autodock Vina Docking
        vina_ligand = path.join(DESKTOP, 'DHFR', rfolder, 'vina_ligand')
        # try:
        makedirs(vina_ligand)
        # except OSError:
        #     pass
        copy2("receptor_transformed.pdbqt", "vina_{}".format('ligand'))

        vina_lig = path.join(vina_ligand, 'lig')
        # try:
        makedirs(vina_lig)
        # except OSError:
        #     pass

        filelist = list_dir("ligand/%s*.pdbqt" % KEY)
        for i in filelist:
            copy2(i, vina_lig)

        chdir(vina_ligand)
        print(" Autodock Vina Docking starting work..!\n")
        system(
            "sh {}/DHFR/Dock_pgms/vina_VS_input_final.sh "
            "receptor_transformed.pdbqt lig/ 30 30 30".format(
                DESKTOP))

        # Change to vina_ligand/ligand
        chdir(path.join(vina_ligand, 'ligand'))
        list_dir('.', path.join(getcwd(), "list1"))
        items = ['Molecules.pdb']
        ligand_list = path.join(rfolder_ligand, 'trans_list')
        list1 = path.join(vina_ligand, 'ligand', 'list1')
        alist = path.join(vina_ligand, 'ligand', 'list')
        items.extend(open(ligand_list, "rb").readlines())
        for a in items:
            val = (a.split('.', 1)[0])
            with open(list1, "a+") as obj:
                obj.write(val + '\n')
            with open(alist, "a+") as al:
                al.write(val + '\n')

        vina_ligand_active = path.join(vina_ligand, 'ligand', 'active')
        _vina_ligand_active = path.join(vina_ligand, 'ligand')
        # try:
        makedirs(vina_ligand_active)
        # except OSError:
        #     pass
        run("perl {}/vina_split.pl list".format(DOCK),
            shell=True)

        copy2("{}/receptor_transformed.pdbqt".format(vina_ligand),
              vina_ligand_active)

        chdir(vina_ligand_active)

        list_dir("*.pdbqt", "pdbqt_list", True)
        run("perl {}/prepare_pdbqt_to_pdb.pl".format(DOCK),
            shell=True)
        chdir(_vina_ligand_active)
        # Vina_energy

        run("ls | grep %s > list_vina" % KEY, shell=True)
        run("perl {}/parse.pl list_vina".format(DOCK),
            shell=True)
        chdir("{}/DHFR/".format(DESKTOP))



if __name__ == "__main__":
    cleanup()
    copy_database.moving()
    processing()
    antechamber.execute()
    print("\nPlease Check MMPBSA Result here for ligands: /home/naveen/Desktop/work/DHFR/MMPBSA_result/ligand_mmpbsa/result..Thanks")
    print("\nPlease Check MMPBSA Result here for Decoys: /home/naveen/Desktop/work/DHFR/MMPBSA_result/decoys_mmpbsa/result...Thanks")
    #subprocess.call(["python", "{}/script2.py".format(DOCK)])
