##  Excel Source File (원본 소스  엑셀 파일에 대한 설명)
- reference.xlsx (분단에 대한 자료 엑셀 파일)
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


##  Bin  Source File(원본 소스 변환 파일에 대한 설명)
-  nouns.p
       - reference 엑셀파일 중 extraction sheet에 있는 명사들을 리스트로 저장한 파일

-  dict_id_name.p
       - whole_table 엑셀파일에서 id를 key 값으로 name 을 value 로 하여 dictionary 형태로 저장한 파일

-  dict_org.p
       - whole_table 엑셀파일에서 org 을 value 로 하여 dictionary 형태로 저장한 파일(key 값은 0부터 자동 증가)

-  dict_pos.p
       - whole_table 엑셀파일에서 position을 value 로 하여 dictionary 형태로 저장한 파일(key 값은 0부터 자동 증가)

-  dict_informer.p
       - whole_table 엑셀파일과 생성된 dictionary 파일을 활용하여 생성한 정보원 dictionary 파일



## Data Structure (사용되는 Class/Dictionary 에 대한 설명)
- wholetable 엑셀파일에 나와있는 정보원 소스를 바탕으로 구성
- class NewsSource :
       - id = [] 
       - name = [] 
       - org = [] 
       - type=[]
       - pos = [] 
       - code = []
       - isclassified =[]

- all NewSource Dictionary
       - 모든 정보원의 NewsSource 구조체를 value로 하는 dict_informer.p dictionary 파일을 사용



## Code Description 
- 사용되는 함수에 대한 설명

- 전체 코드 파일들 리뷰. 
- 코드에 대한 설명
- 클래스, 함수 등등

## Functions
- excel_noun()
       - 엑셀 인용문에서 명사 분리 코드

- excel_excel_nouns()
       - 분리된 명사를 dictionary로 변환

- get_excel_informers()
       - dict_id_name.p, dict_org.p, dict_pos.p dictionary 파일 생성

- informer_save()
       - dictionary 파일과 excel 파일을 활용하여 NewsSource 클래스를 dictionary로 저장

- get_all_NS()
       - NewsSource 클래스가 dictionary로 저장되어있는 dict_informers.p 파일을 활용하여 메트릭스 생성
 
## How to use
- git clone "http://github.com/kowonsik/NLP.git"
- python na_analysis.py
 
 
## Output Description 
- Script 파일 실행 결과











