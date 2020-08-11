pyinstaller --onefile --name "SPL-OBS Updater" script.py --version-file "winupdaterinfo.txt"
pyinstaller --onefile --name "SPL-OBS Countdown" countdown.py --version-file "wincountdowninfo.txt"
copy input.yml dist
copy duration.txt dist
copy README.md dist
copy schedule.txt dist
copy spls-template.yml dist
copy install.cmd dist
copy LICNESE dist
copy updater.ini dist
copy countdown.ini dist