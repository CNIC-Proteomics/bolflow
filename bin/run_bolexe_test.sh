#!/usr/bin/bash

LOCAL_DIR=`dirname $0`
SRCDIR="${LOCAL_DIR=`dirname $0`}/../"
WSKDIR="${SRCDIR}/tests"
cd ${WSKDIR}
OUTNAME="test1-out-bol"
SCRIPT="${SRCDIR}/dist/win_x64/bolflow/bolflow.exe"

echo "** exectute 'bolflow' script"
${SCRIPT} -s 1234  -n ${OUTNAME}  -ii test1-in1.xlsx test1-in2.xlsx  -ic test1-inC.xlsx  -o ${WSKDIR}  -d '{"A":[0,5], "B":[4,10]}'  -t QC  -f 50

echo "** exectute 'bolflow' workflow"
OUTNAME="test1-out-bol2"

echo "-- join files and add features"
${SCRIPT} -s 1  -n ${OUTNAME}  -ii test1-in1.xlsx test1-in2.xlsx -ic test1-inC.xlsx -o ${WSKDIR}

echo "-- calculate frequency and coefficient variation"
${SCRIPT} -s 2  -n ${OUTNAME}  -ii ${OUTNAME}.join.csv  -ic test1-inC.xlsx  -o ${WSKDIR}

echo "-- remove duplicates"
${SCRIPT} -s 3  -n ${OUTNAME}  -ii ${OUTNAME}.f-cv.csv  -ic test1-inC.xlsx  -o ${WSKDIR}  -d '{"A":[0,5], "B":[4,10]}'

echo "-- filter only the freq for the Quality Control"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${WSKDIR}  -t QC  -f 50

echo "-- filter the freq and CV for the Quality Control"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${WSKDIR}  -t QC  -f 50  -cv

echo "-- filter the freq of Biological samples"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${WSKDIR}  -t S   -f 80

echo "-- filter the freq of Control group"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${WSKDIR}  -t C   -f 80

echo "-- filter the freq of Disase group"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${WSKDIR}  -t D   -f 80
