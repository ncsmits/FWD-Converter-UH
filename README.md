# FWD Converter-UH

Versie 1.x is geschreven in MATLAB, vanaf versie 2.0 wordt er in Python 3.6 geschreven. Voor compilen bleek het noodzakelijk / makkelijker om de oude main.py en fwdconvert.py samen te voegen.

Om te compileren: 
1. In cmd-prompt CD naar de map waar de bestanden staan
2. In cmd: pyinstaller.exe --icon=includes/Icon1.ico -F --noconsole FWD_Converter_V2.0.py
3. Kopieer de defaults.setup en de includes directory in de 'dist' folder
