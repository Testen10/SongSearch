# 음원 검색 프로그램

## 개발 환경
<img src="https://img.shields.io/badge/Python-61DAFB?style=flat&logo=React&logoColor=white"/>
version: 3.9.7


## 목적
<p> 여러 음원 사이트에서 원하는 곡을 편하게 검색하고자 만들어진 프로그램입니다.</p>

## 실행 준비
<p> 가상환경을 사용할 것을 권장합니다. <a href="https://sdc-james.gitbook.io/onebook/2./2.1./2.1.1.", target = "_blank">conda 가상환경 설치하기</a></p>
<p>프로그램 실행을 위해 <b>main.py</b>, :file_folder:<b>img_resource</b>를 다운로드해주세요.</p>
<p>
  명령어를 통해 필요한 라이브러리들을 설치해주세요:
</p>

  ```
    pip install beautifulsoup4
    pip install selenium
    pip install requests
    pip install simplejson
    pip install undetected-chromedriver
    pip install urllib3
    pip install tk
    pip install Image
    pip install pytube
    pip install multiprocess
  ```
<p>
  GUI의 폰트가 깨지지 않고 정상적으로 보일 수 있도록 :file_folder:<b>S-Core_Dream_OTF</b> 에스코어 드림 폰트를 설치해주세요.
</p>

## 기능 설명
### 1. 도움말
<img width="434" alt="help" src="https://github.com/Testen10/SongSearch/assets/140326092/7b9eb1fa-68e0-492e-870c-db944610e32a">
<img width="889" alt="helpenabled" src="https://github.com/Testen10/SongSearch/assets/140326092/d3f0afb3-2729-4904-a0d3-8ed87f8f09a1">

<p>
  커서를 가져다 댈 경우 도움말이 보입니다. 커서를 뗄 경우 도움말이 사라집니다.
</p>

### 2. 음원 정보 추출
<img width="823" alt="urlLink" src="https://github.com/Testen10/SongSearch/assets/140326092/e0bfe2d9-9177-47b6-b40f-fff47e3a4fa0">
<p>
  곡의 유튜브 링크를 붙여넣고 '곡 정보 가져오기' 버튼을 누르면 영상의 썸네일, 영상의 제목, 그리고 채널명이 자동으로 복사됩니다.
  <br>만약 복사 붙여넣기가 안 되는 경우, 아무 알파벳이나 입력하고 지운 후 다시 붙여넣으시면 됩니다.
</p>

### 3. 검색어 수정 및 포함 유무 결정
<img width="861" alt="info" src="https://github.com/Testen10/SongSearch/assets/140326092/7de827c1-ad40-4fa9-8403-c452edf8c09e">
<p>
  2에서 정보들이 자동으로 복사되는 곳입니다. 입력된 값들은 직접 수정할 수 있으며, '곡의 제목'과 '작곡가'란 아래에 검색어를 추가할 수 있습니다.
  <br>Entry 안에 입력된 값이 있을 경우 자동으로 오른쪽의 체크박스가 활성화됩니다. 비어있는 경우에는 자동으로 비활성화됩니다. 체크박스는 직접 활성화/비활성화 시킬 수 있습니다.
</p>

### 4. 키워드 검색 + 검색 팁
<img width="840" alt="search" src="https://github.com/Testen10/SongSearch/assets/140326092/0d3c2b7e-099a-48fa-9a33-fa9c5401ab48">
<p>
  '검색하기' 버튼을 누르면 3에서 입력하고 체크박스를 활성화한 키워드들을 선택한 음원 사이트에서 자동으로 검색합니다.
  <br>선택 가능한 음원 사이트들은 아마존, 아마존 재팬, 오토오이, 네이버 바이브, 밴드캠프, 레코츠쿠입니다. 한 번에 여러 개를 선택할 수 있습니다.
  <br> '음원 검색 Tip'을 누르시면 j-pop 음원 구매 위주의 짤막한 팁을 담은 sub window가 나타납니다.
</p>

## 사용 예시
https://github.com/Testen10/SongSearch/assets/140326092/343d093b-48e2-4c56-85e2-9282abebd508

## 개발 기간
<p> Jul 24, 2023 ~ Aug 10, 2023</p>

## Contact
<p> 오류나 질문 사항 접수: <a href="https://pushoong.com/ask/9746204848", target='_blank'>푸슝</a>

