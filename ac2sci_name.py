#!/bin/py
# Get the gene symbols according to the accession from gene2accession database.
# Usage:
#       python ac2taxid.py ac2taxid_dbfile accession_file ac2sci_name_file
#       eg. python ac2taxid.py ac2taxid.db all_viral_accession.txt all_viral_ac2sci_name.txt

import re
import sqlite3
import datetime
import string
import sys

dbfile = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]


print "connecting gene2accession database..."
conn = sqlite3.connect(dbfile)
c = conn.cursor()
print "OK!"

print datetime.datetime.now().time().isoformat()
facc = open(infile, 'rU')
accessions = []

print "Load accessions..."
for line in facc:
    ac = re.split('\.', line.rstrip())[0]
    accessions.append(ac)

AC_s = tuple(accessions)

print len(AC_s), "AC_s loaded."
all_taxids = []
for i in range(0, len(AC_s)/8000):
    start = i*8000
    end = (i+1)*8000
    if end > len(AC_s):
        end = len(AC_s)
    tmp_acs = AC_s[start:end]
    c.execute("""select accession,taxid from pr_ac2taxid where accession in
            ({0})""".format(','.join('?' for _ in tmp_acs)),tmp_acs)
    tmp_taxid = c.fetchall()
    all_taxids.extend(tmp_taxid)

print "Finish searching the ac2taxid database."
print len(all_taxids), "searched items."

print "Construct a dictionary of searched results."
sch_dict = {}
for each in all_taxids:
    sch_dict[each[0]] = each[1]

#-----------------------------------------------------------------------#
# prepare nodes and names database
print 'Loading nodes database....'
node={}
f=open('nodes.dmp','r')
for line in f:
    temp=re.split('\t\|\t',line)
    node[temp[0]] = temp[1]
f.close()

print 'Loading merged nodes database...'
merged = {}
f = open('merged.dmp','r')
for line in f:
    temp=re.split('\t\|\t',line.rstrip())
    merged[temp[0]] = temp[1]
f.close()

print 'Loading names database....'
name={}
f=open('names.dmp','r')
for line in f:
    temp=re.split('\t\|\t',line)
    ptemp=re.split('\|',temp[3])
    p2temp=ptemp[0].rstrip()
    if p2temp=='scientific name':
        name[temp[0]] = temp[1]
f.close()

#----------------------------------------------------------------------#

sci_name = {}
print "Get scientific names of species and genus according to taxid."
for acc in AC_s:
    if acc not in sch_dict.keys():
        sci_name[acc] = ("--","--")
    else:
        if acc not in sci_name.keys():
            tid = sch_dict[acc]
            if tid in merged.keys():
                tid = merged[tid]
            if tid in node.keys():
                pid = node[tid]
            else:
                pid = False
            if tid in name.keys():
                sp_name = name[tid]
            else:
                sp_name = "--"
            if not pid:
                ge_name = "--"
            else:
                if pid in name.keys():
                    ge_name = name[pid]
                else:
                    ge_name = "--"
            sci_name[acc] = (sp_name, ge_name)

facc.close()
c.close()
conn.close()
print "Finish searching."

print datetime.datetime.now().time().isoformat()
print "Writing the results..."
fout = open(outfile, 'w')
fout.write("accession\t|\tspecies\t|\tgenus\n")
for each in sorted(sci_name.keys()):
    fout.write(each+'\t|\t'+'\t|\t'.join(sci_name[each])+'\n')
fout.close()
print "Finished."

