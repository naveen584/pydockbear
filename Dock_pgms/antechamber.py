#!/usr/bin/python
"""
Created on Mon Feb 3 2017

@author: dockpybear49_sit@jnu.ac.in

"""
__author__ = 'naveen Kumar'
__email__ = 'naveen49_sit@jnu.ac.in'
import os
import subprocess
from os.path import dirname, abspath
from shutil import copy2
from subprocess import check_output as run
from time import sleep
FOLDER = ['ligands', 'decoys']
# FOLDER = ['folder1', 'folder2']
# RESULT_FOLDER = ['folder1_result', 'folder2_result']
RESULT_FOLDER = ['ligand_result', 'decoys_result']

MMPBSA_result = 'MMPBSA_result'
#antechamber_cmd = 'antechamber -i {0} -fi pdb -o {2}.mol2 -fo mol2 -c bcc -s 2 -nc {1} &>/dev/null'
antechamber_cmd = 'antechamber -i {0} -nc 3 -fi pdb -o {0}.mol2 -fo mol2 -c bcc -s 2'
parm_chk = 'parmchk2 -i {0}.mol2 -f mol2 -o {0}.frcmod &>/dev/null'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
KEY = 'ZINC'
DHFR = dirname(dirname(abspath(__file__)))
MMPBSA_result_dir = os.path.join(DHFR, MMPBSA_result)
automation_task = os.path.join(DHFR, 'input_files')


def execute():
    try:
        for folder in RESULT_FOLDER:
            # Reset counter and ligands result for each result folder
            ligands = []
            active_dir = os.path.join(DHFR, folder, 'vina_ligand',
                                      'ligand', 'active')

            files_list = os.listdir(active_dir)
            print('FILE_LIST_________________ %s ' % files_list)
            for f in files_list:  # get all ligands
                # if str(f).startswith('ligand') and str(f).endswith(
                if str(f).startswith(KEY) and str(f).endswith(
                        '.pdbqt.pdb'):
                    ligands.append(f)
            print('\nTotal %d Ligands found in %s ' % (len(ligands),
                                                       active_dir))

            antechamber_data = os.path.join(active_dir, 'antechamber_data')
            result = os.path.join(active_dir, 'result')

            # Creating antechamber_data directory
            if not os.path.exists(antechamber_data):
                os.makedirs(antechamber_data)
            if not os.path.exists(result):
                os.makedirs(result)

            print('Copying (%s)s to %s' % (KEY, antechamber_data))
            # Copy all ligands in antechamber_data
            for ligand in sorted(ligands):
                # Copy ligand file to antechamber_data
                src = os.path.join(active_dir, ligand)
                dst = os.path.join(antechamber_data)
                copy2(src, dst)
                os.chdir(antechamber_data)
                print 'Current files in antechamber_data %s' % os.listdir(antechamber_data)
                print('\nExecuting antechamber for %s' % ligand)
                # Run antechamber and paramchk command
                subprocess.call([antechamber_cmd.format(ligand)],
 
 
 
 
                                cwd=antechamber_data,shell=True)
                print '..........Finished executing antechamber for %s ' \
                      '..........\n' % f
                print('..........Executing parmchk for %s ..........' % ligand)
                sleep(2)  # wait for 2 seconds
                subprocess.call([parm_chk.format(ligand)],
                                cwd=antechamber_data, shell=True)
                print('..........Finished executing parmchk for %s ' \
                      '..........' % ligand)

            # Lets setup to result folder
            # lets get .mol2 and .frcmod first
            sleep(20)
            mol2_str = '_trnsfrmd.pdbqt1.pdbqt.mol2_bcc.mol2'
            frcmod_str = '_trnsfrmd.pdbqt1.pdbqt.mol2_bcc.mol2.frcmod'
            ant_files = os.listdir(antechamber_data)
            for _f in ant_files:
                if str(_f).startswith(KEY) and str(_f).endswith('.mol2'):
                    mol2 = os.path.join(antechamber_data, _f)
                    new_mol2 = str(_f).split('.')[0] + mol2_str
                    new_mol2 = os.path.join(result, new_mol2)
                    copy2(mol2, new_mol2)
                elif str(_f).startswith(KEY) and str(_f).endswith('.frcmod'):
                    frcmod = os.path.join(antechamber_data, _f)
                    new_frcmod = str(_f).split('.')[0] + frcmod_str
                    new_frcmod = os.path.join(result, new_frcmod)
                    copy2(frcmod, new_frcmod)

            src_script = os.path.join(DHFR, 'Dock_pgms', 'script.py')
            script = os.path.join(result, 'script.py')
            src_receptor = os.path.join(automation_task,
                                        'receptor_transformed.pdbqt.pdb')
            dst_receptor = os.path.join(result,
                                        'receptor_transformed.pdbqt.pdb')
            copy2(src_script, script)
            copy2(src_receptor, dst_receptor)
            subprocess.call(['chmod', '777', script])
            os.chdir(result)
            #os.system('/bin/bash script.sh')
            from .script import setup
            # run script.py
            setup()
            os.system('/usr/bin/python %s' % script)
            #os.system('/usr/bin/python script.py')
            # move results
            decoys_mmpbsa_dir = os.path.join(MMPBSA_result_dir, 'decoys_mmpbsa', 'result')
            ligand_mmpbsa_dir = os.path.join(MMPBSA_result_dir, 'ligand_mmpbsa', 'result')
            if 'ligand_result' == folder:
                final_result = ligand_mmpbsa_dir
            else:
                final_result = decoys_mmpbsa_dir
            import shutil
            if not os.path.exists(final_result):
                print('Moving results to %s' % final_result)
                shutil.copytree(result, final_result)
    except Exception as ExError:
        print('*' * 50)
        val = input('Error %s occured, Do you want to retry Antechamber '
                        '?(YES/NO) ' % ExError)
        if val.lower() == 'yes' or val.lower() == 'y':
            execute()
        else:
            exit()
