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
<a href="https://developers.google.com/youtube/v3/getting-started?hl=ko" target="_blank" rel="noopener noreferrer">Youtube API</a>.
