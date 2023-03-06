#!/Users/erin/opt/miniconda3/envs/DS_pub/bin/python
'''
MODULE DOCSTRING
'''
import glob
import os
import pandas as pd


def grab_cbio_data(raw_data_loc):
    ''' This function accepts a file path containing a cBioPortal dataset
    and organizes it into a dictionary of dictionaries.
    Each outer dictionary is the data "category" (clinical data, metadata, and patient case_lists).
    Each inner dictionary contains a Pandas dataframe.
    Arguments:
        raw_data_loc (str): the file path of the folder containing the downloaded cBio Dataset

    Returns:
        raw_data_dict: a dictionary of dictionaries   '''

    files = glob.glob(raw_data_loc+"/*") #grabs all subdirs and files
    #(mostly .txt files but there is one .seg file that can be read by a text editor)
    raw_data_dict = {}

    for f in files:
        #if the element is a subdir, then use os.listdir to
        #list the files inside that subdir, iterate through, and process
        if os.path.isdir(f):
            subfiles = os.listdir(f)
            subdata = {}
            #for each file in the subdir, create the necessary keys,
            #read in data with Pandas, and organize into subdict
            #example value for subf: cases_sv.txt --> key1 becomes "cases", key2 becomes "sv"
            #loc is the full file path
            #("/Users/erin/Downloads/220215_msk_met_2021/case_lists/cases_sv.txt")
            for subf in subfiles:
                key1 = subf.split('_')[0]
                key2 = subf.split('_')[-1].split('.')[0]
                loc = os.path.join(f,subf)
                table = pd.read_csv(loc,header=None,low_memory=False)
                #read in the sv.txt file into a dict called subdata with sv as key2
                subdata[key2] = table
            #organize that subdict into the parent dict which is raw_data_dict['cases']
            raw_data_dict[key1] = subdata
        #if the element is a file, no further iteration necessary. Ignore readme.txt and LICENSE
        elif os.path.isfile(f) and 'readme' not in f.lower() and 'license' not in f.lower():
            #example value for f: /Users/erin/Downloads/220215_msk_met_2021/meta_cna.txt
            #--> key1 becomes "meta", key2 becomes "cna",
            key1 = os.path.basename(f).split('_')[0] #
            key2 = os.path.basename(f).split('_')[-1].split('.')[0]
            #'comment=#' skips lines starting with #, which is helpful for the metadata files
            table = pd.read_table(f,comment='#',header='infer',low_memory=False)
            #if this is a new key, create an empty inner dictionary
            if key1 not in raw_data_dict.keys():
                raw_data_dict[key1] = {}
            #if we've already seen this outer key, then add the inner key and dataframe
            else:
                raw_data_dict[key1][key2] = table
    return raw_data_dict

def report_cbio_data_ingest(raw_data_dict):
    ''' This function accepts a raw_data_dict and prints out
    how much data was scraped successfully.
    Sorts by data categories (clinical data, metadata, case data, etc.),
    reports shape of each inner
    dataframe.

    Arguments:
        raw_data_dict (dict): a dictionary of dictionaries of Pandas dataframes

    Returns:
        nothing, produces a print-out   '''

    print("DATA INGEST REPORT")
    for k,v in raw_data_dict.items():
        print("*" * 20)
        print(f"DATA CATEGORY: {k}")
        print(' ' * 2, f"VALUES: {len(v)}")
        for k2,v2 in v.items():
            print(' ' * 4, k2, v2.shape)

def reorg_cbio_meta_data(raw_dict):
    ''' This function accepts a raw_data_dict of cBioPortal data,
    reorganizes it for ease of use, and returns the reorganized dataframes.
    The processed dict allows dynamic grabbing of attributes via .loc
    (example: processed_data_dict['meta']['sv'].loc['data_filename']['Value']
    returns ' data_sv.txt').

    Here is an example:
    raw_data_dict['meta']['sv'] (original DF):
    cancer_study_identifier: msk_met_2021
    0   genetic_alteration_type: STRUCTURAL_VARIANT
    1   datatype: SV
    2   stable_id: structural_variants
    3   show_profile_in_analysis_tab: true
    4   profile_name: Structural variants
    5   profile_description: Structural Variant Data
    6   data_filename: data_sv.txt
    ----
    processed_data_dict['meta']['sv'] (processed DF returned by this function):
                    Value
    genetic_alteration_type STRUCTURAL_VARIANT
    datatype    SV
    stable_id   structural_variants
    show_profile_in_analysis_tab    true
    profile_name    Structural variants
    profile_description Structural Variant Data
    data_filename   data_sv.txt
    ----
    Arguments:
        raw_data_loc (str): the file path of the folder containing the downloaded cBio Dataset

    Returns:
        raw_data_dict: a dictionary of dictionaries   '''

    processed_dict = {}
    for k,v in raw_dict.items():
        new_cols = []
        reorg_data = []
        #I use iterrows here because each dataframe is small (6 rows or fewer)
        #and the result of each row will be different.
        for idx, data in v.iterrows():
            #example data: cancer_study_identifier: msk_met_2021,
            #    genetic_alteration_type: CLINICAL
            #--> new_col becomes "genetic_alteration_type" and new_data becomes "CLINICAL"
            new_col = (data.str.split(':')[0][0])
            new_cols.append(new_col)
            new_data = data.str.split(':')[0][1]
            reorg_data.append(new_data)
        processed_dict[k] = pd.DataFrame(data=reorg_data,index=new_cols,columns=['Value'])
        return processed_dict
