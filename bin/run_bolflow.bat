@ECHO OFF

ECHO ** sets the env. variables from input parameters:

ECHO **
SET  SRC_HOME="%~dp0"
SET  SRC_HOME=%SRC_HOME:"=%
SET  SRC_HOME=%SRC_HOME:~0,-1%
SET  SCRIPT=%SRC_HOME%/bolflow.exe

:: get input variables ----------------------
SET  /p INFILES="** Enter the list of input file(s) (Excel format): "
SET  /p CATFILE="** Enter the catgory file (Excel format): "
SET  /p OUT_DIR="** Enter the output directory: "
FOR  /F "delims=" %%i IN ("%CATFILE%") DO ( SET OUTNAME=%%~ni )

:: check if we want only to filter the files ----------------------
:init_param
    SET /p answer="Do you want to execute all program or only Filter (b/f)? : "
    IF /i "%answer:~,1%" EQU "b" GOTO all_params
    IF /i "%answer:~,1%" EQU "f" GOTO filter_params
    ECHO "Please type 'f' for only filter or 'b' for the execution of everything"
    GOTO init_param


:: parameters for the ask by the input parameters ----------------------
:all_params
    SET /p answer="Do you want to remove duplicates (y/n)? : "
    IF /i "%answer:~,1%" EQU "y" GOTO param1_y
    IF /i "%answer:~,1%" EQU "n" GOTO param1_n
    ECHO "Please type 'y' for Yes or 'n' for No"
    GOTO all_params
:param1_y
    SET /p answer="Which are the times for the samples in the following format {'A':[0,5], 'B':[4,10]} : "
    SET REMDUPL_OPTION=-d "%answer%"
    SET STEPS=123
    GOTO filter_params
:param1_n
    SET STEPS=13
    GOTO filter_params

:filter_params
    SET /p answer="Do you want to filter (y/n)? :"
    IF /i "%answer:~,1%" EQU "y" GOTO param2_y
    IF /i "%answer:~,1%" EQU "n" GOTO run_bolflow
    ECHO "Please type 'y' for Yes or 'n' for No"
    GOTO filter_params
:param2_y
    SET STEPS=%STEPS%4
    SET /p answer="Type of filter (eg, QC; S; C; C,D) : "
    SET filer_type=-t %answer%
    SET /p answer="Value of frequency (integer) : "
    SET filter_freq_val=-ff %answer%
    SET /p answer="Value of coefficient variation (n/integer) : "
    IF not "%answer:~,1%" EQU "n" SET filter_cv_val=-fc %answer%
    SET FILTER_OPTIONS=%filer_type% %filter_freq_val% %filter_cv_val%
    GOTO run_bolflow

:: execute all workflow in one script ----------------------
:run_bolflow
    ECHO ** execute workflow
    CMD /C " "%SCRIPT%"  -d %STEPS%  -ii %INFILES% -ic "%CATFILE%"  -o "%OUT_DIR%"  -n "%OUTNAME%"  %REMDUPL_OPTION%  %FILTER_OPTIONS% "

GOTO EndProcess

:: wait to Enter => Good installation
:EndProcess
    SET /P DUMMY=End of installation. Hit ENTER to continue...
