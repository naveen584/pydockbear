#!/usr/bin/perl 
#===============================================================================
#
#         FILE: parse.pl
#
#        USAGE: ./parse.pl  
#
#  DESCRIPTION: 
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (), 
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 06/11/2014 12:56:52 PM
#     REVISION: ---
#===============================================================================
use strict;
use warnings;
open(OUT,">positive_Vina_energy");
my $list=shift;
open (F,$list);
my @file=<F>;
#shift @file;
print OUT "Ligand Name\tVINA Energy\n";
foreach (@file)
{
	chomp $_;
	my $filename=$_;
	system("sed -i '/^\$/d' $_/log.txt");
	open(LIST, "$_/log.txt")||die "can not open file";
	while (<LIST>)
	{
		chomp $_;
		if ($_=~/^\s+1/)
		{
			my @temp=split '\s+',$_;
			print OUT "$filename\t$temp[2]\n";
		}
	}
}
close LIST;
