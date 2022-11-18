# AI 영상분석을 활용한 스마트 스쿨존 안전시스템

## Note!
- Team Notion을 함께 이용하여 자료 공유
- Notion을 이용하여 회의록 및 기타 공유자료 upload
- Git을 이용하여 code update

## 소개
- 보다 안전한 스쿨존 시스템을 구축하기 위하여 프로젝트를 시작하게 됨
- 카메라를 통해 스쿨존을 촬영하고, 실시간으로 이를 분석하여 위험 객체 판단, 충돌 위험 감지, 불법 주/정차 차량 등을 판단하는 시스템을 제작하고자 함
- 위험을 판단하고 실시간으로 상황을 보행자 및 운전자에게 동시다발적으로 제공함
- 판단되는 정보를 데이터베이스에 저장하고, 이를 지속적으로 수집하여 분석함

## 전체 구성도
![image](https://user-images.githubusercontent.com/62232217/178446713-744e8607-09ac-4042-8f8b-2e7c44da12eb.png)

## 차별성(장점)
- 지도화를 통한 상대적 거리 측정 가능
- 스테레오 비전 기술을 활용한 보다 정확한 거리 측정
- 기존 시스템과는 차별적으로, 운전자와 보행자 모두에게 양방향 알림 제공

## 주요 기능
- 스쿨존을 현황을 파악하기 위한 센서(카메라, 과속 센서 등) 및 표출을 위한 교통 안전 장비 구축
- 카메라를 활용한 데이터의 수집, 분석을 위한 AI Platform 구축
- 카메라를 통해 영상정보를 수집하여, 머신러닝 기반 돌발 이벤트(과속, 주/정차, 역주행, 차선변경, 갑작스럽게 뛰어나오는 어린이 등) 인식 모델 구축
- 돌발 이벤트 발생 시에 교통 안전 장비에서 알람(영상, 소리 등) 기능 제공

## Dataset
- 상황별로 촬영된 CCTV(15~30fps) 동영상을 5프레임마다 1장씩 이미지화한 영상 (3840 X 2160 [4k])
- 선별 영상 데이터 : (Training : 10000장, Test : 2500장)

![image](https://user-images.githubusercontent.com/62232217/178444171-4b83b334-e58c-4601-9823-7379717a04e7.png)

(출처 : 어린이 보호구역 내 도로보행 위험행동 영상 소개[AI Hub])<br>
(https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=169)

## 수행 일정
![image](https://user-images.githubusercontent.com/62232217/178445033-d15871b0-829c-4c2a-902e-957724693009.png)

## 모의 시연 영상(gif 형태라 소리는 나지 않음)

### 1. 보행자 ver.
![보행자ver](https://user-images.githubusercontent.com/62232217/192712130-fb4490f4-4b32-4084-a0aa-64c8cd80de7c.gif)

### 2. 운전자 ver.
![운전자ver](https://user-images.githubusercontent.com/62232217/174145988-dfeb4f41-e22f-4688-a80d-90eedd507f49.gif)
