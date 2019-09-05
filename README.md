# bolflow

Metabolomic workflow

<!-- # Path in tierra: TEMPORAL
S:\U_Proteomica\PROYECTOS\PESA_omicas\METABOLOMICS\HILIC\HILIC-POS -->

# Workflow steps

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

Step 1-2, pre-processing:
```
bolflow.exe  -s 1  -n test1-out  -ii tests/test1-in1.xlsx  tests/test1-in2.xlsx  -ic tests/test1-inC.xlsx  -o tests/
```

Steps 3-6, calculation:
```
bolflow.exe  -s 2  -n test1-out  -ii tests/test1-out.join.csv -ic tests/test1-inC.xlsx  -o tests/
```

Steps 7-8, discarding error:
```
bolflow.exe  -s 3  -n test1-out  -ii tests/test1-out.f-cv.csv -ic tests/test1-inC.xlsx  -o tests/  -d "{'A':[0,5], 'B':[4,10]}"

```
Steps , filtering:
```
echo "-- filter only the freq for the Quality Control"
bolflow.exe  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t QC  -ff 50

echo "-- filter the freq and CV for the Quality Control"
bolflow.exe  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t QC  -f 50  -fc 60

echo "-- filter the freq of Biological samples"
bolflow.exe  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t S   -ff 80

echo "-- filter the freq of Control group"
bolflow.exe  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t C   -ff 80

echo "-- filter the freq of Disase group"
bolflow.exe  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t D   -ff 80

echo "-- filter the freq of Control group and Disase group"
bolflow.exe  -s 4  -n test1-out  -ii tests/test1-out.rem.csv  -ic tests/test1-inC.xlsx  -o tests/  -t C,D   -ff 80
```

<!-- 

# Create dist

Execute the following shell script
```
./build_win-dist.sh 0.1.26
```


pyinstaller.exe -y --distpath d\:/projects/metabolomics/bolflow/dist/win_x64 bolflow.py
cd dist/win_x64
zip -r bolflow-win_x64.zip bolflow

-->


<!-- Run sample workflow:
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
``` -->