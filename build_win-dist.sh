#!/usr/bin/bash

LOCAL_DIR=`dirname $0`
DIST_DIR="${LOCAL_DIR}/dist/win_x64"
TEST_INFILES="${LOCAL_DIR}/tests/test1-in*"
TEST_SCRIPT="${LOCAL_DIR}/run_test.bat"
VERSION=$1

echo "-- build distribution"
pyinstaller  -y  --add-data "${TEST_INFILES};tests/" --add-data "${TEST_SCRIPT};."  --distpath ${DIST_DIR}  bolflow.py

echo "-- compress distribution"
OUTNAME="bolflow_Windoxs-x64_${VERSION}"
cd ${DIST_DIR}
zip -r ${OUTNAME}.zip bolflow