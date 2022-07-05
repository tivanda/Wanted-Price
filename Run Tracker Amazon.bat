@echo off
SET BROWSER=chrome.exe
title Pokreni Tracker za Amazon
echo Otvaram server kliknite ako zelite proslijediti s uputama... 
pause
start chrome.exe
start %BROWSER% -new-tab http://127.0.0.1:8000/
"C:\Users\Tomislav\Desktop\wantedprice-masterZI\manage.py" "runserver"
start http://127.0.0.1:8000/
pause


