#!/usr/bin/perl
open(IN,"trans_list");
@ligands=<IN>;
close IN;
$len= scalar@ligands;
for ($i=0;$i<$len;$i++)
     {
     chomp  $ligands[$i];
     print $ligands[$i],"\n";
system("/home/naveen/Downloads/mgltools_x86_64Linux2_1.5.6/bin/pythonsh /home/naveen/Desktop/work/DHFR/Dock_pgms/prepare_ligand4.py -l $ligands[$i] -U '' -A 'hydrogens'\n");
     }
