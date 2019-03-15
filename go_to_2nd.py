#! bin/src/env python3
from collections import Counter
import os
import csv
import requests, sys, getopt
import json
import re

# function retrieve GOnumber ('GO:0034219') from GOterm ('transmembrane transport')
# parameters: go_term (str)
# return go_number (str)
def get_GOterm_to_GOnumber(go_term):
    quickgo_url="https://www.ebi.ac.uk/QuickGO/services/ontology/go/search?query="\
                +go_term+\
                "&limit=25&page=1"
    req = requests.get(quickgo_url, headers={ "Accept" : "application/json"})
    try:
        page1 = req
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"

    if not req.ok:
        req.raise_for_status()
        sys.exit()
    json_data = json.loads(req.text)
    for jdata in json_data["results"]:
        go_number = str(jdata["id"])
    return go_number


# function: get a list of ancestors GO (['GO:1902494', 'GO:1902495',..., 'GO:0071944'])
#           given a GOnumber ('GO:0043190') using EMBL-EBI's QuickGO browser
# parameter: go_number (str)[a valid Gene Ontology ID, e.g. GO:0048527]
# return: all ancestors (list)
def get_ancestors(go_number):
	number=go_number[3:] # to remove "GO:" and use only the number
	quickgo_url='https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/GO%3A'\
	            +number+\
	            '/ancestors?relations=is_a%2Cpart_of%2Coccurs_in%2Cregulates'
	req = requests.get(quickgo_url, headers={ "Accept" : "application/json"})
	if not req.ok:
		req.raise_for_status()
		sys.exit()
	json_data = json.loads(req.text)

	go_ancestors = []
	for k_jdata,v_jdata in json_data.items():
		if k_jdata == "results":
			for v_jd in v_jdata:
				for k_dic,v_dic in v_jd.items():
					if k_dic == "ancestors":
						for go in v_dic:
							go_ancestors.append(go)
	return go_ancestors

# function: make a dictionary from a data
# parameter : csv file with two colums: GO,description (csv file)
# return: dictionary (dict)
def building_dic(data_to_dic):
	dict_2nd = {}
	with open(data_to_dic, "r") as my_dict:
	    readrows = csv.reader(my_dict,delimiter=",")
	    for row in readrows:
	        k,v = row[0],row[1]
	        dict_2nd[k]=v
	return dict_2nd

# function: find the GOs in raw data (output of the program GO)
# parameter: raw string that contain GOs, example: 'F:GO:0003924; C:GO:0005840'
# return: list of GOnumbers
def findall_GOs(string):
    raw_string_gos = re.findall('GO:(\d+)',string)
    list_go_numbers =[]
    for go in raw_string_gos:
        go_find = 'GO:'+go
        list_go_numbers.append(go_find)
    return list_go_numbers


# function: find the term GOs in raw data (output of the program GO)
# input : string that contein GO terms. example.: 'P:transmembrane transport; P:deoxyribonucleoside monophosphate biosynthetic process; P:transport'
def findall_terms(string):
	raw_string_terms = string.split(";")
	list_terms =[]
	for i in raw_string_terms:
		term = re.findall(':\s*([^.]+|\S+)',i)
		for t in term:
			list_terms.append(t)
	return list_terms


#############################################################################################

txt_input = sys.argv[1]
if os.path.isfile(txt_input):
	if txt_input.endswith('txt'):
		print("--> working in ",txt_input)
		csv_output= txt_input[:-4]+'_out.csv'
	else:
		print('This file (',txt_input,') is not txt file! Review your file')
		sys.exit()
else:
	print('The file ',txt_input,'not exists')
	sys.exit()

#step_0 : Finding the columns with GOnumbers or GOterms
print('### FINDING THE COLUMNS WITH GOnumbers and/or GOterms ###')
# to identify the headers that contain the GOnumbers we will use regular expressions
# and they will be store in:
headers_GOs = []
# to indetify the header that contain the GOterm we will use this list
# and tehy will be store in:
posibles_headers = ['GO Names list','GO Names','Annotation GO Term','InterPro GO Term','InterPro GO Names']
headers_terms = []
with open(txt_input,'r') as my_data:
	#making dictionary with all raw data
	readrows = csv.DictReader(my_data,delimiter='\t',skipinitialspace=True)
	data = {name:[] for name in readrows.fieldnames}
	for row in readrows:
		for header in readrows.fieldnames:
			data[header].append(row[header])
	
	for head, rows in data.items():
		if len(head) != 0 and len(rows) != 0:
			for r in rows:
				regex_GO = re.findall('.*GO:.*',r)				
				if regex_GO:
					headers_GOs.append(head)
				else:
					if head in posibles_headers:
						headers_terms.append(head)

headers_GOnumber_GO_term = [list(set(headers_GOs)),list(set(headers_terms))]
headers_GOnumber_GO_term = [l for l in headers_GOnumber_GO_term if l != []] # Removing the empty lists

number_col = []
if len(headers_GOnumber_GO_term) == 0:
	print("It was not possible to find any column with GOnumber or GOterms")
	sys.exit()
else:
	if len(headers_GOnumber_GO_term) == 2:
		columns_selected = headers_GOnumber_GO_term[0] #chose the GOnumber colums
		print('This file contain GO codes in:')
		key_list = list(data)
		keys_of_interest = headers_GOnumber_GO_term[0]
		for key in keys_of_interest:
			number_col.append(key_list.index(key))
		number_col.insert(0,'GO codes')
		for n in sorted(number_col[1:]):
			print("Column ",n)
	if len(headers_GOnumber_GO_term) == 1:
		columns_selected = headers_GOnumber_GO_term[0]
		print('This file contain GO terms in:')
		key_list = list(data)
		keys_of_interest = headers_GOnumber_GO_term[0]
		for key in keys_of_interest:
			number_col.append(key_list.index(key))
		number_col.insert(0,'GO terms')
		for n in  sorted(number_col[1:]):
			print("Column ",n)

key_list = list(data)
for n,i in enumerate(key_list):
	if i == 'SeqName':
		SeqName_column = n

#step_1: geting all GOs_IDs
#        or getting GO_IDs from GO_terms
print("#### MAKING A LIST WITH UNIQUES GOs OF THE ROW DATA ###")

list_GO = []
no_retrieve = []
no_InterPro = []
with open(txt_input,'r') as my_data:
    readrows = csv.reader(my_data,delimiter='\t')
    for rw in readrows:
    	if number_col[0] == 'GO codes':
    		column = sorted(number_col[1:])
	    	regex = re.findall('GO:',rw[column[0]])
	    	if regex:
	    		GOs_retrieve = findall_GOs(rw[column[0]])
	    		for i in GOs_retrieve:
	    			list_GO.append(i)
	    	else:
	    		if len(column) == 2:
		    		no_retrieve.append(rw[SeqName_column])
		    		GOs_retrieve = findall_GOs(rw[column[1]])
		    		if len(GOs_retrieve)!=0:
		    			for i in GOs_retrieve:
		    				list_GO.append(i)
		    		else:
		    			no_InterPro.append(rw[SeqName_column])

with open(txt_input,'r') as my_data:
    readrows = csv.reader(my_data,delimiter='\t')
    for rw in readrows:
    	if number_col[0] == 'GO terms':
    		column = sorted(number_col[1:])
    		list_term  = []
    		rows_string = str(rw[column[0]])
    		term_retrieve = findall_terms(rows_string)
    		if len(term_retrieve) != 0:
    			for tr in term_retrieve:
    				list_term.append(tr)
    		else:
    			if len(column) == 2:
    				no_retrieve.append(rw[SeqName_column])
    				rows_string = str(rw[column[1]])
    				term_retrieve = findall_terms(rows_string)
    				if len(term_retrieve) != 0:
    					for tr in term_retrieve:
    						list_term.append(tr)
    				else:
    					no_InterPro.append(rw[SeqName_column])

    		for my_term in list_term:
    			my_request = get_GOterm_to_GOnumber(my_term)
    			list_GO.append(my_request)

print("SeqName without principal GO IDs found:")
if len(no_retrieve[1:]) != 0:
	for n in no_retrieve[1:]:
		print(n)
else:
	print("0")
print("\nTrying to find in InterPro ...")
print("SeqName without InterPro GO IDs found:")

if len(no_InterPro[1:]) != 0:
	for n in no_InterPro[1:]:
		print(n)
else:
	print("0")

lista_GO_uniques_pre = set(list_GO)

#step_2: building a dic and buildind a list of GO ids
print("#### BUILDING A DICTIONARY 2ND LEVEL ###")
my_dic_2nd_nivel = building_dic("dictionary_2_level.csv")
list_GOs_dic = []
for k,v in my_dic_2nd_nivel.items():
	list_GOs_dic.append(k)

print("#### GETING ANCESTOR TO EACH GO ###")
lista_GO_uniques_no_retrieve_ancestral = []
lista_GO_uniques =[]
for _GO in lista_GO_uniques_pre:
	if _GO in list_GOs_dic:
		lista_GO_uniques_no_retrieve_ancestral.append(_GO)
	else:
		lista_GO_uniques.append(_GO)

lista_term_uniques_no_retrieve_ancestral = []
for i in lista_GO_uniques_no_retrieve_ancestral:
	for k,v in my_dic_2nd_nivel.items():
		if i == k:
			lista_term_uniques_no_retrieve_ancestral.append(v)

print("GOs with existing 2nd-level ancestors:")
for n in lista_GO_uniques_no_retrieve_ancestral:
	print(n)

#step_3: geting ancestors and filtering with the before lis of the dic
my_GO_and_term_ancest_selected = {}
for my_GOs in lista_GO_uniques:
	list_all_ancestors = get_ancestors(my_GOs)
	list_selected_GO_ancestors = []
	for GO_ancest in list_all_ancestors:
		if GO_ancest in list_GOs_dic:
			list_selected_GO_ancestors.append(GO_ancest)

	#step 4: retrieving the term from the selected GO id
	list_selected_GOterm_ancestors = []
	for selected_GO_ancestor in list_selected_GO_ancestors:
		for k,v in my_dic_2nd_nivel.items():
			if selected_GO_ancestor == k:
				list_selected_GOterm_ancestors.append(v)
	my_GO_and_term_ancest_selected[my_GOs]=list_selected_GOterm_ancestors

#step_3: geting a list with all terms
all_terms_pre = []
for k,v in my_GO_and_term_ancest_selected.items():
    for i in v:
        all_terms_pre.append(i)
all_terms = all_terms_pre + lista_term_uniques_no_retrieve_ancestral

#step_4: counting the frecuency of the terms and writing in a csv file
print("#### COUNTING THE FRECUENCY OF THE TERMS AND WRITING THE RESULTS ###")
with open(csv_output,"w") as my_out:
	writerow = csv.writer(my_out,delimiter=',')
	list_terms_freq = []
	for terms,freq in Counter(all_terms).items():
		terms_freq = [terms,freq]
		list_terms_freq.append(terms_freq)
	writerow.writerows(list_terms_freq)

print("#### FINALIZED ###","\nCheck the file ",csv_output)