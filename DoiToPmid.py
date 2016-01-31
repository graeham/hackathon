import requests
import re
import csv

# !"Requesting_Tool" and "Requesting_Email" can be set dynamically
# by moving them to the function 'getPmid'and providing the values
# in the function call

# constants, required by the PubMED API for succesful API calls
utility_root_url = 'http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?&'
requesting_tool = 'paperGraph'
requesting_email = 'kc461@cam.ac.uk'

def get_pmid(target_doi):
    target_doi = target_doi # DOI to be converted; multiple DOIs must be sperated by ','
    

    #request = requests.get('http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=hackcambridge&email=kc461@cam.ac.uk&ids=10.1016/j.ab.2010.04.018&versions=noformat=json')

    request = requests.get(utility_root_url + 'tool=' + requesting_tool + '&' + 'email=' + requesting_email + '&' + 'ids=' + target_doi + '&versions=noformat=json')
    raw_result = request.content.decode('utf-8')
    useful_data = re.search('(?<=pmid=")\w+', raw_result)
    if useful_data is not None:
        return useful_data.group(0)
    else:
        return 'Invalid article id: PubMed does not hold a PMID/PMC for this DOI'


# !Above regex does not deal well with results from multiple
# DOI conversions. Use a loop, calling the get_pmid function
# for each DOI and returning the PMID
list_of_dois = ['10.4161/nucl.2.5.17707','10.4161/nucl.2.5.17707','10.1016/j.devcel.2008.11.011','10.1016/j.devcel.2008.11.011','10.1038/nature11279','10.1016/j.stem.2013.04.013','10.1016/j.stem.2013.04.013','10.1128/AEM.05610-11','10.1186/s13059-015-0745-7','10.1101/gr.169417.113','10.1186/s13059-015-0745-7','10.1101/gr.169417.113','10.1016/j.gde.2008.10.002','10.4161/nucl.28825','10.1038/,10.1016/j.ymeth.2012.04.004','10.1038/nsmb.1936','10.1038/nsmb.1936','10.1007/s10577-010-9167-2','10.1038/ncomms8147','10.1038/ncomms8147','10.1093/nar/gkt1353','10.1038/NMETH.1266','10.1038/NMETH.1266','10.1016/j.tcb.2014.08.010','10.1016/j.tcb.2014.08.010','10.1016/j.cell.2013.02.001','10.1016/j.cell.2013.02.001','10.1186/s13059-015-0730-1','10.1186/s13059-015-0730-1','10.1007/s10577-011-9245-0','10.1093/bib/bbv085','10.1016/j.stem.2014.04.003','10.1016/j.stem.2014.04.003','10.1038/NMETH.2688','10.1038/nature14590','10.1038/nature14590','10.1038/nature','10.1016/j.cell.2012.08.023','10.1016/j.cell.2012.08.023','10.1186/s12867-015-0040-x','10.1186/s12867-015-0040-x','10.1038/nsmb.3066','10.1038/ncomms7178']

# Read input text file containing DOis appending each DOI to an array
#list_of_dois = []



# Get the pmid of each corresponding DOI, if the paper exists in PubMed
# and write each line into a text file
output_file = open('pmids.txt', 'w')

for doi in list_of_dois:
    pmid = str(get_pmid(doi))
    output_file.write(pmid + '\n')
