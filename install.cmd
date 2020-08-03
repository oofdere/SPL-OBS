@echo off
echo Welcome to the installer for SPL-OBS.
echo.
echo First things first, is Python 3.7 or later installed on your system?
echo --------------------------------------------------------------------
python --version
echo.
echo If the above text says something along the lines of Python 3.X.X,
echo you should be fine.
echo.
echo If not, install it. A Microsoft Store window might have popped up,
echo and that version is fine.
echo If a window hasn't popped up, refer to the README.
echo If you just installed Python, close this window and run install.cmd
echo again.
echo --------------------------------------------------------------------
pause

echo.
echo Creating venv...
REM python -m venv env
echo.
echo Updating packages...
call update.cmd