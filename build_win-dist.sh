#!/usr/bin/bash

LOCAL_DIR=`dirname $0`
DIST_DIR="${LOCAL_DIR}/dist/win_x64"
OUTNAME="bolflow-Windows_x64"

echo "-- build distribution"
pyinstaller -y --distpath ${DIST_DIR} bolflow.py

echo "-- compress distribution"
cd ${DIST_DIR}
zip -r ${OUTNAME}.zip bolflow