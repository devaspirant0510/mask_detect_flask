# mask_detect_flask

최근 안면인식 로봇이 많이 상용화가 되고 있습니다.

열 감지 마스크 착용 여부 확인하는 것뿐만 아니라 안면인식까지 가능하다고 하네요

물론 가격이 비싸다는 단점이 있죠



그래서 저는 인공지능 모델 maskdetect랑

웹서버 라이브러리 flask를 연결해 웹서비스를 개발하였습니다.

기계를 따로 구입하지 않아도 웹서버에 접속만 하면 마스크 착용 여부를 확인할 수 있고

로그인 시스템도 있어서 더 효과적으로 관리할 수 있어요

아직 인공지능이나 웹서버 지식이 많이 부족한 상황이라, 작품성이 그렇게 좋진 않습니다...



https://blog.naver.com/nova020510
자세한 내용은 블로그를 참고해주세요


 




cmd에서 detect_mask_video.py를 실행시킵니다.

이러면 사진이 들어올 때마다 마스크 착용 여부를 판단하고 판단한 사진을 폴더에 저장해요


그다음 app.py를 실행시켜 웹서버를 열면 돼요

아직 로컬 호스트에서만 구동 가능해요..

물론 if__name__=='__main__'에서

app.run(host='아이피 주소')

를 하면 같은 네트워크에 있으면 접속이 가능합니다.

나중에 클라우드 서비스도 배포할 계획입니다.



첫 화면입니다. 회원가입을 해볼게요


회원가입을 누르고 정보를 입력하면


회원가입에 성공하셨습니다라는 문구가 뜨고 데이터 베이스에서 테이블을 보면


방금 생성한 아이디가 테이블에 추가됐고

웹페이지에 로그인을 해볼게요


그럼 이렇게 반겨주네요


코로나 확진자 정보를 누르면 

현재 코로나 확진자 현황을 실시간으로 보여줍니다.

홈으로 돌아가 startnow를 누르면 사진을 전송할 수 있어요



사진을 전송하면 몇 명이 마스크로 썼고 몇 명이 마스크를 안 썼는지 보여줍니다.


빨간색 테두리가 그려지고 마스크 미착용에 1이 있네요


마스크를 착용하고 찍으면 마스크 착용에 1이 표시됩니다.


여러 사람도 인식됩니다.




로그아웃을 하면 세션에 저장된 정보가 사라지고

startnow 버튼을 눌러도


로그인 후 이용해달라는 문구가 뜹니다.



이렇게 입력된 사진은 엑셀데이터에 자동으로 저장됩니다.

사진이 입력된 시간하고 사용자 이름, 아이디, 마스크 착용 여부 등이 저장되는데

인코딩 문제 때문에 그런지 사용자 이름이 깨져서 나오네요.. 


엑셀데이터에 사용자 이름을 따로 저장하는 이유가

공공장소에 방문할 때 방명록을 쓰는데

최근 방명록에 있는 개인 정보를 보고 악의적인 목적으로 쓰는 사례가 종종 있어

마스크 착용 여부도 확인하면서 방명록도 자동으로 작성해 주고자 만들었지만

기능적인 면에서 많이 부족한 것 같고 계속해서 고쳐가고 개선해 나가야 될 부분인 것 같아요


입력된 정보는 제  파일에 자동으로 저장됩니다.

원래는 파일 하나로 사진을 덮어씌우기 하는 방식으로 저장하여

용량을 줄이고 싶었지만 플라스크에서 사진 보여주는 방식이 동적으로 안 되는 것 같아 

어쩔 수 없이 사진 이름을 조금씩 바꿔가면서 보여주게 하였습니다.
