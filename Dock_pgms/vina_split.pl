#!/usr/bin/perl 
#===============================================================================
#
#         FILE: shilpi_vina_mmpbsa.pl
#
#        USAGE: perl shilpi_vina_mmpbsa.pl <list>  
#
#  DESCRIPTION: reads a list file, containing the names of the ligands used by Vina. 
#               Reads the out.pdbqt file from a directory of the same name, and converts
#               it to mol2 using babel
#      OPTIONS: ---
# REQUIREMENTS: Openbabel
#         BUGS: babel gives errors with the test data. out.pdbqt seems to have multiple poses? 
#        NOTES: script modified from parse.pl present in the Vina results directory
#       AUTHOR: YOUR NAME (), 
# ORGANIZATION: 
#      VERSION: 0.1
#      CREATED: 06/27/2014 21:10:00 PM
#     REVISION: ---
#===============================================================================
use strict;
use warnings;
my $list=shift;
open (F,$list);
my @file=<F>;
shift @file;
foreach (@file)
{
	chomp $_;
	my $filename=$_;
    system("vina_split --input $filename/out.pdbqt --ligand $filename/$filename.pdbqt");
	system("cp $filename/$filename.pdbqt1.pdbqt ./active");
}
close (F);
