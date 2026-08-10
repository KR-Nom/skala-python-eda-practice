'''results.csv 한국어 표시 도우미

작성자: 장현진
작성일: 2026-08-05
변경사항: 114개 컬럼의 한국어 이름과 설문 응답 번역 기능 추가
프로그램 설명: 원본 데이터는 변경하지 않고 EDA 화면에서 컬럼과 응답을 한국어로 표시한다.
실행 방법: 00_eda_guide.ipynb에서 import하여 사용
'''

from __future__ import annotations

import re
from typing import Any

import pandas as pd


# 원문 컬럼명은 분석 코드와의 호환성을 위해 별도로 보존한다.
COLUMN_KO = {
    "ResponseId": "응답 ID", "MainBranch": "개발 활동 유형", "Age": "연령대",
    "Employment": "고용 상태", "RemoteWork": "근무 방식", "Check": "설문 확인값",
    "CodingActivities": "업무 외 코딩 활동", "EdLevel": "최종 학력",
    "LearnCode": "코딩 학습 경로", "LearnCodeOnline": "온라인 학습 자료",
    "TechDoc": "기술 문서 이용 방식", "YearsCode": "코딩 경력(년)",
    "YearsCodePro": "전문 개발 경력(년)", "DevType": "개발자 직무",
    "OrgSize": "조직 규모", "PurchaseInfluence": "구매 의사결정 영향력",
    "BuyNewTool": "새 도구 조사 방법", "BuildvsBuy": "구축 대 구매 선호",
    "TechEndorse": "기술 선택 시 선호 요소", "Country": "거주 국가",
    "Currency": "급여 통화", "CompTotal": "총 보수(현지 통화)",
    "LanguageHaveWorkedWith": "사용해 본 프로그래밍 언어", "LanguageWantToWorkWith": "사용하고 싶은 프로그래밍 언어",
    "LanguageAdmired": "계속 사용하고 싶은 프로그래밍 언어", "DatabaseHaveWorkedWith": "사용해 본 데이터베이스",
    "DatabaseWantToWorkWith": "사용하고 싶은 데이터베이스", "DatabaseAdmired": "계속 사용하고 싶은 데이터베이스",
    "PlatformHaveWorkedWith": "사용해 본 클라우드 플랫폼", "PlatformWantToWorkWith": "사용하고 싶은 클라우드 플랫폼",
    "PlatformAdmired": "계속 사용하고 싶은 클라우드 플랫폼", "WebframeHaveWorkedWith": "사용해 본 웹 프레임워크",
    "WebframeWantToWorkWith": "사용하고 싶은 웹 프레임워크", "WebframeAdmired": "계속 사용하고 싶은 웹 프레임워크",
    "EmbeddedHaveWorkedWith": "사용해 본 임베디드 기술", "EmbeddedWantToWorkWith": "사용하고 싶은 임베디드 기술",
    "EmbeddedAdmired": "계속 사용하고 싶은 임베디드 기술", "MiscTechHaveWorkedWith": "사용해 본 기타 프레임워크·라이브러리",
    "MiscTechWantToWorkWith": "사용하고 싶은 기타 프레임워크·라이브러리", "MiscTechAdmired": "계속 사용하고 싶은 기타 프레임워크·라이브러리",
    "ToolsTechHaveWorkedWith": "사용해 본 개발 도구", "ToolsTechWantToWorkWith": "사용하고 싶은 개발 도구",
    "ToolsTechAdmired": "계속 사용하고 싶은 개발 도구", "NEWCollabToolsHaveWorkedWith": "사용해 본 개발 환경",
    "NEWCollabToolsWantToWorkWith": "사용하고 싶은 개발 환경", "NEWCollabToolsAdmired": "계속 사용하고 싶은 개발 환경",
    "OpSysPersonal use": "개인용 운영체제", "OpSysProfessional use": "업무용 운영체제",
    "OfficeStackAsyncHaveWorkedWith": "사용해 본 비동기 협업 도구", "OfficeStackAsyncWantToWorkWith": "사용하고 싶은 비동기 협업 도구",
    "OfficeStackAsyncAdmired": "계속 사용하고 싶은 비동기 협업 도구", "OfficeStackSyncHaveWorkedWith": "사용해 본 실시간 협업 도구",
    "OfficeStackSyncWantToWorkWith": "사용하고 싶은 실시간 협업 도구", "OfficeStackSyncAdmired": "계속 사용하고 싶은 실시간 협업 도구",
    "AISearchDevHaveWorkedWith": "사용해 본 AI 검색·개발 도구", "AISearchDevWantToWorkWith": "사용하고 싶은 AI 검색·개발 도구",
    "AISearchDevAdmired": "계속 사용하고 싶은 AI 검색·개발 도구", "NEWSOSites": "이용한 Stack Overflow 사이트",
    "SOVisitFreq": "Stack Overflow 방문 빈도", "SOAccount": "Stack Overflow 계정 보유 여부",
    "SOPartFreq": "Stack Overflow 참여 빈도", "SOHow": "Stack Overflow 이용 목적",
    "SOComm": "Stack Overflow 커뮤니티 소속감", "AISelect": "AI 도구 사용 여부",
    "AISent": "AI 도구에 대한 태도", "AIBen": "AI 도구의 이점",
    "AIAcc": "AI 결과 신뢰도", "AIComplex": "AI의 복잡한 작업 처리 평가",
    "AIToolCurrently Using": "현재 AI를 사용하는 업무", "AIToolInterested in Using": "AI 사용에 관심 있는 업무",
    "AIToolNot interested in Using": "AI 사용에 관심 없는 업무", "AINextMuch more integrated": "향후 AI를 훨씬 더 통합할 업무",
    "AINextNo change": "향후 AI 통합 수준을 유지할 업무", "AINextMore integrated": "향후 AI를 더 통합할 업무",
    "AINextLess integrated": "향후 AI를 덜 통합할 업무", "AINextMuch less integrated": "향후 AI를 훨씬 덜 통합할 업무",
    "AIThreat": "AI의 현재 직업 위협 여부", "AIEthics": "AI 윤리 우려",
    "AIChallenges": "조직의 AI 도입 과제", "TBranch": "전문 개발자용 문항 대상 여부",
    "ICorPM": "개별 기여자·관리자 구분", "WorkExp": "업무 경력(년)",
    **{f"Knowledge_{i}": f"지식 공유·업무 인식 문항 {i}" for i in range(1, 10)},
    **{f"Frequency_{i}": f"업무 방해 상황 빈도 {i}" for i in range(1, 4)},
    "TimeSearching": "답을 찾는 데 쓰는 시간", "TimeAnswering": "질문에 답하는 데 쓰는 시간",
    "Frustration": "업무 중 불만 요인", "ProfessionalTech": "조직에서 사용하는 전문 개발 기술",
    "ProfessionalCloud": "조직의 클라우드 환경", "ProfessionalQuestion": "업무 질문의 답을 찾는 경로",
    "Industry": "근무 산업", "JobSatPoints_1": "직무 만족 요인 배점 1",
    "JobSatPoints_4": "직무 만족 요인 배점 4", "JobSatPoints_5": "직무 만족 요인 배점 5",
    "JobSatPoints_6": "직무 만족 요인 배점 6", "JobSatPoints_7": "직무 만족 요인 배점 7",
    "JobSatPoints_8": "직무 만족 요인 배점 8", "JobSatPoints_9": "직무 만족 요인 배점 9",
    "JobSatPoints_10": "직무 만족 요인 배점 10", "JobSatPoints_11": "직무 만족 요인 배점 11",
    "SurveyLength": "설문 길이 평가", "SurveyEase": "설문 난이도 평가",
    "ConvertedCompYearly": "연간 환산 보수(USD)", "JobSat": "직무 만족도(0~10)",
}


VALUE_KO = {
    "NA": "미응답", "<MISSING>": "미응답", "Yes": "예", "No": "아니요",
    "Other (please specify):": "기타(직접 입력)", "Other:": "기타",
    "I am a developer by profession": "전문 개발자로 일함", "I am learning to code": "코딩을 배우는 중",
    "I am not primarily a developer, but I write code sometimes as part of my work/studies": "주 직무는 개발자가 아니지만 업무·학업에서 코드를 작성함",
    "I code primarily as a hobby": "주로 취미로 코딩함", "I used to be a developer by profession, but no longer am": "과거에는 전문 개발자였으나 현재는 아님",
    "Under 18 years old": "18세 미만", "65 years or older": "65세 이상", "Prefer not to say": "응답하지 않음",
    "Employed, full-time": "정규직", "Employed, part-time": "시간제 근무", "Student, full-time": "전일제 학생",
    "Student, part-time": "시간제 학생", "Independent contractor, freelancer, or self-employed": "독립 계약자·프리랜서·자영업",
    "Not employed, but looking for work": "미취업·구직 중", "Not employed, and not looking for work": "미취업·구직하지 않음",
    "Retired": "은퇴", "I prefer not to say": "응답하지 않음", "Remote": "원격근무", "In-person": "대면근무",
    "Hybrid (some remote, some in-person)": "혼합근무(원격+대면)", "Hobby": "취미",
    "Contribute to open-source projects": "오픈소스 프로젝트 기여", "Freelance/contract work": "프리랜서·계약 업무",
    "School or academic work": "학교·학술 활동", "Bootstrapping a business": "직접 사업 시작",
    "I don’t code outside of work": "업무 외에는 코딩하지 않음", "Professional development or self-paced learning from online courses": "전문성 개발·온라인 자기주도 학습",
    "Primary/elementary school": "초등학교", "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "중·고등학교",
    "Some college/university study without earning a degree": "대학 과정 일부 이수(학위 없음)", "Associate degree (A.A., A.S., etc.)": "전문학사",
    "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "학사", "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "석사",
    "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "전문·박사 학위", "Something else": "기타 학력",
    "Books / Physical media": "책·인쇄 매체", "Coding Bootcamp": "코딩 부트캠프", "Colleague": "동료",
    "Friend or family member": "친구·가족", "On the job training": "직무 교육", "Online Courses or Certification": "온라인 강좌·자격증",
    "School (i.e., University, College, etc)": "학교(대학 등)", "Technical documentation": "기술 문서", "Blogs": "블로그",
    "Books": "책", "Written Tutorials": "글 형태 튜토리얼", "How-to videos": "사용법 영상", "Interactive tutorial": "대화형 튜토리얼",
    "Coding sessions (live or recorded)": "실시간·녹화 코딩 세션", "Social Media": "소셜 미디어", "Auditory material (e.g., podcasts)": "오디오 자료(팟캐스트 등)",
    "Multiple times per day": "하루 여러 번", "Daily or almost daily": "매일 또는 거의 매일", "A few times per week": "주 몇 회",
    "A few times per month or weekly": "월 몇 회 또는 주 1회", "Less than once per month or monthly": "월 1회 이하",
    "Not sure/can't remember": "모름·기억나지 않음", "No, and I don't plan to": "아니요, 사용할 계획도 없음",
    "No, but I plan to soon": "아니요, 곧 사용할 계획", "Very favorable": "매우 긍정적", "Favorable": "긍정적",
    "Indifferent": "중립적", "Unfavorable": "부정적", "Very unfavorable": "매우 부정적", "Unsure": "잘 모르겠음",
    "Increase productivity": "생산성 향상", "Greater efficiency": "효율 향상", "Improve collaboration": "협업 개선",
    "Speed up learning": "학습 속도 향상", "Improve accuracy in coding": "코딩 정확도 향상", "Make workload more manageable": "업무 부담 완화",
    "Highly trust": "매우 신뢰", "Somewhat trust": "어느 정도 신뢰", "Neither trust nor distrust": "신뢰도 불신도 아님",
    "Somewhat distrust": "다소 불신", "Highly distrust": "매우 불신", "Strongly agree": "매우 동의", "Agree": "동의",
    "Neither agree nor disagree": "동의도 반대도 아님", "Disagree": "반대", "Strongly disagree": "매우 반대",
    "Never": "전혀 없음", "10+ times a week": "주 10회 이상", "6-10 times a week": "주 6~10회",
    "3-5 times a week": "주 3~5회", "1-2 times a week": "주 1~2회", "Individual contributor": "개별 기여자",
    "People manager": "인력 관리자", "Cloud only (single or multi-cloud)": "클라우드만 사용(단일·멀티 클라우드)",
    "Hybrid (on-prem and cloud)": "하이브리드(온프레미스+클라우드)", "On-prem": "온프레미스",
    "Appropriate in length": "적절한 길이", "Too long": "너무 김", "Too short": "너무 짧음",
    "Difficult": "어려움", "Easy": "쉬움", "Neither easy nor difficult": "쉽지도 어렵지도 않음",
    "Neutral": "중립", "No, not at all": "전혀 아님", "No, not really": "별로 아님", "Not sure": "잘 모르겠음",
    "Yes, definitely": "매우 그러함", "Yes, somewhat": "어느 정도 그러함", "I'm not sure": "잘 모르겠음",
}


def translate_value(value: Any) -> Any:
    """결측·다중응답·서술형 범주를 한국어로 표시하고 수치와 기술 고유명사는 보존한다."""
    if pd.isna(value):
        return "미응답"
    if not isinstance(value, str):
        return value
    if ";" in value:
        return "; ".join(translate_value(part.strip()) for part in value.split(";") if part.strip())
    if value in VALUE_KO:
        return VALUE_KO[value]
    age_match = re.fullmatch(r"(\d+)-(\d+) years old", value)
    if age_match:
        return f"{age_match.group(1)}~{age_match.group(2)}세"
    employee_match = re.fullmatch(r"([\d,]+) to ([\d,]+) employees", value)
    if employee_match:
        return f"직원 {employee_match.group(1)}~{employee_match.group(2)}명"
    minute_match = re.fullmatch(r"(\d+)-(\d+) minutes a day", value)
    if minute_match:
        return f"하루 {minute_match.group(1)}~{minute_match.group(2)}분"
    if value == "Less than 15 minutes a day":
        return "하루 15분 미만"
    if value == "Over 120 minutes a day":
        return "하루 120분 초과"
    return value  # 언어·제품·국가·통화 등 고유명사는 검색 가능하도록 원문 유지


def korean_view(frame: pd.DataFrame) -> pd.DataFrame:
    """원본을 건드리지 않고 컬럼명과 표시값을 한국어화한 복사본을 반환한다."""
    translated = frame.copy()
    object_columns = translated.select_dtypes(include=["object", "string"]).columns
    for column in object_columns:
        translated[column] = translated[column].map(translate_value)
    return translated.rename(columns=COLUMN_KO)
