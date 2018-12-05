#!/usr/bin/python

import argparse
import sys
import string
import math
import time
from random import randint

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

def fandr(seq,rlen,overlap): #Does the randomization, outputs f and r, called by createReads
    ampSize = ((rlen - overlap) * 2) + overlap
    headless = ''.join(seq.split("\n")[1:])
    if len(headless) >= ampSize + overlap:
        seedStart = randint(0, len(headless) - ampSize)
        amp = headless[seedStart:seedStart + ampSize]
        forward = amp[0:rlen]
        reverse = amp[rlen - overlap:]
        return [forward, reverse]
    else:
        pass

def createReads(fasta,readlen,tput,outfile,over): #Returns a list containing list containing forward and reverse sequences randomly generated
    allSeqs = []
    fnrs = []
    numOrg = len(fasta)
#    numReads = (tput * 1000000000)/readlen
    numReads = (tput * 1000000000)/readlen #For debugging
    numSeeds = math.ceil(numReads/2)
    rpairsPerOrg = numSeeds/numOrg
    for seq in fasta:
        allSeqs += int(rpairsPerOrg) * [seq]
    counter = 0 #For debugging
    for seq in allSeqs:
        counter += 1
        print("Run completion: {0:.2f} percent.".format((float(counter)/len(allSeqs))*100))
        fnr = fandr(seq,readlen,over)
        fnrs.append(fnr)
    return fnrs

def main():
    if checkiffasta(multifasta):
        multifa = fixFormatting(multifasta)
        r1r2s = createReads(multifa,rlen,thput,output,overlap)
        #    subsetfasta(multifasta,1000) #For subsetting the input

start_time = time.time()
main()
end_time = (time.time() - start_time)
print("--- %s seconds ---" % end_time)
