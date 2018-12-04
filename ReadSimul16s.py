#!/usr/bin/python

import argparse
import sys
import string

parser=argparse.ArgumentParser(description='''Creates simualted sequencing reads given the fasta files of organisms to start with using GPU''', epilog="""Epilog!!!""")
parser.add_argument("fastaFile", type=argparse.FileType('r'), help="starting fasta file")
parser.add_argument('--rlen', type=int, default=200, help='Desired length of simulated reads')
parser.add_argument('--thput', type=int, default=7, help='Desired throughput in GBs')
parser.add_argument('--qual', type=int, default=20, help='Desired average read quality')
#parser.add_argument('onoff', nargs='*', default=[1, 2, 3], help='this thing if in the command does this')
#parser.add_argument('onoff2', nargs='*', default=[1, 2, 3], help='this thing if in the command does this2')
args=parser.parse_args()
multifasta=args.fastaFile.read()

def checkiffasta(fasta):#Need to improve this one
    if fasta.startswith(">"):
        return True
    else:
        return False

def subsetfasta(fasta,numLines):#For creating subste input
    outfile = open("subset-0-" + str(numLines), "w")
    gsplit = fasta.split(">")[1:]
    fastas = []
    for i in range(0, len(gsplit) - 1):
        if gsplit[i].count("\n") > 1:
            fastas.append(">" + gsplit[i])
        else:
            fastas.append(">" + gsplit[i] + gsplit[i+1])
    for fast in fastas[:numLines + 1]:
        outfile.write(fast)
    outfile.close()

def main():
#    subsetfasta(multifasta,4)
#    if checkiffasta(multifasta):
#        print("Yes")


main()
