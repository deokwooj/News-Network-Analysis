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


##  Bin  Source File(원본 소스 변환 파일에 대한 설명)
-  nouns.p
       - reference 엑셀파일 중 extraction sheet에 있는 명사들을 리스트로 저장한 파일

-  dict_id_name.p
       - whole_table 엑셀파일에서 infosrc_id_whole를 key 값으로 infosrc_name 을 value 로 하여 dictionary 형태로 저장한 파일

-  dict_org.p
       - whole_table 엑셀파일에서 infosrc_org를 value 로 하여 dictionary 형태로 저장한 파일(key 값은 0부터 자동 증가)

-  dict_type.p
       - whole_table 엑셀파일에서 infosrc_type을 value 로 하여 dictionary 형태로 저장한 파일(key 값은 0부터 자동 증가)

      ```
            | S | 1 |
            | R | 2 |
            | I | 3 |
            | N | 4 |
            | O | 5 |
            | s | 6 |
      ```

-  dict_pos.p
       - whole_table 엑셀파일에서 infosrc_pos을 value 로 하여 dictionary 형태로 저장한 파일(key 값은 0부터 자동 증가)

-  dict_code.p
       - whole_table 엑셀파일에서 infosrc_code를 value 로 하여 dictionary 형태로 저장한 파일(key 값은 0부터 자동 증가)

-  dict_classified.p
       - whole_table 엑셀파일에서 infosrc_isclassified를 value 로 하여 dictionary 형태로 저장한 파일(key 값은 0부터 자동 증가)
       - is_classified_paper_category
       - Y : 0
       - N : 1

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
![NLP Flow](https://raw.githubusercontent.com/kowonsik/NLP/master/file/NLP_flow.png)

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
- 소스 다운로드
       - git clone "http://github.com/kowonsik/NLP.git"
- 실행 방법
       - python na_analysis.py
- na_analysis.py
       - main 코드
       - 엑셀 파일과 dictionary 파일로 현재 정보원 메트릭스 생성 코드
- extraction.py
       - reference.xlxs 엑셀파일 중 Reference sheet 의 STN_CONTENT 퀄럼에서 인용문을 분리하고 인용문에서 명사 분리한 코드
- file directory
       - 사용되고 있는 엑셀파일과 dictionary 파일이 존재하는 디렉토리
 
## Output Description (Script 파일 실행 결과)
- 100개 클래스에 대한 메트릭스 예

                U[a:b,0]=all_ns[i].id
                U[a:b,1]=all_ns[i].org
                U[a:b,2]=all_ns[i].type
                U[a:b,3]=all_ns[i].pos
                U[a:b,4]=all_ns[i].code
                U[a:b,5]=all_ns[i].classified


[[   3.    9.    4.   27.   14.    0.]
 [   2.    9.    4.   27.   14.    0.]
 [   1.    9.    4.   27.   14.    0.]
 [   0.    9.    4.   27.   43.    0.]
 [   7.    2.    3.   24.   13.    0.]
 [   6.    9.    4.    8.   14.    0.]
 [   5.    2.    3.   24.   13.    0.]
 [   4.    1.    3.    8.   43.    0.]
 [   9.    4.    3.    2.  331.    0.]
 [   8.    9.    4.   27.   14.    0.]
 [  35.    9.    4.   17.   14.    0.]
 [  36.    6.    3.   16.  121.    0.]
 [  33.    9.    4.   23.   43.    0.]
 [  34.    9.    4.    5.  331.    0.]
 [  39.    9.    4.   27.   14.    0.]
 [  37.    8.    3.    4.  142.    0.]
 [  38.    9.    4.   27.   14.    0.]
 [  43.    9.    4.    4.   14.    0.]
 [  42.    9.    4.   19.   14.    0.]
 [  41.    9.    4.   10.  422.    0.]
 [  40.    9.    4.   18.  422.    0.]
 [  22.    9.    4.   27.   14.    0.]
 [  23.    9.    4.   27.   14.    0.]
 [  24.    9.    4.   17.  331.    0.]
 [  25.    9.    4.   13.  422.    0.]
 [  26.    9.    4.   27.  422.    0.]
 [  27.    9.    4.    8.  422.    0.]
 [  28.    9.    4.    4.   14.    0.]
 [  29.    9.    4.   27.   14.    0.]
 [  30.    7.    3.   20.  994.    0.]
 [  32.    9.    4.   27.  422.    0.]
 [  31.    9.    4.   12.  331.    0.]
 [  19.    7.    3.    7.   14.    0.]
 [  17.    9.    4.   14.  331.    0.]
 [  18.    9.    4.   27.   43.    0.]
 [  15.    9.    4.    6.   14.    0.]
 [  16.    9.    4.   27.   14.    0.]
 [  13.    7.    3.    7.   15.    0.]
 [  14.    9.    4.   27.  422.    0.]
 [  11.    9.    4.   27.   14.    0.]
 [  12.    9.    4.   23.   14.    0.]
 [  21.    9.    4.   27.  422.    0.]
 [  20.    9.    4.    4.  422.    0.]
 [  10.    3.    3.   14.  114.    0.]
 [  79.    9.    4.   27.   14.    0.]
 [  78.    9.    4.   27.   43.    0.]
 [  77.    9.    4.   27.   43.    0.]
 [  82.    9.    4.   25.  331.    0.]
 [  83.    9.    4.   27.   14.    0.]
 [  80.    9.    4.   27.  422.    0.]
 [  81.    9.    4.   27.   14.    0.]
 [  86.    9.    4.   27.  422.    0.]
 [  87.    9.    4.    8.  422.    0.]
 [  84.    9.    4.   27.  422.    0.]
 [  85.    9.    4.   27.   14.    0.]
 [  67.    9.    4.    1.   14.    0.]
 [  66.    9.    4.   27.  422.    0.]
 [  69.    5.    3.   19.   14.    0.]
 [  68.    9.    4.   17.   14.    0.]
 [  70.    9.    4.   16.  331.    0.]
 [  71.    9.    4.   27.   43.    0.]
 [  72.    9.    4.   11.   14.    0.]
 [  73.    9.    4.    5.  331.    0.]
 [  74.    9.    4.   21.  121.    0.]
 [  75.    9.    4.   27.   15.    0.]
 [  76.    0.    3.   16.  121.    0.]
 [  59.    9.    4.   15.   14.    0.]
 [  58.    4.    3.   15.  994.    0.]
 [  57.    9.    4.   27.  331.    0.]
 [  56.    9.    4.   16.   14.    0.]
 [  55.    9.    4.   27.  331.    0.]
 [  64.    9.    4.   27.   43.    0.]
 [  65.    9.    4.   27.   14.    0.]
 [  62.    9.    4.   27.   14.    0.]
 [  63.    9.    4.   27.   14.    0.]
 [  60.    9.    4.   27.  422.    0.]
 [  61.    6.    3.   27.  121.    0.]
 [  49.   11.    3.   19.  532.    0.]
 [  48.    9.    4.   19.  422.    0.]
 [  45.    9.    4.   27.  422.    0.]
 [  44.    9.    4.   11.   14.    0.]
 [  47.    9.    4.    0.   43.    0.]
 [  46.    9.    4.    3.   43.    0.]
 [  51.    9.    4.   27.   14.    0.]
 [  52.    9.    4.   27.   14.    0.]
 [  53.    9.    4.   16.   14.    0.]
 [  54.    4.    3.   16.  994.    0.]
 [  50.    9.    4.   27.   14.    0.]
 [  99.    9.    4.   27.   43.    0.]
 [  98.    9.    4.    9.  422.    0.]
 [  97.    9.    4.    8.   14.    0.]
 [  96.    9.    4.   21.  121.    0.]
 [  95.    9.    4.   26.  422.    0.]
 [  94.    9.    4.   27.   14.    0.]
 [  93.    9.    4.    4.  422.    0.]
 [  92.    9.    4.   27.  422.    0.]
 [  91.   10.    3.   27.  322.    0.]
 [  90.    9.    4.   22.  422.    0.]]











