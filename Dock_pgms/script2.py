import os

print "How many graphs you want to add?"
n=int(raw_input())
array_ff=[None]*n
array_gg=[None]*n
k=[]
l=[]
h=[]



r_file = open("log.R", "w")
r_file.write("library(\"enrichvs\")")


for i in range(0,n):
    print "Enter the Name of method",i,":"
    abc_name=raw_input()
    print "Enter Input file name of",abc_name,"plot:"
    abc_elements=raw_input()
    print "If ranking of values is in deacreasing order, Enter \"FALSE\" otherwise \"TRUE\" "
    abc_data_type=raw_input()
    print "Enter the colour name of"
    abc_colour=raw_input()
    if (i==0):
        abc_add="FALSE"
    else:
        abc_add="TRUE"
    A="\nfile<- read.delim(\"",abc_elements,"\", header=TRUE)"
    array_ff[i]=A
    B="\nplot_enrichment_curve(file$x, file$y, add=",abc_add,", decreasing=",abc_data_type,", col=\"",abc_colour,"\")"
    print ''.join(A)
    r_file.write(''.join(A))
    print ''.join(B)
    r_file.write(''.join(B))

    array_gg[i]=B
    k.append(abc_colour)
    print k

    l.append(abc_name)
    print l

    v=1
    h.append(v)
    print h


print array_ff
print "Enter Title"
title=raw_input()

##for j in range(0,n):
##    f=str(array_ff[i])
##    r_file.write(f)
##    r_file.write(str(array_gg[i]))
    
r_file.write("\nlegend(\"bottomrigh\", legend = c(\"ideal\", \"Random\"")
for i in k:
    r_file.write(", \"")
    r_file.write(i)
    r_file.write("\"")
r_file.write(")")


r_file.write(", lty=c(2,3")
for i in h:
    r_file.write(", ")
    r_file.write(str(i))
r_file.write(")")
             

r_file.write(", col=c(\"black\", \"grey\"")
for i in l:
    r_file.write(", \"")
    r_file.write(i)
    r_file.write("\"")
r_file.write(")")
            
r_file.write(", bty=\"n\")")
r_file.write("\ntitle(\"")
r_file.write(title)
r_file.write("\")")
r_file.close()

os.system("R CMD BATCH log.R")


