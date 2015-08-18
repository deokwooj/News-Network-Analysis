#  Excel Source File (원본 소스  엑셀 파일에 대한 설명)
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

- table_define.xlsx

- wholetable.xlsx (정보원 자료 엑셀 파일)
      ```
| infosrc_id_whole | infosrc_id_day | infosrc_name | infosrc_org | infosrc_type | infosrc_pos | infosrc_code | infosrc_isclassified |
| ---------------- | -------------- | ------------ | ----------- | ------------ | ----------- | ------------ | -------------------- |
| infosrc_id_whole | infosrc_id_day | infosrc_name | infosrc_org | infosrc_type | infosrc_pos | infosrc_code | infosrc_isclassified |
      ```

#  Bin  Source File(원본 소스 변환 파일에 대한 설명)
-  nouns.p
-  dict_id_name.p
-  dict_informer.p
-  dict_org.p
-  dict_pos.p

# Data Structure 
- 사용되는 Class 에 대한 설명
- Dictionary에 대한 설명 등등



# Code Description 
- 사용되는 함수에 대한 설명

- 전체 코드 파일들 리뷰. 
- 코드에 대한 설명
- 클래스, 함수 등등

# Functions
- 사용되는 함수에 대한 설명
 
# How to use
- Script 파일을 어떻게 사용할 건가 ?>
 
 
# Output Description 
- Script 파일 실행 결과











