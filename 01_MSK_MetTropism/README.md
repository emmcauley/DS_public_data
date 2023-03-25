Background and Context
-----

### Scope

### Data
Input data is from MSK-MET (Memorial Sloan Kettering - Metastatic Events and Tropisms), a pan-cancer cohort comprised of >25,000 patients. 50 different cancer types are represented in the dataset, available at [cBioPortal](https://www.cbioportal.org/study?id=msk_met_2021) and [Zenodo](https://doi.org/10.5281/zenodo.5801902). The dataset includes tumor genomic profiling data and clinical information on metastatic events and outcomes. [Nguyen et al., 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9147702/) investigates the degree to which genetic alterations are associated with cancer-specific metastatic patterns.  

### Nguyen et al., 2022 Key Findings
Nguyen et al., 2022 evaluated the genomic differences betweeen metastatic and primary samples across the various tumor types and molecular subtypes in the dataset. The team looked at genomic differences between primary and metastatic samples. They also compared primary tumors from metastatic and non-metastatic patients, stratified by tumor type and molecular subtypes.

-----

Code Tour  
-----

### Data Ingest
-----
`cbio_data_ingest.py` contains some helper functions to ingest the cBio data after download that is compatible with Python `pandas`. While there is an [API](https://github.com/odagayev/cbio_py), I found this easier to start with. The user provides the directory of the data to the `grab_cbio_data` function, which uses `glob` and `pandas` to ingest the data and return a dictionary of dictionaries. `report_cbio_data_ingest` can be used to look at shapes of resultant dataframes that are housed in the inner dictionary. `reorg_cbio_meta_data` specifically works to reorganize the metadata files, which will be helpful in the future if a user wants to interrogate a specific file.  


### Data Visualization
-----
This code covers some of the early figures in [Nguyen et al., 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9147702/). Histograms are modeled after Supplemental Figure 1B, dual scatterplots are based off of Figure 2A. Pie charts and bar charts like these are typically of interest and also help to illustrate some of the findings in the text (in-line comments in the code contain examples). 


### Data Cleaning for Machine Learning
-----
I used 3 main sources of data for the ML algorithms I was testing: `patient`, `sample`, and `mutations`. I keep the raw data and build a new dictionary called _processed_data_dict_ to house the cleaned data. I replace and sometimes impute missing values in both the _sample_ and _patient_ dataframes. I also encode the PRIMARY_SITE and ORGAN_SYSTEM values using `pd.get_dummies`. For the _mutations_ dataframe, I use `pd.pivot_table` to create a dataframe in which each column is a gene (denoted by Hugo Symbol) and each row is a sample (denoted by Tumor_Sample_Barcode). I combine all 3 dataframes (keyed by SAMPLE_ID) into a new dataframe called _for_ml_ and work from there. 

### Research Questions and ML Models Implemented
-----
Using the _for_ml_ dataframe, I test out some classification algorithms to try and predict whether a sample is from a primary or metastatic site. First, I used Pricipal Component Analysis (PCA) to encode 524 features (all float + int values) into 5 components, mostly because I am running this on my laptop. The 5 Principal Components (PCs) explain 97% of variance in the data. I looked at the difference in train/test scores between the native features and PC-transformed features using LogisticRegression and didn't see a huge difference. I moved forward with the 5 PCs as features.    

I also tested out an L1-penalized LogisticRegression model to do early feature selection and compare those resultant models to the models ran on just the 5 PCs. I did not see significant differences in AUC. 

### Dataset Tour

The dataset is roughly divided into 3 categories: clinicogenomic data, associated metadata, and case lists.  

```bash
├── LICENSE
├── Readme.txt
├── case_lists
│   ├── cases_all.txt
│   ├── cases_cna.txt
│   ├── cases_cnaseq.txt
│   ├── cases_sequenced.txt
│   └── cases_sv.txt
├── data_clinical_patient.txt
├── data_clinical_sample.txt
├── data_cna.txt
├── data_cna_hg19.seg
├── data_gene_panel_matrix.txt
├── data_mutations.txt
├── data_sv.txt
├── data_timeline_diagnosis.txt
├── data_timeline_sequencing.txt
├── data_timeline_status.txt
├── data_timeline_surgery.txt
├── meta_clinical_patient.txt
├── meta_clinical_sample.txt
├── meta_cna.txt
├── meta_cna_hg19_seg.txt
├── meta_gene_panel_matrix.txt
├── meta_mutations.txt
├── meta_study.txt
├── meta_sv.txt
├── meta_timeline_diagnosis.txt
├── meta_timeline_sequencing.txt
├── meta_timeline_status.txt
└── meta_timeline_surgery.txt
```