#*********************************************************************************************/
#*                                                                                           */
#*         SCRIPT FOR TRANSFORMING A MOLECULE TO THE ORIGINE CORDINATES                      */
#*                                                                                           */
#*********************************************************************************************/

# This program finds out the mean (x,y,z) cordinate of the molecule.
# calculate the center of the x,y,z-cordinates of the molecule
# and than deduct the center of the ....
# Written on 1st Feb, 2009

#      ATOM    837  H   LEU A  90     -0.568   5.933  10.691   0.00 15.00             H
#$str='ATOM      1  N   PRO A   1     -12.735  38.918  31.287  1.00 39.83           N';
##     012345678901234567890123456789012345678901234567890123456789012345678901234567890
##     0         1         2         3         4         5         6         7         8
#http://bmerc-www.bu.edu/needle-doc/latest/atom-format.html#pdb-atom-format


use vars qw($recname $serial $atom $altLoc $resName $chainID $Seqno $xCor $yCor $zCor $occupancy $tempFactor $footnote $segID $element $charge);


my $file_list = shift;

open(FH_FILE,$file_list);
my @list=<FH_FILE>;
close(FH_FILE);

foreach $file (@list)
{
   chomp $file;

   my ($minX,$minY,$minZ,$maxX,$maxY,$maxZ,$centerX,$centerY,$centerZ)=0;

   $recname=$serial=$atom=$altLoc=$resName=$chainID=$Seqno=$xCor=$yCor=$zCor=$occupancy=$tempFactor=$footnote=$segID=$element=$charge=0;

   open(FH,$file);
   my @file=<FH>;
   close(FH);

   my $firstTime=1;
   foreach(@file)
   {
      if($_ =~ /^ATOM/)
      {
         assignValues($_);

         if($firstTime){$minX=$maxX=$xCor;$minY=$maxY=$yCor;$minZ=$maxZ=$zCor;$firstTime=0;next}
         $minX=($xCor<$minX)?$xCor:$minX;
         $minY=($yCor<$minY)?$yCor:$minY;
         $minZ=($zCor<$minZ)?$zCor:$minZ;

         $maxX=($xCor>$maxX)?$xCor:$maxX;
         $maxY=($yCor>$maxY)?$yCor:$maxY;
         $maxZ=($zCor>$maxZ)?$zCor:$maxZ;
      }
   }

   $centerX = ($minX+$maxX)/2;
   $centerY = ($minY+$maxY)/2;
   $centerZ = ($minZ+$maxZ)/2;

   #print $centerX,"\t",$centerY,"\t",$centerZ,"\n";
   #exit;

   $file =~ s/.pdb/_transformed.pdb/;

   open(FH,">$file");
   foreach(@file)
   {
      if($_ !~ /^ATOM/){ print FH $_; next}
      if($_ =~ /^ATOM/)
      {
         assignValues($_);

         $xCor-=$centerX;
         $yCor-=$centerY;
         $zCor-=$centerZ;
#$~ = "FFTOUT";
         write (FH);
      }
   }
}

#print " The center cordinate of the molecule: ",$centerX,"\t",$centerY,"\t",$centerZ,"\n";

sub assignValues()
{
   $str = shift;
        $recname=substr($str,0,6);
        $serial=substr($str,6,5);
        $atom=substr($str,12,4);
        $altLoc=substr($str,16,1);
        $resName=substr($str,17,3);
        $chainID=substr($str,21,1);
        $Seqno=substr($str,22,5);
        $xCor=substr($str,30,8);
        $yCor=substr($str,38,8);
        $zCor=substr($str,46,8);
        $occupancy=substr($str,54,6);
        $tempFactor=substr($str,60,6);
        $footnote=substr($str,66,6);
        $segID=substr($str,72,4);
        $element=substr($str,76,2);
        $charge=substr($str,78,2);

      $xCor=~s/ //; $yCor=~s/ //; $zCor=~s/ //;
}

format FH =
#0         1         2         3         4         5         6         7          # COUNTER OF THE INDEX
#01234567890123456789012345678901234567890123456789012345678901234567890123456789 # INDEX
#ATOM     86  CG  ARG    11      -2.455   1.706  24.211  1.00 17.72      1AAK 146 # EXAMPLE LINE
@<<<<<@>>>> @|||@@|| @@>>>>   @##.### @##.### @##.### @>>>>>@>>>>>@|||| @<<<@<@<
$recname,$serial,$atom,$altLoc,$resName,$chainID,$Seqno,$xCor,$yCor,$zCor,$occupancy,$tempFactor,$footnote,$segID,$element,$charge
.

#format OUT =
#TEST
#.
#@<<<     @#  @<<<@<<   @<<<     @##.###  @#.###  @#.###  @.##  @.##    @#.###
#$cordinates[0],$cordinates[1],$cordinates[2],$cordinates[3],$cordinates[4],$cordinates[5],$cordinates[6],$cordinates[7],$cordinates[8],$cordinates[9],$cordinates[10]
#.

