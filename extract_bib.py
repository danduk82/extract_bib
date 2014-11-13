#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script parses one :term:`latex` text file and a :term:`bibtex` bibliography 
file and returns a :term:`bibtex` bibliography  string on the ``stdout``. This 
string contains the bibliography subset with only the references that are cited
in the input :term:`latex` file.

I know there are already other tools to do that, but I had a few dependencies 
problems with my laptop, so I decided to write "yet anoter one" of them... This 
script is willingly kept extremely simple, so that it may not suit all the complex
cases, but at least it should work with most of normal cases. 

Created on:
Wed Nov 12 16:42:29 2014
Author: 
Andrea Borghi, laboratoire GeoRessources, ENSG Nancy
License:
WTFPL v2 (http://www.wtfpl.net/about)
"""

import sys,re,os

VERSION='0.1'

BIBTEXCOMMANDLIST=(r'\citet',r'\citep',
                   r'\citet\*',r'\citep\*',
                   r'\citeauthor',r'\citeauthor\*',
                   r'\citeyear',r'\citeyearpar',
                   r'\citealt',r'\citealp',r'\citetext')

FORBIDDENTYPES=('comment','COMMENT')
       
def parseCitationList(str2parse,occurList,commandName):
    """
    Parses one citation list that has been identified by ``parseTexDocument`` 
    and returns a list containing the :term:`bibtex` keys.
    """
    outStrList=[]
    for occurence in occurList:
        startIndex=occurence+len(commandName)-1
        while True:
            if str2parse[startIndex] == '{':
                startIndex+=1
                break
            startIndex+=1
        stopIndex=startIndex
        while True:
            if str2parse[stopIndex] == '}':
                break
            stopIndex+=1
        treadedStrings = str2parse[startIndex:stopIndex].split(',')
        for key in treadedStrings:
            outStrList.append(key.strip())
    return outStrList
    

def parseTexDocument(texFile):
    """
    Parses a :term:`latex` file and returns a sorted list of all the :term:`bibtex`
    keys that where found. It uses ``BIBTEXCOMMANDLIST`` global variable to identify
    the citations whitin the text file.
    """
    bibKeys=[]    
    with open(texFile,'r') as nFile:
        fileText=''.join(nFile.readlines())
        for currComm in BIBTEXCOMMANDLIST:
            listOfOccurences=[occur.start() for occur in re.finditer(currComm, fileText)]
            bibKeys = bibKeys + parseCitationList(fileText,listOfOccurences,currComm)
    bibKeys=list(set(bibKeys))
    return sorted(bibKeys)
    

def addEntryToDict(bibFile,rdln):
    """
    Parses a :term:`bibtex` file from an initial line (found earlier) which contains
    the type of entry. Then it fills a list with all the lines that correspond to 
    that entry. In practic the result is equivalent to the ``file.readlines()`` 
    output.
    """
    tmp=[]
    tmp.append(rdln)
    # small counter that allows to exit from an infinite loop if the file does
    # not contain a line containing only '}', this raises an error
    c=0
    while True:
        rdln = bibFile.readline()
        tmp.append(rdln)
        if rdln == '}\n':
            break
        else:
            c+=1
        if c>1000:
            raise ValueError('error: did not find a line with only "}" to close a record. This appened at flag "%s"' % tmp[0])
    return tmp

def createBiblioStr(bibDict):
    """
    Returns one unique string from the bibliographic dictionnary. This correspond
    to the output of the script.
    """
    outStr=''
    for key in sorted(bibDict.keys(),key=str.lower):
        outStr=outStr + ''.join(bibDict[key.strip()]) + '\n'
    return outStr

def createBiblioDict(bibFileName):
    """
    Returns a dictionnary containing all the bibliographic entries from a given 
    :term:`bibtex` file. The :term:`key` of the dictionnary is the bibliographic key 
    that is used in the ``\cite*`` commands, and the :term:`value` corresonding to
    each :term:`key` is a list of all the text lines corresponding to that field
    in the source :term:`.bib` file.
    
    The list of available ``\cite*`` commands is in the ``BIBTEXCOMMANDLIST`` global
    variable. Just edit it if you need more commands (e.g. ``\citeauthor*``)
    """
    bibDict={}
    with open(bibFileName,'r') as bibFile:
        while True:
            rdln = bibFile.readline()
            if(len(rdln) == 0):
                # End of file
                break 
            elif rdln[0] == '@':
                # check if it is a comment (jabref!!) or another useles flag
                try:
                    for forbidden in FORBIDDENTYPES:
                        if rdln[1:len(forbidden)+1] == forbidden:
                            raise ValueError('forbidden : %s' % forbidden)
                except ValueError:
                    continue
                keyword=''.join(rdln.split("{")[-1]).rstrip()[:-1]
                bibDict[keyword]=addEntryToDict(bibFile,rdln)
    return bibDict

def usage():
    """display an help string"""
    print "%s version %s\nusage: %s <texFile> <bibFile>" % (os.path.basename(__file__),VERSION,os.path.basename(__file__))
    
def errorOnExecution(message):
    print "The program ended with the following error:\n%s" % message
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit(0)
    # not checking the correctness of the input files types. The user is supposed 
    # to be smart enough...
    texFileName=sys.argv[1]
    bibFileName=sys.argv[2]
    try:
        bibDatabase=createBiblioDict(bibFileName)
        bibKeys2search=parseTexDocument(texFileName)
 
        bibEntry={}
        for key in bibKeys2search:
            if bibDatabase.has_key(key):
                bibEntry[key]=bibDatabase[key]
            else: 
                raise ValueError('critical error: citation "%s" not found' % key )
    except ValueError,err:
        errorOnExecution(err.message)        
        exit(1)
    except IOError,err:
        errorOnExecution(err.strerror)
        print '"%s"' % err.filename
        exit(2)
       
    print createBiblioStr(bibEntry)