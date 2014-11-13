
===================================
README of extract_bib python script
===================================
This script is extremely simple willingly. Its only goal is to extract all the 
*Bibtex* bibliographic references that are cited in a given *Latex* text file. 

It is used to create a *Bibtex* database that contains only the references cited 
in the given *Latex* file. This can be useful, for example, when submitting a paper
to create the *.bib* file needed for the submission. 

1. Install
==========

The goal of the script is to bee easy to install and use, therefore the only 
prerequisite is **python 2.7**. 

Simply clone the repository (or copy the script) on your computer, and add the 
folder to your PATH environment variable. Linux users may need to add execution 
priviledges using `chmod +x extract_bib.py`


2. How to use  it
=================
To use it you need:


- one *Bibtex* file with all your references. Important: the references entries must end with a line containing only the *}* character that closes the entry. This is normally the case if you use e.g. *Jabref* to manage your citations.
- one *Latex* file. Use standard *natbib* commands, if you need custom commands, you will need to add them to the *BIBTEXCOMMANDLIST* global variable at the beginning of the script.


Then run *extract_bib.py LatexFile BibtexFile* in a command line replacing *LatexFile*
with your *Latex* text file path and *BibtexFile* with your bibliographic file path. 

If all the references cited in *LatexFile* are found in *BibtexFile*, 
the script outputs the subset to *stdout*. To create a file, just redirect 
the output to a file using **">"** like this:

*extract_bib.py LatexFile BibtexFile > newBibtexFile* 

If some references are not found, the script will report an error and end. This is 
useful to find the missing references from a *Bibtex* database for example.

3. Issues and compatibility
===========================

- this script is written for python 2.7, it may work for some earlier releases, but it **is not compatible with python 3**
- there may be errors if you use particular character encodings for you files, this has not been tested. It has been tested on UTF-8 encoding files sucessfully.
- if your Bibtex entries are not ended with a line containing only "}" the script reports an error.  


4. License
==========

This script is released under the WTFPL_v2. See the file LICENSE for details.
