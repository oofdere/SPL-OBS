pyinstaller --onefile --name "SPL-OBS Updater" script.py --version-file "winupdaterinfo.txt" --icon=updater.ico
pyinstaller --onefile --name "SPL-OBS Countdown" countdown.py --version-file "wincountdowninfo.txt" --icon=countdown.ico
copy input.yml dist
copy duration.txt dist
copy README.md dist
copy schedule.txt dist
copy spls-template.yml dist
copy install.cmd dist
copy LICNESE dist
copy updater.ini dist
copy countdown.ini dist
pip-licenses --format=plain-vertical --with-license-file --with-notice-file --no-license-path --output-file=LICENSES
copy LICENSES dist