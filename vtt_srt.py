import os, re, sys
from stat import *


def convertContent(fileContents):

	replacement = re.sub(r'([\d]+)\.([\d]+)', r'\1,\2', fileContents)
	replacement = re.sub(r'WEBVTT\n\n', '', replacement)
	replacement = re.sub(r'^\d+\n', '', replacement)
	replacement = re.sub(r'\n\d+\n', '\n', replacement)

	return replacement
	


def fileCreate(strNamaFile, strData):
	#--------------------------------
	# fileCreate(strNamaFile, strData)
	# create a text file
	#
	try:
	
		f = open(strNamaFile, "w")
		f.writelines(str(strData))
		f.close()
	
	except IOError:
	
		strNamaFile = strNamaFile.split(os.sep)[-1]
		f = open(strNamaFile, "w")
		f.writelines(str(strData))
		f.close()
		
	print("file created: " + strNamaFile + "\n")
	
	
	
def readTextFile(strNamaFile):

	f = open(strNamaFile, "r")
	print("file being read: " + strNamaFile + "\n")
	return f.read().decode("windows-1252").encode('ascii', 'ignore')


def vtt_to_srt(strNamaFile):

	fileContents = readTextFile(strNamaFile)
	
	strData = ""
	
	strData = strData + convertContent(fileContents)
	
	strNamaFile = strNamaFile.replace(".vtt",".srt")
  
	print(strNamaFile)
	fileCreate(strNamaFile, strData)
	
	
	
def walktree(TopMostPath, callback):

    '''recursively descend the directory tree rooted at TopMostPath,
       calling the callback function for each regular file'''

    for f in os.listdir(TopMostPath):
	
        pathname = os.path.join(TopMostPath, f)
        mode = os.stat(pathname)[ST_MODE]
		
        if S_ISDIR(mode):
		
            # It's a directory, recurse into it
            walktree(pathname, callback)
			
        elif S_ISREG(mode):
		
            # It's a file, call the callback function
            callback(pathname)
			
        else:
		
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

			

def convertVTTtoSRT(file):
	
	if '.vtt' in file:
	
		vtt_to_srt(file)
		
def main():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  TopMostPath = dir_path
  walktree(TopMostPath, convertVTTtoSRT)
	
main()	