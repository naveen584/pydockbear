import os
import sys
from random import *
from string import *
def pdb_data_string(en):
    
    if len(en[2])<=3:
        spacer="  "
        spacer2=" "
    else:
        spacer=" "  
        spacer2="  "  
    #try:
    strn=en[0]+en[1].rjust(8)+en[2].rjust(8)+en[3].rjust(8)+en[4]
    #except:
    #strn=0
#     pass
    return strn
#ATOM     37  C4'   G A   2      -4.123   2.828   4.227  1.00  1.00           C

def read_pdb(pdbfl,nw_pdbfl):
    flid=open(pdbfl,'r');
    flidw=open(nw_pdbfl,'w');
    all_data=flid.readlines()
    success=0
    flid.close()
    

                
    for lns in all_data:
        pr_str=pdb_data_string(lns)
        print pr_str
        flidw.write(lns)
    success=1
    return success



def pdb_splitter(pdbf):
# 
#  1 -  6        Record name     "ATOM  "  
#  7 - 11        Integer         Atom serial number.  
# 13 - 16        Atom            Atom name.   
# 17             Character       Alternate location indicator.
# 18 - 20        Residue name    Residue name.  
# 22             Character       Chain identifier.   
# 23 - 26        Integer         Residue sequence number. 
# 27             AChar           Code for insertion of residues.  
# 31 - 38        Real(8.3)       Orthogonal coordinates for X in Angstroms. 
# 39 - 46        Real(8.3)       Orthogonal coordinates for Y in Angstroms. 
# 47 - 54        Real(8.3)       Orthogonal coordinates for Z in Angstroms.                            
    fl=open(pdbf,'r')
    data=fl.readlines()	
    fl.close()
    out=[];
    for l in data:
        if len(l)>5:
            if l[0:4]=='ATOM' or l[0:6]=='HETATM' :
                pre_data=str(l[0:30])
                xi=float(strip(l[30:38]))
                yi=float(strip(l[38:46]))
                zi=float(strip(l[46:54]))
                post_data=str(l[54:])
                out.append([pre_data,xi,yi,zi,post_data])
            else: out.append([l])     
        else:   out.append([l])         
    
    return out


def my_program(pdbflr,xi,yi,zi):
    datar=pdb_splitter(pdbflr)
    nw_pdbfl='receptor_transformed.pdb'
    flidw=open(nw_pdbfl,'w');
    for lnsd in datar:
        if len(lnsd)>1:
#             lnsd[1]='{:0.3f}'.format(lnsd[1]+xi)
#             lnsd[2]='{:0.3f}'.format(lnsd[2]+xi)
#             lnsd[3]='{:0.3f}'.format(lnsd[3]+xi)
            lnsd[1]="%0.3f" % (lnsd[1]-xi)
            lnsd[2]="%0.3f" % (lnsd[2]-yi)
            lnsd[3]="%0.3f" % (lnsd[3]-zi)
            pr_str=pdb_data_string(lnsd)
        else: pr_str=lnsd[0] 
        flidw.write(pr_str)
        
        
pdbflnmr=sys.argv[1]
print pdbflnmr
xii=float(sys.argv[2])
yii=float(sys.argv[3])  
zii=float(sys.argv[4])
my_program(pdbflnmr,xii,yii,zii)
