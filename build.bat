@echo off

set ICON=.\assets\multi-crawler.ico  :: Windows용 아이콘

:: PyInstaller 실행
pyinstaller --onefile --add-data ".env.prod;." --icon=%ICON% .\src\main.py

echo Build completed with icon: %ICON%