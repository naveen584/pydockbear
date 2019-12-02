#! /bin/bash


mkdir -p ligand
python /home/naveen/Desktop/work/DHFR/Dock_pgms/conf_input_final.py $1 $3 $4 $5
cd $2

for f in *.pdbqt; do
    b=`basename $f .pdbqt`
    echo -e "Processing ligand $b..\n"
    mkdir -p ../ligand/$b
    echo  -e "Starting for $f ..\n"
 vina --receptor ../$1 --config ../conf.txt --ligand $f --out ../ligand/${b}/out.pdbqt --log ../ligand/${b}/log.txt
 echo  -e "Completed for $f ..\n"
done











































###MAYANK #########
###MAYANK #########

###MAYANK #########

###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
###MAYANK #########
