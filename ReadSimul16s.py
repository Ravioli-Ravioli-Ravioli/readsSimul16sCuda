#!/usr/bin/python

import argparse
import sys
import string
import math
import time
from random import randint
from numba import jit

parser = argparse.ArgumentParser(description='''A program that creates simulated 16S sequencing reads from 16S sequences, utilizing the power of GPUs for creating reads''', epilog = """Not yet ready for research use, for grad class requirements only!""")
parser.add_argument("fastaFile", type = argparse.FileType('r'), help = "starting fasta file")
parser.add_argument('--rlen', type = int, default = 300, help = 'Length of simulated reads, default is 200')
parser.add_argument('--thput', type = int, default = 7, help = 'Throughput of simulated reads in GBs, default is 7')
parser.add_argument('--qual', type = int, default = 15, help = 'Average read quality of simulated reads, default is 15')
parser.add_argument('--overlap', type = int, default = 50, help = 'Overap between R1 and R2')
parser.add_argument('--output', type = str, default = "reads.fq", help = 'Output file name')
args = parser.parse_args()
multifasta = args.fastaFile.read()
rlen = args.rlen
thput = args.thput
qual = args.qual
overlap = args.overlap
output = args.output

def checkiffasta(fasta): #Need to improve this one, just checks if fasta or not
    if fasta.startswith(">"):
        return True
    else:
        return False

def subsetfasta(fasta,numLines): #For creating subset input, independent from the actual program
    fastas = []
    outfile = open("subset-0-" + str(numLines) + ".fasta","w")
    for line in fasta.split(">"):
        if line.count("\n") > 1:
            newline = ">" + line
            fastas.append(newline)
    for line in fastas[:numLines]:
        outfile.write(line)
    outfile.close()

def fixFormatting(fasta): #Fixes double greater than sign from headers in a fasta file
    fastas = []
    for line in fasta.split(">"):
        if line.count("\n") > 1:
            newline = ">" + line
            fastas.append(newline)
    return fastas

#@jit
def fandri(seqlen,rlen,overlap):
    ampSize = ((rlen - overlap)*2) + overlap
    seedStart = randint(0, seqlen - ampSize)
    fstart = seedStart
    fend = seedStart + rlen
    rstart = fend - overlap
    rend = rstart + rlen
    return [fstart, fend, rstart, rend]

def create():
    print("yes")

def createReads(fasta,readlen,tput,outfile,over): #Returns a list containing list containing forward and reverse sequences randomly generated
    fnrs = []
    pairStats = []
    numOrg = len(fasta)
#    numReadPairs = math.ceil(((tput * 1000000000)/readlen)/2) #1B
#    numReadPairs = math.ceil(((tput * 100000000)/readlen)/2) #100M
#    numReadPairs = math.ceil(((tput * 10000000)/readlen)/2) #10M
    numReadPairs = math.ceil(((tput * 1000000)/readlen)/2) #1M
#    numReadPairs = math.ceil(((tput * 100000)/readlen)/2) #100K
#    numReadPairs = math.ceil(((tput * 10000)/readlen)/2) #10K
#    numReadPairs = math.ceil(((tput * 1000)/readlen)/2) #1K
    pairsPerOrg = math.ceil(numReadPairs/numOrg)
    for seq in fasta:
        headless = ''.join(seq.split("\n")[1:])
        seqlen = len(headless)
        if seqlen >= (readlen*2):
            for i in range(0, pairsPerOrg): 
                pairStats.append(fandri(seqlen,readlen,over))
    print(len(pairStats))

def main():
    if checkiffasta(multifasta):
        multifa = fixFormatting(multifasta)
        r1r2s = createReads(multifa,rlen,thput,output,overlap)
        #    subsetfasta(multifasta,1000) #For subsetting the input

start_time = time.time()
main()
end_time = (time.time() - start_time)
print("--- %s seconds ---" % end_time)
