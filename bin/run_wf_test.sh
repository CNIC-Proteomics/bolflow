#!/usr/bin/bash

LOCAL_DIR=`dirname $0`
SRC_DIR="${LOCAL_DIR}/../"
TEST_DIR="${SRC_DIR}/tests"
cd ${TEST_DIR}
OUTNAME="test1-out-wf"

echo "-- join files and add features"
python "${SRC_DIR}/join_files.py" -ii test1-in1.xlsx test1-in2.xlsx -ic test1-inC.xlsx -o ${OUTNAME}.join.csv -v

echo "-- calculate frequency and coefficient variation"
python "${SRC_DIR}/calc_freq-cv.py" -i ${OUTNAME}.join.csv -ic test1-inC.xlsx -o ${OUTNAME}.freq-cv.csv -v

echo "-- remove duplicates"
python "${SRC_DIR}/rem_duplicates.py" -i ${OUTNAME}.freq-cv.csv -d '{"A":[0,5], "B":[4,10]}' -o ${OUTNAME}.freq-cv-rem.csv -v

echo "-- filter only the freq for the Quality Control"
python "${SRC_DIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t QC -f 50 -o ${OUTNAME}.freq-cv-rem.filt_QC.csv
echo "-- filter the freq and CV for the Quality Control"
python "${SRC_DIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t QC -cv -f 50 -o ${OUTNAME}.freq-cv-rem.filt_QC_with_cv.csv
echo "-- filter the freq of Biological samples"
python "${SRC_DIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t S -f 80 -o ${OUTNAME}.freq-cv-rem.filt_grp_biological.csv
echo "-- filter the freq of Control group"
python "${SRC_DIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t C -f 80 -o ${OUTNAME}.freq-cv-rem.filt_grp_control.csv
echo "-- filter the freq of Disase group"
python "${SRC_DIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t D -f 80 -o ${OUTNAME}.freq-cv-rem.filt_grp_disases.csv
