# MovieStar 사이트

## 1) 팀원 정보 및 업무 분담 내역

![image](https://user-images.githubusercontent.com/37765338/57835807-59955900-77fa-11e9-845f-9b697ee27d18.png)

### 1-1. 팀원 정보

1. 신동찬 : 기획, 데이터 처리, 디자인, 웹사이트기능 구현, 발표, README.md 제작
2. 김영림 : 기획, 디자인, **PPT, 발표**

## 2) 목표 서비스 구현 및 실제 구현 정도

### 2-1. 목표 서비스  + 실제 구현 정도

* 사이트명 : Troll Movie

* 주요 제작 포인트 

  * 시대를 풍미했던 희대의 망작 영화들을 한 사이트에서 볼 수 있는 추억저장소
  * 코믹함을 살리기 위해서 여러 사이트의 요소들을 패러디하고 싶었음. (일부 구현)
    1. 왓챠플레이
    2. UBD.GG
    3. 구글 폼
    4. 디시위키
    5. 좋은 글들 보여주기

* 구현하고 싶었던 기능들

  1. 영화목록

     * 전체 영화 열람(구현)

       * 여러 크기의 브라우저에 맞는 반응형 웹사이트 (구현)

     * 영화 상세정보 열람(구현)

       * vue.js를 통해서 seamless한 사이트를 만들고 싶음.(구현)

       * 영화 상세정보를 url을 통해서 접근할 수 있도록 하고 싶음(미구현)

     * 영화의 리뷰 조회, 삭제, 수정 기능(구현)

       * 기본적인 리뷰의 정보(날짜, 아이디..) (구현)

       * 추천수, 조회수를 유저의 행동마다 카운팅하여 반영(미구현)

     * 영화 검색기능(미구현)

     * 영화를 Troll Score 순서로 정렬하는 기능(구현)

     * pagination(구현)

       * 역시 페이지의 정보를 url을 통해서 접근할 수 있도록 하고 싶음(미구현)

  2. 인물정보

     * 영화목록과 유사함
       * 인물에 대한 리뷰는 구현하지 못하였음.
     * 배우에 좋아요(like)표시를 할 수 있는 기능 (구현)
     * 망작에 많이 출연한 배우들을 열람/정렬할 수 있는 기능 (미구현)

  3. 추천기능

     * 구글 폼(과 유사한) 디자인을 이용하여 유저의 선호정보를 설문조사로 받음(구현)

       * 구글 폼의 기능을 잘 살려서 패러디(구현)

       * 선호정보를 바탕으로 적절한 추천 제공(구현)

     * 사용자의 선호정보를 데이터베이스화 하여 맞춤추천영화를 자동으로 제공할 수 있는 기능(미구현)

  4. 회원관리

     * 로그인, 로그아웃, 개인정보 변경시스템 (구현)
       * vue.js를 이용하여 seamess한 회원관리 (미구현)
     * 개인 프로필 페이지(미구현)

## 3) 데이터베이스 모델링

![MovieStar_20190515_42_49](https://user-images.githubusercontent.com/37765338/57835808-5a2def80-77fa-11e9-9e02-01ae2095c428.png)

## 4) 핵심 기능

### 4-1. [패러디] 디시위키 헤더

![디시위키_헤더](https://user-images.githubusercontent.com/37765338/57837371-a62e6380-77fd-11e9-81ec-0c849c7a8a24.gif)

vue를 이용하여 여닫음을 조정할 수 있는 기능 추가

### 4-2. 영화페이지

* 영화 정보 + 상세정보 + 리뷰 관리

![Detail_Review](https://user-images.githubusercontent.com/37765338/57835916-8d707e80-77fa-11e9-989f-e46df0010fd4.gif)

* pagination

![pagination](https://user-images.githubusercontent.com/37765338/57835825-5e5a0d00-77fa-11e9-81d5-21ca89d4e8bc.gif)

### 4-3. 배우 페이지

![Actor_페이지](https://user-images.githubusercontent.com/37765338/57835820-5dc17680-77fa-11e9-89c0-4de4cc4f69b9.gif)

좋아요 기능을 vue.js와 django를 연동하여 구현함

### 4-4. 추천기능

![추천기능](https://user-images.githubusercontent.com/37765338/57835823-5dc17680-77fa-11e9-8a62-70a3bf25ff74.gif)

Google Form을 패러디하여 개인의 선호장르와 선호배우를 기반으로 영화를 추천하였습니다\

### 4-5. 회원관리

![회원관리](https://user-images.githubusercontent.com/37765338/57835824-5e5a0d00-77fa-11e9-8ff6-3bc0158fa59d.gif)

로그인, 프로필변경, 비밀번호 변경 등의 기본적인 회원관리 기능

## 5) 배포 서버 URL

### https://moviestar-start666.c9users.io/

## 6) 느낀점

1. 간단해 보이는 서비스를 만드는 것도 실제로 구현해보면 전혀 간단하지 않다는 것을 느꼈습니다

2. API를 이용해서 데이터를 수집할 일이 많이 없었는데, 수집해 볼 수 있는 좋은 기회였습니다.

3. 수집한 데이터를 전처리하기 위한 작업들이 생각보다 시간이 많이 걸리고 힘들었습니다.

4. Html과 CSS를 이용하여 전체적인 디자인을 하는데, 쉬워 보이는 사이트를 패러디하는 것도 생각보다 힘들었습니다.

   특히 클래스와 클래스간의 상속관계와 우선순위가 워낙 복잡해서 생각하던 디자인을 꾸며내는 작업이 힘들었습니다.

5. 패러디를 위한 좋은 아이디어를 찾기가 힘들었습니다.

   4번과 연관지어서 좋아 보이는 패러디를 찾아도, 실제로 구현할 수 있는 시간이 부족하여 선택하지 못한 패러디들이 많습니다.

6. 망한 작품들을 눈대중으로만 알고 있었지, 영화에 대한 도메인 지식을 보유하지 않아서 데이터 분석을 통해서 망한 작품들을 추출하는 일이 생각보다 힘들다는 것을 깨달았습니다.

7. vue.js를 이용하여 유저 편의성을 위한 작업들을 많이 시행했는데, 생각보다 편리하면서도 공부해야할 기능들이 많다는 것을 깨달았습니다.

8. 대학생 시절에 조별과제를 하면서 ppt를 많이 제작했었고, 웹사이트도 이것과 비슷할 것이라고 판단했지만, 웹사이트의 구성요소들이 매우 복잡하다는 것을 느꼈습니다.

9. 프로젝트 시간이 너무 촉박해서 다양한 기능과 화려한 디자인을 만들기가 현실적으로 힘들었습니다.

10. 이미 왓챠플레이나 넷플릭스와 같은 매우 훌륭한 웹 사이트가 많음에도 불구하고, 영화라는 주제로 참신한 프로젝트를 하는 것이 상당히 힘들었습니다.

    