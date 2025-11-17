# 🎯 신입사원 멘토링 매칭 Agent

규칙 기반 알고리즘을 활용하여 멘토와 멘티의 프로필을 분석하고, 최적의 멘토링 프로그램을 추천하는 지능형 매칭 시스템입니다.

## ✨ 주요 기능

- **규칙 기반 프로필 분석**: 멘토와 멘티의 프로필, 관심사, 활동 취향을 체계적으로 분석
- **맞춤형 프로그램 추천**: 지역, 예산, 활동 유형을 고려한 최적의 멘토링 프로그램 추천
- **매칭 점수 & 이유 제공**: 각 추천에 대한 점수(0-100)와 상세한 추천 이유 제공
- **다양한 활동 옵션**: 카페 미팅, 식사, 운동, 문화생활 등 12가지 이상의 프로그램
- **비용 없음**: API 키나 외부 서비스 없이 즉시 사용 가능

## 🚀 빠른 시작

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# Windows PowerShell (실행 정책 변경 필요)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# 또는 Windows CMD
.\venv\Scripts\activate.bat
```

### 2. 의존성 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 실행

```bash
python main.py
```

끝입니다! 별도의 설정이나 API 키가 필요하지 않습니다. 🎉

## 📁 프로젝트 구조

```
Test/
├── main.py                      # 메인 실행 파일 (시나리오 예시 포함)
├── requirements.txt             # 의존성 패키지 목록
├── models/                      # 데이터 모델
│   ├── __init__.py
│   ├── mentor.py               # 멘토 프로필 모델
│   ├── mentee.py               # 멘티 프로필 모델
│   └── program.py              # 멘토링 프로그램 모델
├── services/                    # 비즈니스 로직
│   ├── __init__.py
│   └── matching_service.py     # 규칙 기반 매칭 로직
├── data/                        # 데이터
│   └── sample_programs.json    # 샘플 멘토링 프로그램 (12개)
└── README.md                    # 프로젝트 문서
```

## 💡 사용 예시

### 시나리오 1: 개발자 멘토-멘티 매칭

```python
from models import Mentor, Mentee
from services import MatchingService

# 멘토 프로필
mentor = Mentor(
    name="김시니어",
    age=35,
    location="서울",
    job_title="시니어 소프트웨어 엔지니어",
    experience_years=10,
    expertise=["Python", "웹 개발", "코드 리뷰"],
    interests=["카페", "독서", "영화감상"],
    available_days=["월", "수", "금"],
    preferred_budget=20000
)

# 멘티 프로필
mentee = Mentee(
    name="이주니어",
    age=25,
    location="서울",
    job_title="주니어 개발자",
    experience_years=1,
    learning_goals=["코드 리뷰 방법", "클린 코드"],
    interests=["카페", "독서", "게임"],
    budget_limit=30000
)

# 매칭 실행
matching_service = MatchingService()
matching_service.load_programs_from_file("data/sample_programs.json")

recommendations = matching_service.find_matches(
    mentor=mentor,
    mentee=mentee,
    top_k=3
)

# 결과 출력
for rec in recommendations:
    print(f"추천: {rec.program.title}")
    print(f"점수: {rec.match_score}/100")
    print(f"이유: {rec.reason}\n")
```

## 🎨 주요 기술 스택

- **Python 3.11+**
- **규칙 기반 알고리즘**: 지역, 예산, 관심사, 직무를 고려한 점수 계산
- **Pydantic**: 데이터 검증 및 모델 관리

## 📊 매칭 알고리즘

규칙 기반 점수 계산 방식:

1. **지역 매칭 (30점)**: 멘토/멘티 지역과 프로그램 지역 일치도
2. **예산 적합성 (25점)**: 멘티 예산 대비 프로그램 비용 적정성
3. **관심사 일치도 (30점)**: 멘토와 멘티의 공통 관심사 및 프로그램 활동 유형 매칭
4. **직무 적합성 (15점)**: 프로그램이 해당 직무에 적합한지 여부

**총점 100점 만점**으로 계산하여 상위 프로그램을 추천합니다!

## 🔧 커스터마이징

### 새로운 프로그램 추가

`data/sample_programs.json`에 새로운 프로그램을 추가하세요:

```json
{
  "program_id": "PROG013",
  "title": "새로운 프로그램",
  "description": "설명",
  "location": "서울",
  "activity_type": "카페 미팅",
  "estimated_cost": 20000,
  "duration_minutes": 120,
  "recommended_for": ["개발자"],
  "tags": ["실내", "캐주얼"]
}
```

### 매칭 알고리즘 조정

`services/matching_service.py`의 `_calculate_match_score()` 함수에서 가중치를 조정할 수 있습니다:

```python
# 예: 지역 매칭 가중치를 50점으로 증가
if program.location in mentor.location:
    score += 50  # 기존 30점에서 변경
```

## 📊 샘플 프로그램 목록

현재 12개의 샘플 프로그램이 포함되어 있습니다:

- 카페 미팅 (강남, 홍대, 성수)
- 야외 활동 (한강 산책, 등산)
- 식사 (런치, 브런치)
- 스터디 (코드 리뷰, 포트폴리오 피드백)
- 문화생활 (갤러리, 공방 체험)
- 운동 (스크린 골프)
- 게임 (보드게임)

## 🤝 개발자

- 작성자: Jiwoo
- 날짜: 2025-11-17
- 기술: Python, 규칙 기반 알고리즘, Pydantic

## 📝 라이선스

이 프로젝트는 교육 및 개인 용도로 자유롭게 사용할 수 있습니다.

## 🆘 문제 해결

### PowerShell 실행 정책 오류

```
이 시스템에서 스크립트를 실행할 수 없습니다
```

→ 관리자 권한으로 PowerShell을 열고 실행하세요:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

또는 CMD를 사용하세요:
```bash
.\venv\Scripts\activate.bat
```

