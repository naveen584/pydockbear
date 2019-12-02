# Mayank #

import sys

def main():
	
	string1=sys.argv[1]
	string2=sys.argv[2]
	string3=sys.argv[3]
	string4=sys.argv[4]
	file_input = open("conf.txt", "w+")	##  creating output file (the file name conf.txt) and opening it in write mode 
	file_input.write("receptor = ")		##  writting to the file name conf.txt 
	file_input.write(string1)
	file_input.write("\nligand = l.pdbqt\n\ncenter_x = 0\ncenter_y = 0\ncenter_z = 0\n\nsize_x = ")
	file_input.write(string2)
	file_input.write("\nsize_y = ")
	file_input.write(string3)
	file_input.write("\nsize_z = ")
	file_input.write(string4)
	file_input.write("\n\nexhaustiveness = 32")
	file_input.close()

if ( __name__=="__main__" ):
	main()



