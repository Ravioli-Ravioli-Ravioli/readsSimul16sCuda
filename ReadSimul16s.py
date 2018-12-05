#!/usr/bin/python

import argparse
import sys
import string
import math
import time
from random import randint

parser = argparse.ArgumentParser(description='''Creates simualted sequencing reads given the fasta files of organisms to start with using GPU''', epilog = """Epilog!!!""")
parser.add_argument("fastaFile", type = argparse.FileType('r'), help = "starting fasta file")
parser.add_argument('--rlen', type = int, default = 300, help = 'Length of simulated reads, default is 200')
parser.add_argument('--thput', type = int, default = 7, help = 'Throughput of simulated reads in GBs, default is 7')
parser.add_argument('--qual', type = int, default = 15, help = 'Average read quality of simulated reads, default is 15')
parser.add_argument('--overlap', type = int, default = 50, help = 'Overap between R1 and R2')
parser.add_argument('--output', type = str, default = "reads.fq", help = 'Output file name')
#parser.add_argument('onoff', nargs='*', default=[1, 2, 3], help='this thing if in the command does this')
#parser.add_argument('onoff2', nargs='*', default=[1, 2, 3], help='this thing if in the command does this2')
args = parser.parse_args()
multifasta = args.fastaFile.read()
rlen = args.rlen
thput = args.thput
qual = args.qual
overlap = args.overlap
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
    fastas = []
    for line in fasta.split(">"):
        if line.count("\n") > 1:
            newline = ">" + line
            fastas.append(newline)
    return fastas

def seqRand(seq,rlen,overlap):
    ampSize = (rlen - overlap) * 2
    headless = ''.join(seq.split("\n")[1:])
    seedStart = randint(0, len(headless) - ampSize)
    amp = headless[seedStart:seedStart + ampSize]
    forward = amp[0:rlen]
    reverse = amp[-rlen:]
    if len(amp) == 500:
        print("Forward {0}".format(len(forward)))
        print("Reverse {0}".format(len(reverse)))

def randomShearing(fasta,readlen,tput,outfile,over):
    allSeqs = []
    numOrg = len(fasta)
    numReads = (tput * 1000000000)/readlen
    numSeeds = math.ceil(numReads/2)
    rpairsPerOrg = numSeeds/numOrg
    for seq in fasta:
        allSeqs += int(rpairsPerOrg) * [seq]
    for seq in allSeqs:
        seqRand(seq,readlen,over)


def main():
#    subsetfasta(multifasta,1000) #For subsetting the input

    if checkiffasta(multifasta):
        multifa = fixFormatting(multifasta)
        randomShearing(multifa,rlen,thput,output,overlap)

start_time = time.time()
main()
end_time = (time.time() - start_time)
print("--- %s seconds ---" % end_time)
