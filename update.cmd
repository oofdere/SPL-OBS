@echo off
REM call env\Scripts\activate
python --version
echo Getting newest version from GitHub...
echo Not yet implemented :(
echo.

echo Updating python packages...
py -m pip install -r requirements.txt
echo.

echo Done!
pause
