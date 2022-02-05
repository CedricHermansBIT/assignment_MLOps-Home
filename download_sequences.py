import xml.etree.ElementTree as ET

import requests

keyword = 'PKS'
keyword = 'NRPS'
term = f"txid1883[Organism:exp] AND ({keyword}[All Fields]) AND refseq[filter] AND not partial"
skipfirst = 0
max_seqs = -1
db = "protein"
verbose = True


def esearch(db, term, retstart=0, retmax=200):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term={term}&usehistory=y&retstart={retstart}&retmax={retmax}"
    if verbose:
        print(url)
    r = requests.get(url)
    tree = ET.fromstring(r.text)
    ids = tree.find("IdList")
    return([id.text for id in ids])


def efetch(db, id, rettype="fasta", retmode="text"):
    if type(id) == type(list()):
        id = ','.join(id)
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id={id}&usehistory=y&rettype={rettype}&retmode={retmode}"
    if verbose:
        print(url)
    r = requests.get(url)

    return([seq for seq in r.text.split("\n\n")[:-1]])


if max_seqs == -1:
    max_seqs = 90000000
for i in range(0, max_seqs, 100):
    if verbose:
        print(i)
    try:
        ids = esearch(db=db, term=term, retstart=i+skipfirst, retmax=100)
        if ids == []:
            break
        seqs = efetch(db=db, id=ids)
        # print(seqs)
        for seq in seqs:
            id = seq.split(".")[0][1:]
            with open(f"{keyword}/{id}.fasta", 'w') as ofile:
                ofile.write(seq)
    except Exception as e:
        print(e)
        break
