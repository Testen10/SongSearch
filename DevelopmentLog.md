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

Reserach
=====
Title/channel Name/thumbnail extractor
----
이 프로그램은 유튜브 링크를 통해 영상의 이름, 영상의 썸네일, 그리고 작곡가의 이름을 받아올 수 있어야 한다. 검색해보니 <a href="https://developers.google.com/youtube/v3/getting-started?hl=ko" target="_blank">구글에서 제공해주는 유튜브 api</a>도 존재하고, BeautifulSoup과 request이라는 라이브러리를 활용하여 코드를 작성할 수 있었다. 우선 <a href="https://youtu.be/KcPimbou-kI" target="_blank">이 영상</a>을 참고하여 코드가 내가 원하는 결과물을 출력하는지 실험해보았다.
<p>conda를 사용해 프로젝트를 진행할 새 가상환경을 구축하고 필요한 라이브러리들을 설치했다.<br>
<pre><code>conda create -n SongSearch python=3.9.7
conda activate SongSearch
pip install beautifulsoup4
pip install requests
</code></pre>
가상환경을 구축했으니, 기능을 실험해보았다. 먼저 채널명을 가져오는 기능을 실험하기 위해 앞에서 언급한 영상의 코드를 그대로 복사하여 파이썬을 실행했다.
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

print(channel_id)
print(channel_name)</code></pre>
잘 나온다. 채널명과 아이디가 출력되었다.
<code><pre>UCBR8-60-B28hp2BmDPdntcQ
YouTube</code></pre>
<p>이번에는 동영상 제목을 가져오는 코드를 시험해봤다. 처음에는 geeksforgeeks.org의 <a href src="https://www.geeksforgeeks.org/python-obtain-title-views-and-likes-of-youtube-video-using-beautifulsoup/" target="_blank">이 게시글</a>을 참고하였으나,
<code><pre>
AttributeError: 'NoneType' object has no attribute 'text'</pre></code>
계속 이 에러가 발생했다. 텍스트로 변환이 불가능하다고 나오는데, 제대로 작동이 된다면  NoneType object가 나오면 안 된다. 찾아보니, 나와 비슷한 문제를 겪는 사람들이 보였다. 그 사람들은 가져오려는 텍스트가 글자가 아닌 정수(ex: 가격, 조회수 등)이어서 에러가 발생했고, try except 구문을 사용하여 에러를 고쳤다고 한다. 하지만 내가 url을 사용하고 있는 영상은 그냥 영어 제목의 노래이다... 어떻게 손봐야할지 감이 안 와서 작동이 되는 다른 코드를 찾아보았다.
<code><pre># testing if the code can extract video title
URL = "https://youtu.be/_PSjoVXFGAQ"

r = requests.get(URL)
s = BeautifulSoup(r.text, "lxml")

try:    
    # finding meta info for title
    title = s.select_one('meta[itemprop="name"][content]')['content']
    print(title)

except Exception as exp:
    # if error occurs
    print(exp)</code></pre>
다행히 이 코드는 잘 작동한다.
<code><pre>Mili - Fly, My Wings [Limbus Company]</code></pre>
혹시나 해서 내가 영상을 클릭했을 때 원본 제목이 아닌 번역된 버전이 나오는 영상의 링크로도 실험을 해보았다.
<code><pre>URL = "https://youtu.be/ZEy36W1xX8c"
#원본 제목은 メルティランドナイトメア / はるまきごはん feat.初音ミク - Melty Land Nightmare
#영상을 클릭했을 때 나에게 보이는 제목은 멜티랜드 나이트메어 / 하루마키고한 feat.하츠네 미쿠 - Melty Land Nightmare
</code></pre>
원본 제목으로 나온다.
<code><pre>メルティランドナイトメア / はるまきごはん feat.初音ミク - Melty Land Nightmare</code></pre>
<p>다만, 내가 원하는 건 곡의 이름만 가져오는 것인데, 코드는 영상의 제목을 가져온다. 생각해보니, 유튜버마다 영상의 제목에 곡의 이름을 올리는 방식은 다르므로 처음부터 곡의 제목만 가져오게 하지 않고, 우선 프로그램이 유튜브 영상의 제목을 가져오면 유저가 그것을 자신이 원하는대로 수정하는 방식으로 바꿔야 할 듯 하다.

<p>마지막으로 영상의 썸네일을 가져오는 코드다. 유튜브 썸네일은 무조건 'https://i.ytimg.com/vi/(영상 id)/maxresdefault.jpg'의 링크를 띈다고 하니, 영상의 id를 가져오는 코드가 있으면 잘동할 듯 하다. 찾아보니 모든 종류의 유튜브 링크에 대응할 수 있는 파이썬 코드가 있어서 그 코드를 사용하기로 했다.(<a href="https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python" target="_blank">참고한 블로그</a>)
<code><pre>
import urllib.parse

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urllib.parse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urllib.parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None
    
  print(video_id('https://youtu.be/pIP4unQk_EY')
  print(video_id('https://www.youtube.com/watch?v=170Mx8KuURM')
  print(video_id('https://www.youtube.com/watch?v=dZW5hbveouY&list=PLC1og_v3eb4jE0bmdkWtizrSQ4zt86-3D')</code></pre>

모두 잘 나온다.
<code><pre>
  pIP4unQk_EY
  170Mx8KuURM
  dZW5hbveouY</code></pre>

<p>추출한 id를 바탕으로 썸네일 이미지를 출력하기 위해 image 라이브러리를 사용하였다.
<code><pre>
import urllib.request
from PIL import Image
  
url = 'https://www.youtube.com/watch?v=dZW5hbveouY&list=PLC1og_v3eb4jE0bmdkWtizrSQ4zt86-3D'

urllib.request.urlretrieve(
  'https://i.ytimg.com/vi/{}/maxresdefault.jpg'.format(video_id(url)),
   "thumbnail.png")
  
img = Image.open("thumbnail.png")
img.show()</code></pre>

<p>정상적으로 썸네일 이미지가 출력되었다.
  
Auto Searching
----
주어진 키워드를 버튼만 누르면 각종 음원 사이트에 자동으로 검색하게 하는 기능도 필요하다. 예전에 진행했던 내 internal assessment에 비슷한 코드가 사용되었는데, 그 때 사용한 selenium이라는 라이브러리를 활용해보았다. 우선 코드에 필요한 <a href src="https://chromedriver.chromium.org/downloads" target = "_blank">chromedriver</a>를 설치하여 코드 파일이 들어있는 폴더로 옮기고, 예전에 작성한 코드를 그대로 실행해보았다.
<code><pre># testing auto seraching
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time

driver_open = True
chrome_options = Options()
#keep the browser open after searching is conducted
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path="/Users/admin/Documents/CS_IA/chromedriver", options= chrome_options)
#open chrome browser and wait for 0.5s
driver.get("https://www.google.com")
time.sleep(0.5)
element = driver.find_element("name",'q')
#search the recipe of the menu on google tab
element.send_keys('set')
element.submit()</code></pre>
전에는 문제없이 작동했던 것으로 기억하는데, 이번에는 오류가 발생했다.
<code><pre>TypeError: __init__() got an unexpected keyword argument 'executable_path'</code></pre>
찾아보니, selenium이 업데이트되면서 
<code><pre>driver = webdriver.Chrome(executable_path="/Users/admin/Documents/CS_IA/chromedriver", options= chrome_options)</code></pre>
부분을 사용하면 에러가 발생하게 되었다고. 최신 버전에서는 Service를 써야 한다고 해서 해당 코드를 삭제하고 수정했다.
<code><pre>from selenium.webdriver.chrome.service import Service
service = Service(executable_path='./chromedriver.exe')</code></pre>
그랬더니 제대로 구글에 검색창을 띄웠다. 이로써 필요한 기능들은 모두 구현이 가능할 것으로 보인다.

Flowchart / WireFrame
=====
구상이 끝났으니 본격적으로 flowchar와 wireframe을 그려보았다. 유저 친화성을 위해 추가적으로 앱 기능 설명 도움말을 넣었다.
<p>Flowchart
<br>
  <img height="600" alt="main_flowchart" src="https://github.com/Testen10/SongSearch/assets/140326092/23c509b8-0d48-43c2-a807-8aeb75a9a2ec">
  <img height="600" alt="getSongInfo_flowchart" src="https://github.com/Testen10/SongSearch/assets/140326092/4a2540b2-b834-4c15-971c-4dcc33bdf324">
  <img height="600" alt="searchSong_flowchart" src="https://github.com/Testen10/SongSearch/assets/140326092/523c88a4-2296-4d7c-abda-c784eecb79c1">
  <img height="600" alt="showHelpWindow_flowchart" src="https://github.com/Testen10/SongSearch/assets/140326092/461e5b0d-02a9-4912-887a-0e91ea2fa490">
<p>WireFrame
<br>
  <img height="600" src="https://github.com/Testen10/SongSearch/assets/140326092/1b2c9f07-30e4-4fa6-8f36-b4f766eff426">
  <img height="600" src="https://github.com/Testen10/SongSearch/assets/140326092/547e9b7f-d1cb-4338-9873-5b58bc967e7d">
  <img height="600" src="https://github.com/Testen10/SongSearch/assets/140326092/b685b87a-2146-403d-bdae-9689ac2c74a9">
