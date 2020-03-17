#!/usr/bin/bash

LOCAL_DIR=`dirname $0`
DIST_DIR="${LOCAL_DIR}/dist/win_x64"
TEST_INFILES="${LOCAL_DIR}/test/test1-in*"
BATCH_SCRIPT="${LOCAL_DIR}/bin/bolflow.bat"
PARAMS_YML="${LOCAL_DIR}/params.yml"
VERSION=$1

echo "-- build distribution"
pyinstaller  -y  --add-data "${TEST_INFILES};test/" --add-data "${BATCH_SCRIPT};." --add-data "${PARAMS_YML};."  --distpath ${DIST_DIR}  bolflow.py

echo "-- compress distribution"
OUTNAME="bolflow_Windoxs-x64_${VERSION}"
cd ${DIST_DIR}
zip -r ${OUTNAME}.zip bolflow
