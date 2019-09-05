#!/usr/bin/bash

# get the machine
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

# get source dir depending on machine
if [[ "${machine}" == "Linux" ]]; then
    LOCAL_DIR=${PWD}
elif [[ "${machine}" == "Cygwin" ]]; then
    LOCAL_DIR=`cygpath -w ${PWD}`
else
    exit 1
fi

# get the rest of paths
SRC_DIR="${LOCAL_DIR}/.."
TEST_DIR="${SRC_DIR}/tests"
cd ${TEST_DIR}
OUTNAME="test1-out-bol"
SCRIPT="python ${SRC_DIR}/bolflow.py"

echo "** exectute 'bolflow' script"
${SCRIPT} -s 1234  -n ${OUTNAME}  -ii test1-in1.xlsx test1-in2.xlsx  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -d '{"A":[0,5], "B":[4,10]}'  -t QC  -ff 50

echo "** exectute 'bolflow' workflow"
OUTNAME="test1-out-bol2"

echo "-- join files and add features"
${SCRIPT} -s 1  -n ${OUTNAME}  -ii test1-in1.xlsx test1-in2.xlsx -ic test1-inC.xlsx -o ${TEST_DIR}

echo "-- calculate frequency and coefficient variation"
${SCRIPT} -s 2  -n ${OUTNAME}  -ii ${OUTNAME}.join.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}

echo "-- remove duplicates"
${SCRIPT} -s 3  -n ${OUTNAME}  -ii ${OUTNAME}.f-cv.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -d '{"A":[0,5], "B":[4,10]}'

echo "-- filter only the freq for the Quality Control"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -t QC  -ff 50

echo "-- filter the freq and CV for the Quality Control"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -t QC  -ff 50  -fc 60

echo "-- filter the freq of Biological samples"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -t S   -ff 80

echo "-- filter the freq of Control group"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -t C   -ff 80

echo "-- filter the freq of Disase group"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -t D   -ff 80

echo "-- filter the freq of Control group or Disase group"
${SCRIPT} -s 4  -n ${OUTNAME}  -ii ${OUTNAME}.rem.csv  -ic test1-inC.xlsx  -o ${TEST_DIR}  -v  -t C,D   -ff 80
