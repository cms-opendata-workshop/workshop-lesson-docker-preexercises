import ROOT

import sys

topdir = "root://eospublic.cern.ch//eos/opendata/cms/"

print("To list the contents of any subdirectories of\n")
print("{0}\n".format(topdir))
print("just add them to the commandline options.\n")
print("Example: ")
print("python list_contents_of_directories.py")
print("python list_contents_of_directories.py Run2011A")
print("python list_contents_of_directories.py Run2011A/SingleMu")
print("\n")


if len(sys.argv)>1:
    topdir += sys.argv[1]

dire = ROOT.TSystemDirectory(topdir,topdir)

# TList object
files = dire.GetListOfFiles()

# For debugging
#files.Print()

print("--------------------------------")
print("Listing the contents of\n")
print(topdir)
print("-------\n")

# For debugging
#print(len(files))

for f in files:
    print(f.GetName())



