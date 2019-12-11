@ECHO OFF

ECHO ** sets the env. variables from input parameters:

ECHO **
SET  SRC_HOME="%~dp0"
SET  SRC_HOME=%SRC_HOME:"=%
SET  SRC_HOME=%SRC_HOME:~0,-1%
SET  SCRIPT=%SRC_HOME%/bolflow.exe
REM SET  SCRIPT=python "%SRC_HOME%/../bolflow.py"

:: get input variables ----------------------
SET  /p PARFILE="** Enter the parameter file (YAML format): "


:: execute all workflow in one script ----------------------
ECHO ** execute workflow
ECHO " "%SCRIPT%"  -p "%PARFILE%" " 
CMD /C " "%SCRIPT%"  -p "%PARFILE%" "

GOTO EndProcess

:: wait to Enter => Good installation
:EndProcess
    SET /P DUMMY=End of installation. Hit ENTER to continue...
