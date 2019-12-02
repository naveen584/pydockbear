#!/usr/bin/python
import pprint

__author__ = 'naveen Kumar'
__email__ = 'naveen49_sit@jnu.ac.in'
import os, sys, subprocess, shutil
import multiprocessing
AMBER = 'source /home/naveen/Documents/software/amber18'

# SCRIPTS
leap_cmd = "source /home/naveen/Documents/software/amber18/dat/leap/cmd/oldff/leaprc.ff99SB\n" \
           "source /home/naveen/Documents/software/amber18/dat/leap/cmd/leaprc.gaff\n" \
           "set default pbradii mbondi2\n" \
           "loadamberparams {0}.frcmod\n" \
           "lig = loadmol2 {0}\n" \
           "saveamberparm lig {0}.leap.prm {0}.leap.crd\n" \
           "savepdb lig {0}.leap.pdb\n" \
           "prot = loadpdb receptor_transformed.pdbqt.pdb\n" \
           "saveamberparm prot receptor.leap.prm receptor.leap.crd\n" \
           "savepdb prot receptor.leap.pdb\n" \
           "complex = combine {1}\n" \
           "saveamberparm complex complex_{0}.leap.prm complex_{0}.leap.crd\n" \
           "savepdb complex complex_${0}.leap.pdb\n" \
           "quit\n"

sander_min1_in = "1st Minimization of protein-ligand complex\n" \
                 " &cntrl\n" \
                 "  imin=1, maxcyc=2000, ncyc=500,\n" \
                 "  cut=12, ntb=0, igb=0, ntr=0, dielc=4,\n" \
                 " &end\n" \
                 " &ewald\n" \
                 "  eedmeth=5,\n" \
                 " &end\n"

sander_md_vacuo_in = "100 ps Implicit MD of protein-ligand complex with restraint on protein\n" \
                     " &cntrl\n" \
                     "  imin=0, irest=0, nstlim=50000, dt=0.002, ntc=2, ntf=2,\n" \
                     "  ntpr=1000, ntwx=1000, igb=0,\n" \
                     "  tempi=300.0, temp0=300.0, ntt=3, gamma_ln=5.0, ig=-1\n" \
                     "  cut=12, ntb=0, igb=0, ntr=1, restraint_wt=5.0, restraintmask=':1-231',\n" \
                     " &end\n"

sander_min2_in = "2nd Minimization of protein-ligand complex\n" \
                 " &cntrl\n" \
                 "  imin=1, maxcyc=2000, ncyc=500,\n" \
                 "  cut=12, ntb=0, igb=0, ntr=0, dielc=4,\n" \
                 " &end\n" \
                 " &ewald  eedmeth=5,\n" \
                 " &end\n"

mmpbsa_in = "Input file for running PB and GB in serial\n" \
            "&general\n" \
            "   startframe=1, endframe=1, keep_files=2,\n" \
            "/\n" \
            "&gb\n" \
            "  igb=5, saltcon=0.100, surften=0.0072, molsurf=0, probe=1.4,\n" \
            "/\n" \
            "&pb\n" \
            "  istrng=0.100, exdi=80.0, indi=1.0,\n" \
            "/\n"

run_sh = "#!/bin/bash\n" \
         "#$ -cwd\n" \
         "#$ -S /bin/bash\n" \
         "#$ -e err.\$JOB_ID.\$JOB_NAME\n" \
         "#$ -o out.\$JOB_ID.\$JOB_NAME\n" \
         "#$ -q all.q\n" \
         "#$ -pe mpi 2\n"

FILES = {
    'leap.cmd': leap_cmd,
    'sander_min1.in': sander_min1_in,
    'sander_md_vacuo.in': sander_md_vacuo_in,
    'sander_min2.in': sander_min2_in,
    'mmpbsa.in': mmpbsa_in,
    'run_sh': run_sh
}


def setup():
    # to save the output
    print('_+_'*50)
    cwd = os.getcwd()
    # print(run_cmd(AMBER, cwd=os.getcwd()))
    receptor_file = os.path.join(cwd, 'receptor_transformed.pdbqt.pdb')
    try:
        #
        directory = os.listdir(cwd)
        for item in directory:
            if item.endswith('_bcc.mol2'):
                mol_dir = os.path.join(cwd, item.split('_bcc.mol2')[0])
                item_path = os.path.join(cwd, item)
                try:
                    if not os.path.exists(mol_dir):
                        os.mkdir(mol_dir)
                    shutil.copy2(item_path, mol_dir)
                    shutil.copy2(item_path + '.frcmod', mol_dir)
                    shutil.copy2(receptor_file, mol_dir)
                except IOError as e:
                    print("Unable to copy file. %s" % e)
                except:
                    print("Unexpected error:", sys.exc_info())
                for file in FILES:
                    if 'run_sh' in file:
                        file_path = os.path.join(mol_dir, 'run_%s.sh' % item)
                        with open(file_path, "w") as text_file:
                            text_file.write(FILES['run_sh'])
                    else:
                        file_path = os.path.join(mol_dir, file)
                        with open(file_path, "w") as text_file:
                            text_file.write(FILES[file].format(item,
                                                               '{prot lig}'))
                # tleap -f leap.cmd
                run_cmd("tleap -f leap.cmd", cwd=mol_dir)

                cmd1 = "mpirun -np 4 sander.MPI -O -i sander_min1.in -o sander_min.out -p complex_{0}.leap.prm -c complex_{0}.leap.crd -r complex_{0}.min1.crd".format(item)
                cmd2 = "mpirun -np 4 sander.MPI -O -i sander_md_vacuo.in -o sander_mdVacuo.out -p complex_{0}.leap.prm -c complex_{0}.min1.crd -ref complex_{0}.min1.crd -r complex_{0}.MDvacuo.crd -x complex_{0}.MDvacuo.mdcrd".format(item)
                cmd3 = "mpirun -np 4 sander.MPI -O -i sander_min2.in -o sander_min2.out -p complex_{0}.leap.prm -c complex_{0}.MDvacuo.crd -r complex_{0}.min2.crd".format(item)
                cmd4 = "ambpdb -p complex_{0}.leap.prm <complex_{0}.min2.crd> complex_{0}.min2.pdb".format(item)
                cmd5 = "MMPBSA.py -O -i mmpbsa.in -o ENERGYcomplex_{0}.dat -cp complex_{0}.leap.prm -rp receptor.leap.prm -lp {0}.leap.prm -y complex_{0}.min2.crd".format(item)

                #########################PMEMD on MPI######################################################################################################3
                """"cmd1 = "mpirun -np 4 pmemd.MPI -O -i sander_min1.in -o sander_min.out -p complex_{0}.leap.prm -c complex_{0}.leap.crd -r complex_{0}.min1.crd".format(item)
                cmd2 = "mpirun -np 4 pmemd.MPI -O -i sander_md_vacuo.in -o sander_mdVacuo.out -p complex_{0}.leap.prm -c complex_{0}.min1.crd -ref complex_{0}.min1.crd -r complex_{0}.MDvacuo.crd -x complex_{0}.MDvacuo.mdcrd".format(item)
                cmd3 = "mpirun -np 4 pmemd.MPI -O -i sander_min2.in -o sander_min2.out -p complex_{0}.leap.prm -c complex_{0}.MDvacuo.crd -r complex_{0}.min2.crd".format(item)
                cmd4 = "ambpdb -p complex_{0}.leap.prm <complex_{0}.min2.crd> complex_{0}.min2.pdb".format(item)
                cmd5 = "MMPBSA.py -O -i mmpbsa.in -o ENERGYcomplex_{0}.dat -cp complex_{0}.leap.prm -rp receptor.leap.prm -lp {0}.leap.prm -y complex_{0}.min2.crd".format(item)
                """
                cpus = multiprocessing.cpu_count()
                if cpus > 1:
                    print('%s CPU detected' % cpus)
                else:
                    print('%s CPUs detected' % cpus)
                # Multiprocess the commands
                print('Please have patience it will take some time...')
                run_multiprocessing(cmd1, cmd2, cmd3, cmd4, cmd5, cwd=mol_dir)
                print('Process complete...')

    except Exception as e:
        raise e
    print('_+_' * 50)


def run_multiprocessing(*commands, **kwargs):
    cwd = kwargs.get('cwd') or os.getcwd()
    for cmd in commands:
        proc = multiprocessing.Process(target=run_cmd(cmd, cwd))
        proc.start()

def run_cmd(cmd, cwd=None):
    try:
        if cwd is None:
            cwd = os.getcwd()
        os.chdir(cwd)
        os.system(cmd)
    except:
        return ('Failed to execute (%s)' % cmd)


if __name__ == "__main__":
    setup()
