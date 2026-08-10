# results.csv EDA Notebook

PDF 강의자료의 Python 데이터 처리 내용을 기반으로 `results.csv`를 분석하는 Notebook 모음입니다.

## 파일 구성

- `00_eda_guide.ipynb`: 중복·무정보 컬럼 1차 제거 후 102개 컬럼의 한국어 데이터 사전과 상세 탐색
- `01_eda_target_relationships.ipynb`: PDF 실습 흐름에 따른 로딩·검증·기술통계·상관·통계 검정·시각화
- `02_preprocessing.ipynb`: 누수 제거, 결측·희소 범주·다중응답 처리, 계층화 분할과 저장
- `eda_korean.py`: 원본을 보존하면서 컬럼명과 의미형 응답을 한국어로 표시하는 도우미
- `내용 정리.md`: 목표 설정부터 EDA·전처리·모델·평가까지 현재 분석 판단만 요약한 문서
- `processed/`: 02에서 생성한 학습·테스트 데이터와 전처리 기준 JSON
- `현재까지의 EDA 및 아이디어 정리.html`: 팀 공유용 A4 요약 보고서와 PDF 저장 화면

## `.ipynb` 직접 실행

VS Code에서 `.ipynb`를 클릭한 뒤 Python 커널을 선택하고 `모두 실행`을 누르면 됩니다.

기본 Jupyter Notebook을 사용하는 경우에만 다음 명령을 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook
```

`00_eda_guide.ipynb`를 실행한 뒤 `01_eda_target_relationships.ipynb`를 위에서부터 순서대로 실행합니다.

## 데이터 주의사항

- `results.csv`: 65,437행, 114열, 약 160MB
- 문자열 `NA`는 결측값으로 처리합니다.
- `;` 구분 컬럼은 다중 선택 문항이며 비율 합계가 100%를 넘을 수 있습니다.
- `CompTotal`은 서로 다른 통화가 섞여 있어 국가 간 직접 비교에 사용하지 않습니다.
- 원본 데이터는 변경하지 않습니다.
- 1차 정제에서는 상수 컬럼 `Check`와 완전히 재생성 가능한 `*Admired` 11개 컬럼을 분석 대상에서 제외합니다.
