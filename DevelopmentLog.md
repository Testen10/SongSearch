시작한 이유
=====
나는 음원을 자주 아마존, 아마존 재팬, 오토오이, 그리고 네이버 바이브 등의 음원 사이트에서 구입한다. 근데 이게 여간 귀찮은 것이 아니다
<br> 내가 음원을 구매하는 과정을 요약해보자면,
<ol>
  <li>곡의 이름과 작곡가 알아내기</li>
  <li>네이버 바이브에서 검색해보기</li>
  <li>나오지 않았을 경우, 곡의 영어 이름과 작곡가의 영어 이름 알아내기</li>
  <li>다시 한 번 네이버 바이브에서 검색해보기</li>
  <li>그래도 나오지 않을 경우 아마존에서 검색해보기</li>
  <li>그래도 나오지 않을 경우 아마존 재팬에서 검색해보기</li>
  <li>그래도 나오지 않을 경우 ototoy에서 검색해보기</li>
</ol>
이다.
<br>하나하나 검색해보는 것도 귀찮고, 일일이 웹사이트 켜고 검색하고 하는 것을 반복하는 것도 힘들다.
<br>그러다 문득 생각이 들었다.
<br><i>이거 자동으로 해주는 프로그램을 만들 수 있지 않을까?</i>
<br>마침 코딩 프로젝트도 해보고 싶었기에, 한 번 해보기로 결심했다.

구상
=====
우선 goodnotes를 켜서 아이디어를 정리해보기로 했다.
<br><img src="https://github.com/Testen10/SongSearch/assets/140326092/fa6c891e-ca32-4fc4-9da2-5321d64ca5e7" width="417" height="540">
<img src="https://github.com/Testen10/SongSearch/assets/140326092/f4e0ba93-9c12-4f23-a5cc-cc0474c5dba9" width="417" height="540">
<br>곡의 링크를 입력값으로 받는다는 가정 하에, success criteria를 작성해보았다.
> <ol>
> <li>Input
>  <ol>
>   <li>곡의 유튜브 영상 링크를 입력값으로 받을 것</li>
>   </ol>
>  </li>
> <li>Button
>  <ol>
>   <li>검색 버튼이 있을 것</li>
>   <li>음원 사이트 별로 버튼이 있을 것</li>
>   <li>음원 사이트 버튼은 여러 개를 동시에 선택할 수 있을 것</li>
>   </ol>
>  </li>
> <li>Function
>  <ol>
>   <li>검색 버튼을 누를 경우, 선택한 버튼의 음원 사이트에서 검색을 자동으로 진행할 것</li>
>   <li>존재하지 않는 영상의 링크인 경우, 에러 메시지 띄우기</li>
>   <li>링크 형식의 input값이 아닌 경우, 에러 메시지 띄우기</li>
>   <li>음원 사이트 버튼이 하나도 눌리지 않았을 경우, 에러 메시지 띄우기</li>
>   </ol>
>  </li>
> </ol>

API
=====
이 프로그램은 유튜브 링크를 통해 영상의 이름과 작곡가의 이름을 받아올 수 있도록 하는 api가 필요하다. 검색해보니, 구글에서 제공해주는 유튜브 api가 있었다.
<a href="https://developers.google.com/youtube/v3/getting-started?hl=ko" target="_blank">Youtube API</a>
<br>게시글을 읽어보니, 영상의 제목을 가져오는 기능은 있지만 채널의 id가 아닌 이름을 가져오는 기능은 보이지 않았다. 따로 찾아본 <a href="https://youtu.be/KcPimbou-kI" target="_blank">이 영상</a>을 참고하기로 했다. 제대로 작동하는지 확인해야 하기 때문에 파이썬에서 간단하게 실험해보았다.
<p> 우선 conda를 사용해 프로젝트를 진행할 새 가상환경을 구축하고 필요한 라이브러리들을 install 했다.<br>
<pre><code>conda create -n SongSearch python=3.9.7
conda activate SongSearch
pip install beautifulsoup4
pip install requests
</code></pre>
그 다음, 앞에서 언급한 영상의 코드를 그대로 복사하여 파이썬을 실행했다.
<code><pre>import re
import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.youtube.com/@YouTube/about"
soup = BeautifulSoup(requests.get(URL, cookies={'CONSENT': 'YES+1'}).text, "html.parser")
data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)

json_data = json.loads(data)

channel_id =json_data['header']['c4TabbedHeaderRenderer']['channelId']
channel_name =json_data['header']['c4TabbedHeaderRenderer']['title']
channel_logo =json_data['header']['c4TabbedHeaderRenderer']['avatar']['thumbnails'][2]['url']

print(channel_id)
print(channel_name)
print(channel_logo) </code></pre>
다행히 잘 나온다.
<code><pre>UCBR8-60-B28hp2BmDPdntcQ
YouTube
https://yt3.googleusercontent.com/584JjRp5QMuKbyduM_2k5RlXFqHJtQ0qLIPZpwbUjMJmgzZngHcam5JMuZQxyzGMV5ljwJRl0Q=s176-c-k-c0x00ffffff-no-rj
</code></pre>
