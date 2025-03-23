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

- user agent
- time sleep (random.uniform(3,5))
- webdriver 셋팅 (utils.py 참고)

## 웹드라이버 설치 필요함?

셀레니움 4.6이후부터 웹드라이버를 자동으로 받는다고함


