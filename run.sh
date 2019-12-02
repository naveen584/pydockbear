
docker run -it --rm  --name dockpybear-ligand-decoys-test  \
-v /home/naveen/Desktop/work3/DHFR/ligands:/home/dockpybear/Desktop/work/DHFR/ligands  \
-v /home/naveen/Desktop/work3/DHFR/decoys:/home/dockpybear/Desktop/work/DHFR/decoys  \
-v /home/naveen/Desktop/work3/DHFR/receptor.pdb:/home/dockpybear/Desktop/work/DHFR/receptor.pdb  \
 dockpybear-ligand-decoys:latest  

