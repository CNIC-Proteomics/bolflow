# bolflow

# Path in tierra: TEMPORAL
S:\U_Proteomica\PROYECTOS\PESA_omicas\METABOLOMICS\HILIC\HILIC-POS

# Workflow steps

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

## More things to do
- Replacing Missing Values with KNN 
- Normalization (include different strategies i.e. LOESS/COMBAT)
- LOG transformation of the value with addition of constant value
- Scaling ?
- Fold change calculation?


## UnitTest

Running a single test module:
```
python -m unittest tests.test_join
```

Running a single test case or test method:
```
python -m unittest tests.test_join.bolflowTests
python -m unittest tests.test_join.bolflowTests.testJoinFiles
```

Running all tests:
```
python -m unittest discover -s tests -p "test_*.py"
```


## Running simple examples

Run sample workflow:
```
$ python join_files.py -ii tests/test1-in1.txt tests/test1-in2.txt -ic tests/test1-inC.xlsx -o tests/test1-out.join.csv -v
$ python freq-cv.py -i tests/test1-out.join.csv -o tests/test1-out.freq-cv.csv -v
$ python filter.py  -i tests/test1-out.freq-cv.csv -o tests/test1-out.freq-cv-filt.csv -v
```

Run real workflow:
```
$ python join_files.py -ii Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_0-6min_Original.txt Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_4-11min_Original.txt -ic Metabolomics_WORKFLOW/Processing_HILIC_POS/Classification_V1.xlsx -o Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.join.csv

$ python freq-cv.py -i Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.join.csv -o Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.freq-cv.csv

$ python filter.py -ff 80 -fc 50 -i Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.freq-cv.csv -o Metabolomics_WORKFLOW/Processing_HILIC_POS/V1_HILIC_POS_combined-filtered.freq-cv-filt.csv
```

## Running WDL workflow

 cp -rp bolflow.wdl bolflow.json /mnt/projects/metabolomics/bolflow/tests/. && cd /mnt/projects/metabolomics/bolflow/tests/ && java -jar /usr/local/lib/cromwell/cromwell.jar   run bolflow.wdl --inputs bolflow.json && cd -

```
$ cp -rp bolflow.wdl bolflow.json /mnt/projects/metabolomics/bolflow/tests/.

$ cd /mnt/projects/metabolomics/bolflow/tests/ && java -jar /usr/local/lib/cromwell/cromwell.jar   run bolflow.wdl --inputs bolflow.json
```
