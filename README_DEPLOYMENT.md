# 🚀 배포 가이드

## 📋 현재 프로젝트 구조

```
Test/
├── app.py                       # Streamlit 웹 애플리케이션 (NEW!)
├── main.py                      # 콘솔 버전 (기존)
├── requirements.txt             # 의존성 패키지
├── .streamlit/
│   └── config.toml             # Streamlit 설정
├── models/                      # 데이터 모델
├── services/                    # 비즈니스 로직
└── data/                        # 데이터 파일
    ├── sample_mentors.json
    ├── sample_mentees.json
    └── sample_programs.json
```

---

## 🖥️ 로컬 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Streamlit 웹앱 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동 오픈!

### 3. 콘솔 버전 실행 (기존)
```bash
python main.py
```

---

## 🌐 Streamlit Cloud 배포 (무료!)

### 준비물
- GitHub 계정
- 이 프로젝트

### 단계

#### 1️⃣ GitHub 저장소 생성

```bash
# Git 초기화 (아직 안했다면)
git init

# 파일 추가
git add .

# 커밋
git commit -m "Add mentoring matching agent"

# GitHub 저장소 연결 (미리 GitHub에서 저장소 생성 필요)
git remote add origin https://github.com/YOUR-USERNAME/mentoring-agent.git

# 푸시
git push -u origin main
```

#### 2️⃣ Streamlit Cloud 배포

1. https://streamlit.io/cloud 접속
2. GitHub 계정으로 로그인
3. "New app" 버튼 클릭
4. 설정:
   - **Repository**: `your-username/mentoring-agent`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. "Deploy!" 클릭

#### 3️⃣ 완료!

약 2-3분 후 배포 완료!  
URL: `https://your-app-name.streamlit.app`

---

## 🔧 다른 배포 옵션

### Heroku (무료 Tier 종료됨, 유료만 가능)

1. `Procfile` 생성:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Heroku CLI로 배포:
```bash
heroku create your-app-name
git push heroku main
```

### Vercel (정적 사이트 호스팅)

Streamlit은 서버가 필요해서 Vercel보다는 Streamlit Cloud가 더 적합합니다.

### AWS / Azure / GCP

고급 옵션 - Docker 컨테이너로 배포 가능

---

## 🎨 커스터마이징

### 테마 변경

`.streamlit/config.toml` 수정:

```toml
[theme]
primaryColor = "#FF6B6B"      # 메인 색상
backgroundColor = "#FFFFFF"    # 배경색
secondaryBackgroundColor = "#F0F2F6"  # 보조 배경색
textColor = "#262730"          # 텍스트 색상
```

### 도메인 연결 (Streamlit Cloud)

Streamlit Cloud Pro 플랜에서 커스텀 도메인 지원

---

## 📊 모니터링

Streamlit Cloud에서 자동으로 제공:
- 앱 상태
- 리소스 사용량
- 로그
- 재시작

---

## ⚠️ 주의사항

1. **무료 플랜 제한**:
   - Streamlit Cloud: 1개 Private 앱, 무제한 Public 앱
   - 리소스 제한: 1 GB RAM

2. **보안**:
   - API 키는 Streamlit Secrets에 저장
   - `.env` 파일은 `.gitignore`에 추가됨

3. **데이터**:
   - JSON 파일이 Git에 커밋되어야 함
   - 대용량 데이터는 외부 DB 사용 권장

---

## 🆘 문제 해결

### 앱이 시작되지 않음
```bash
streamlit run app.py --logger.level=debug
```

### 모듈을 찾을 수 없음
```bash
pip install -r requirements.txt
```

### Streamlit Cloud에서 오류
- "Manage app" → "Reboot" 클릭
- 로그 확인

---

## 📞 도움말

- Streamlit 문서: https://docs.streamlit.io
- Streamlit Cloud: https://streamlit.io/cloud
- 커뮤니티: https://discuss.streamlit.io

