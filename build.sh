#!/bin/bash

OS="$(uname -s)"

# OS별 아이콘 파일 설정
if [[ "$OS" == "Linux" ]]; then
    ICON="./assets/multi-crawler.png"
elif [[ "$OS" == "Darwin" ]]; then
    ICON="./assets/multi-crawler.icns"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# PyInstaller 실행
# pyinstaller --onefile --noconfirm --add-data ".env.prod:." --icon="$ICON" ./src/main.py
pyinstaller  --windowed --noconfirm --add-data ".env.prod:."  ./src/main.py

echo "Build completed with icon: $ICON"