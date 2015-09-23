
## 자연어처리와 연결망분석을 활용한 뉴스 빅데이터 분석 시스템 연구

- 뉴스 빅데이터 분석 시스템의 핵심 원천기술인 뉴스기사 자연어처리와 뉴스기사 내용의 연결망분석 소프트웨어 
- 연결망 분석을 위해 기사 내의 인용문을 활용함

- 신문 기사에서 정보를 제공한 정보원의 신뢰성을 분석하는 소프트웨어
- 빅데이터 처리를 통해, 여러가지 기사에서 언급된 정보원의 정보 제공 정확도 / 신뢰도를 파악

#### Input 
  - Excel 기사 자료 
    - 기사를 정리하여 인용문을 추출하고 인용문의 명사를 분리하여 저장
  - 바이너리 소스 파일 
    - 엑셀의 내용을 Dictionary 형태로 변경하여 저장

#### Output
   - 인용문(문장)의 연결망 그래프
   - 엑셀 분석 파일
     - q_id, q_label, q_ex 정리 sheet 
     - Label에 따른 메트릭스 정리 sheet
     - 인용문의 거리 계산에 따른 정리 sheet
       - 거리가 <= 1인경우, <= 2인 경우, <=3인경우, <=4인경우

     - 정의 ctio
       - 0 같거나 매우 유사한 인용문
       - 1 같은 기사에 등장한 서로 다른 두 인용문
       - 2 서로 다른 두 기사에 모두 등장한 인용문(s1, s4)에 의해 매개된 두 기사에 등장한 모든 서로 다른 인용문
       - 3 서로 다른 두 인용문에 의해 매개된 서로 다른 두 기사의 인용문≥4 공통 인용문에 의해 연결되는 서로 다른 둘 이상의 기사에 의해 매개된 서로 다른 두 기사 간의 인용문

---

## 자연어처리와 연결망분석을 활용한 뉴스 빅데이터 분석 시스템 구현

## 소프트웨어 구조

![Code Flow](https://raw.githubusercontent.com/kowonsik/NLP/master/png/code_flow.png)

## 코드 개요

- na_analysis.py
   - 뉴스소스 분석을 위한 메인 실행 파일
- na_build.py
   - 정보원과 인용문이 들어가 있는 엑셀파일에서 데이터 분석용 바이너리 파일로 저장하기 위한 파일
- na_config.py
   - 파일경로등 분석에 필요한 설정이 들어가 있는 파일
- na_const.py
   - 프로그램에서 사용하고 있는 상수들이 들어가 있는 파일
- extraction.py
   - 인용문이 들어가 있는 엑셀파일에서 명사를 분리하고 extraction sheet 를 추가하여 저장하는 파일

##  Excel Source File (원본 소스  엑셀 파일에 대한 설명)
- reference.xlsx ('분단'에 대한 자료 엑셀 파일)
      - Reference sheet : '분단'이 포함되어 있는 인용문 정리
      ```
            | INFOSRC_NAME | 홍성미 |
            | STN_CONTENT  |가일미술관 홍성미 큐레이터는 “DMZ를 중심으로 ~ |
      ```

      - Article sheet : '분단' 관련 기사의 집합
      ```
            | ART_ID       | 01100101.20130515100000019 |
            | ART_HEADLINE | 분단 60년, 그 현실을 위한 예술의 역할 |
            | ART_DATE     | 2013-05-15 |
            | ART_PROVIDER | 경향신문 |
            | ART_CONTENT  | 비무장지대(DMZ)는 역설적 공 간이다.너비 4㎞, 길이 248㎞의 ~ |
      ```

      - Query_Info: '분단' 기사 분류를 위한 쿼리
      ```
            | QUERY     | 분단 |
            | BEGINE    | 20130101 |
            | END       | 20131231 |
            | PROVIDERS | 경향신문+국민일보+문화일보+서울신문+세계일보+한겨레+한국일보+동아일보 |
      ```
      
      - extraction : '분단' 인용문에서 명사 분리
      ```
            | INFOSRC_NAME | 홍성미  |
            | STN_CONTENT  | DMZ를 중심으로 행해지는 ~ |
            | NOUN         | 중심,작가,다양,작품,분단,현실,이슈,예술,역할,문제의식 |
      ```

- wholetable.xlsx (정보원 자료 엑셀 파일)
      ```
            | infosrc_id_whole    | 5 |
            | infosrc_id_day      | 2003/10/10_408 |
            | infosrc_name        | 김수행 |
            | infosrc_org         | 서울대 |
            | infosrc_type        | I |
            | infosrc_pos         | 교수 |
            | infosrc_code        | 13 |
            | infosrc_isclassified| \N |
      ```


- table_define.xlsx : 정보원 정의

      ```
            | infoSrc_ID                   | 정보원 ID |
            | name                         | 이름 |
            | orgName                      | 소속이름 |
            | type                         | 정보원 구분 |
            | position                     | 직함 |
            | etc_position                 | 기타 직함 정보 |
            | yearOfBirth                  | 생년 |
            | person_id(FK)                | 사전의 인물 ID |
            | code                         | 인물의 소속 분류 |
            | is_classified_paper_category | 신문 지면 정보에 의해 정보원의 분류되었는지 여부 |
            | INFOSRC_GLOBAL_ID            | 전기간에 걸친 UniqueID |
      ```

      - type
      ```
            | S | 익명 - 소속 없는 사람 |
            | R | 익명 - 소속 있는 사람 |
            | I | 실명 개인 - 소속 있음 |
            | N | 무속속 실명 |
            | O | 조직 |
            | s | 성만 나와 있는 익명 |
      ```

      - is_classified_paper_category
      ```
            | Y | 본 정보원이 나온 신문지면의 분류에 의해 코딩 |
            | N | 본 정보원이 직함이나, 소속에 의해 코딩이 된 것 |
      ```


##  Bin Source File(원본 소스 변환 파일에 대한 설명)

- NewsQuoObjs.p
   - /exlfiles/reference.xlsx 파일의

- NewsSrcObjs.p
   - /exlfiles/wholetable.xlsx 파일의 id/name/

- dict_news_info.p
   - /exlfiles/reference.xlsx 파일의 extraction sheet 의 name, quatation, noun, article_id 컬럼의 데이터를 저장



## Data Structure (사용되는 Class에 대한 설명)


### table_define.xlsx 파일에서 정보원의 데이터를 클래스로 정의

```sh
class NewsSource:
    def __init__(self):
        self.id = None # uuid 
        self.date=dt.datetime(1999,12,31) #  quotations data,1999년 12월 31일 23시.
        self.name = None # name_seloadObjectBinaryFastt
        self.org = None # org_set
        self.srctype=None #~ {S,R,I,N,O,s}, (e.g. S ~ 익명 - 소속 없는 사람)
        self.pos = None #  Position  status_out!=True
        self.code=None # organization code
        self.classified=None # isclassified 
    def whoami(self): # print the current information for news source object
        for key in self.__dict__.items():
            print key[0],': ', key[1]\
            
```

- id : 정보원 ID
- name : 정보원 이름
- org : 정보원 조직
- srctype : 정보원 구분 {S,R,I,N,O,s}, (e.g. S ~ 익명 - 소속 없는 사람)
- pos : 정보원 직위
- code : 정보원 소속 분류, {헌법재판소, 재판부: 111 }, {검찰 : 211} 
- classified : 신문 지면 정보에 의해 정보원이 분류되어있는지 여부


### reference.xlsx 파일에서 인용문 관련 데이터를 클래스로 저장


```sh

class NewsQuotation:
    def __init__(self):
        self.quotation_key =None # 4 digit number 
        self.article_id =None # 9 digit number 
        self.media_id = None  # 8 digit number string 
        self.date=dt.datetime(1999,12,31) #  quotations data,1999년 12월 31일 23시.
        self.news_src=NewsSource() # create NewsSource object
        self.quotation =None  # position, need utcto be initionalized by kkd_functions. 
        self.nounvec =None # position, need utcto be initionalized by kkd_functions. 
    def whoami(self):
        for key in self.__dict__.items():
            if key[0]=='news_src':
                print key[0],'name : ', key[1].name
            else:
                print key[0],': ', key[1]
```

- Reference sheet
   - INFOSRC_NAME : 정보원 이름976.911 kB
   - STN_CONTENT : 인용문이 들어간 문장
   - ART_ID : 기사 ID
- extraction sheet : 인용문 분리 후 명사 분리하고 정리
   - 이름
   - 인용문
   - 명사
   - 기사 ID

- Art.ID (meta_data_id) :"01101001[-->매체정보].20130527[-->날짜]100000112[-->기사ID] 



## Functions

 
## How to use
- 소스 다운로드
       - git clone "http://github.com/deokwooj/NLP.git"
- 실행 방법
       - python na_analysis.py










