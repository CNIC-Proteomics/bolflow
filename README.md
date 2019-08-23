# bolflow

# Path in tierra: TEMPORAL
S:\U_Proteomica\PROYECTOS\PESA_omicas\METABOLOMICS\HILIC\HILIC-POS

# Workflow steps

<!-- OLD WORKFLOW -->
<!-- 
## Data pre-processing
1. Combine the 2 matrixes: 0-6 -> take min 0-5;  4-11 -> take min 5-11
2. Add classification to the matrix of data

## Data processing

### Calculation
4. Calculate frequency per group of samples, per single batch, per cohort and global
5. Calculate frequency of QCs per single batch, per cohort and global

### Filtering
6. Filtering 0: Discard duplicates
7. Filtering 1: keeping features that are present at least in the 75% of one group of samples (control and disease) in each cohort, and in at least the 10% in all group of samples per cohort.
8. Filtering 2: keeping features that are present at least in the 80% of samples in at least one group of samples (e.g. for PESA Controls and Diseases)
9. Filtering 3: keeping features that present a CV% in QCs lower than 50% [make it optional]


### Calculation
10. Calculate CV% in QCs per single batch, per cohort and global
-->

## Data pre-processing
1. Combine the 2 matrixes: 0-6 -> take min 0-5;  4-11 -> take min 5-11
2. Add classification to the matrix of data
 
## Data processing

### Calculation
3. Calculate frequency per type of samples, per single batch, per cohort and global
4. Calculate frequency per group of samples, per single batch, per cohort and global
5. Calculate frequency of QCs per single batch, per cohort and global
6. Calculate CV% in QCs per single batch, per cohort and global

### Filtering error
7. Discard duplicates with lower freq. in sample type “S”, and higher CV% in QCs global
8. Keeping features that are present at least in the X% of samples type “S” in at least X group of samples “S” (e.g. for PESA Controls and Diseases)

### Filtering QC:
- keeping features that present at least in the 50% of QCs 
- keeping features that present a CV% in QCs lower than 50% 

### Filtering biological samples:
- keeping features that are present at least in the X% of X group of samples “S” (e.g. control and disease) in each cohort 



## Running scripts

Run sample workflow:
```
SRCDIR="d:/projects/metabolomics/bolflow"
WSKDIR="${SRCDIR}/tests"
cd ${WSKDIR}
```

Step 1-2, pre-processing:
```
python "${SRCDIR}/join_files.py" -ii test1-in1.xlsx test1-in2.xlsx -ic test1-inC.xlsx -o test1-out.join.csv -v
```

Steps 3-6, calculation:
```
python "${SRCDIR}/calc_freq-cv.py" -i test1-out.join.csv -ic test1-inC.xlsx -o test1-out.freq-cv.csv -v
```

Steps 7-8, discarding error:
```
echo "-- remove duplicates"
python "${SRCDIR}/rem_duplicates.py" -i test1-out.freq-cv.csv -d '{"A":[0,5], "B":[4,10]}' -o test1-out.freq-cv-rem.csv -v

```
Steps , filtering:
```
echo "-- filter only the freq for the Quality Control"
python "${SRCDIR}/filter.py" -i test1-out.freq-cv-rem.csv -ic test1-inC.xlsx -t QC -f 50 -o test1-out.freq-cv-rem.filt_QC.csv
echo "-- filter the freq and CV for the Quality Control"
python "${SRCDIR}/filter.py" -i test1-out.freq-cv-rem.csv -ic test1-inC.xlsx -t QC -cv -f 50 -o test1-out.freq-cv-rem.filt_QC_with_cv.csv
echo "-- filter the freq of Biological samples"
python "${SRCDIR}/filter.py" -i test1-out.freq-cv-rem.csv -ic test1-inC.xlsx -t S -f 80 -o test1-out.freq-cv-rem.filt_grp_biological.csv
echo "-- filter the freq of Control group"
python "${SRCDIR}/filter.py" -i test1-out.freq-cv-rem.csv -ic test1-inC.xlsx -t C -f 80 -o test1-out.freq-cv-rem.filt_grp_control.csv
echo "-- filter the freq of Disase group"
python "${SRCDIR}/filter.py" -i test1-out.freq-cv-rem.csv -ic test1-inC.xlsx -t D -f 80 -o test1-out.freq-cv-rem.filt_grp_disases.csv
```


<!-- Run real workflow:
```
$ python join_files.py -ii Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_0-6min_Original.txt Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_4-11min_Original.txt -ic Metabolomics_WORKFLOW/Processing_HILIC_POS/Classification_V1.xlsx -o Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.join.csv

$ python freq-cv.py -i Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.join.csv -qc H_QC1 -o Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.freq-cv.csv

$ python filter.py -ff 80 -fc 50 -i Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.freq-cv.csv -o Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.freq-cv-filt.csv
``` -->


<!--

## More things to do
- Replacing Missing Values with KNN 
- Normalization (include different strategies i.e. LOESS/COMBAT)
- LOG transformation of the value with addition of constant value
- Scaling ?
- Fold change calculation?

-->
