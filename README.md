# WSL 셋팅

## 필요 패키지 설치

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y
```

## 맥북일경우

```bash
asdf uninstall python 3.13.0
asdf install python 3.13.0 --enable-framework # tk개발 라이브러리를 포함시켜서 설치해야함
```

## 차단 방지 조치 방안

- user agent (requests)
- time sleep (random.uniform(3,5))
- webdriver 셋팅 (utils.py 참고)


## app 빌드 스크립트 작성
build.sh
build.bat

## 크롤링 중지 버튼 있어야할듯





