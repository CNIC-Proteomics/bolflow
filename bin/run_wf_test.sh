#!/usr/bin/bash

LOCAL_DIR=`dirname $0`
SRCDIR="${LOCAL_DIR=`dirname $0`}/../"
WSKDIR="${SRCDIR}/tests"
cd ${WSKDIR}
OUTNAME="test1-out-wf"

echo "-- join files and add features"
python "${SRCDIR}/join_files.py" -ii test1-in1.xlsx test1-in2.xlsx -ic test1-inC.xlsx -o ${OUTNAME}.join.csv -v

echo "-- calculate frequency and coefficient variation"
python "${SRCDIR}/calc_freq-cv.py" -i ${OUTNAME}.join.csv -ic test1-inC.xlsx -o ${OUTNAME}.freq-cv.csv -v

echo "-- remove duplicates"
python "${SRCDIR}/rem_duplicates.py" -i ${OUTNAME}.freq-cv.csv -d '{"A":[0,5], "B":[4,10]}' -o ${OUTNAME}.freq-cv-rem.csv -v

echo "-- filter only the freq for the Quality Control"
python "${SRCDIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t QC -f 50 -o ${OUTNAME}.freq-cv-rem.filt_QC.csv
echo "-- filter the freq and CV for the Quality Control"
python "${SRCDIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t QC -cv -f 50 -o ${OUTNAME}.freq-cv-rem.filt_QC_with_cv.csv
echo "-- filter the freq of Biological samples"
python "${SRCDIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t S -f 80 -o ${OUTNAME}.freq-cv-rem.filt_grp_biological.csv
echo "-- filter the freq of Control group"
python "${SRCDIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t C -f 80 -o ${OUTNAME}.freq-cv-rem.filt_grp_control.csv
echo "-- filter the freq of Disase group"
python "${SRCDIR}/filter.py" -i ${OUTNAME}.freq-cv-rem.csv -ic test1-inC.xlsx -t D -f 80 -o ${OUTNAME}.freq-cv-rem.filt_grp_disases.csv
