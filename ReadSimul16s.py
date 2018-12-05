#!/usr/bin/python

import argparse
import sys
import string

parser = argparse.ArgumentParser(description='''Creates simualted sequencing reads given the fasta files of organisms to start with using GPU''', epilog = """Epilog!!!""")
parser.add_argument("fastaFile", type = argparse.FileType('r'), help = "starting fasta file")
parser.add_argument('--rlen', type = int, default = 200, help = 'Length of simulated reads, default is 200')
parser.add_argument('--thput', type = int, default = 7, help = 'Throughput of simulated reads in GBs, default is 7')
parser.add_argument('--qual', type = int, default = 15, help = 'Vverage read quality of simulated reads, default is 15')
parser.add_argument('--output', type = str, default = "reads.fq", help = 'Vverage read quality of simulated reads, default is 15')
#parser.add_argument('onoff', nargs='*', default=[1, 2, 3], help='this thing if in the command does this')
#parser.add_argument('onoff2', nargs='*', default=[1, 2, 3], help='this thing if in the command does this2')
args = parser.parse_args()
multifasta = args.fastaFile.read()
rlen = args.rlen
thput = args.thput
qual = args.qual
output = args.output

def checkiffasta(fasta):#Need to improve this one
    if fasta.startswith(">"):
        return True
    else:
        return False

def subsetfasta(fasta,numLines):#For creating subset input
    fastas = []
    outfile = open("subset-0-" + str(numLines) + ".fasta","w")
    for line in fasta.split(">"):
        if line.count("\n") > 1:
            newline = ">" + line
            fastas.append(newline)
    for line in fastas[:numLines]:
        outfile.write(line)
    outfile.close()

def fixFormatting(fasta):
    

def randomShearing(fasta,readlen,tput,outfile):
    print(len(fasta))

def main():
#    subsetfasta(multifasta,1000) #For subsetting the input

    if checkiffasta(multifasta):
        multifa = fixFormatting(multifasta)
        randomShearing(multifa,rlen,thput,output)
#        print(multifa)
        print("Yes")
        print(rlen)
        print(thput)
        print(qual)
"""

main()
