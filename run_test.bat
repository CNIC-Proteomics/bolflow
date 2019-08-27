@ECHO OFF

ECHO ** sets the env. variables from input parameters:

ECHO **
SET  SRC_HOME="%~dp0"
SET  SRC_HOME=%SRC_HOME:"=%
SET  SRC_HOME=%SRC_HOME:~0,-1%
SET  IN_DIR="%SRC_HOME%/tests"

SET  SCRIPT=%SRC_HOME%/dist/win_x64/bolflow/bolflow.exe
SET  OUTNAME=test1-out-bol
SET  OUT_DIR=%SRC_HOME%/tests

:: exectute all workflow in one script ----------------------
ECHO ** execute all workflow in one script
CMD /C " "%SCRIPT%"  -s 1234  -ii "%IN_DIR%/test1-in1.xlsx" "%IN_DIR%/test1-in2.xlsx"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  -d "{'A':[0,5], 'B':[4,10]}"  -t QC  -f 50 "


:: ANOTTHER WAY ----------------------
:: exectute all workflow step by step ----------------------
ECHO ** exectute 'bolflow' workflow
SET  OUTNAME=test1-out-bol2

ECHO -- join files and add features
CMD /C " "%SCRIPT%"  -s 1  -ii "%IN_DIR%/test1-in1.xlsx" "%IN_DIR%/test1-in2.xlsx"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  "

ECHO -- calculate frequency and coefficient variation
CMD /C " "%SCRIPT%"  -s 2  -ii "%IN_DIR%/%OUTNAME%.join.csv"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  "

ECHO -- remove duplicates
CMD /C " "%SCRIPT%"  -s 3  -ii "%IN_DIR%/%OUTNAME%.f-cv.csv"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  -d "{'A':[0,5], 'B':[4,10]}" "

ECHO -- filter only the freq for the Quality Control
CMD /C " "%SCRIPT%"  -s 4  -ii "%IN_DIR%/%OUTNAME%.rem.csv"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  -t QC  -f 50 "

ECHO -- filter the freq and CV for the Quality Control
CMD /C " "%SCRIPT%"  -s 4  -ii "%IN_DIR%/%OUTNAME%.rem.csv"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  -t QC  -f 50  -cv"

ECHO -- filter the freq of Biological samples
CMD /C " "%SCRIPT%"  -s 4  -ii "%IN_DIR%/%OUTNAME%.rem.csv"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  -t S   -f 80"

ECHO -- filter the freq of Control group
CMD /C " "%SCRIPT%"  -s 4  -ii "%IN_DIR%/%OUTNAME%.rem.csv"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  -t C   -f 80"

ECHO -- filter the freq of Disase group
CMD /C " "%SCRIPT%"  -s 4  -ii "%IN_DIR%/%OUTNAME%.rem.csv"  -ic "%IN_DIR%/test1-inC.xlsx"  -o "%OUT_DIR%"  -n "%OUTNAME%"  -t D   -f 80"




GOTO :EndProcess

:: wait to Enter => Good installation
:EndProcess
    SET /P DUMMY=End of installation. Hit ENTER to continue...
