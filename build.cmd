pyinstaller --onefile --name "OBS-SPL Updater" script.py
pyinstaller --onefile --name "OBS-SPL Countdown" countdown.py
copy input.yml dist
copy duration.txt dist
copy README.md dist
copy schedule.txt dist
copy spls-template.yml dist
copy install.cmd dist