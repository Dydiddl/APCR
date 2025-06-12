# APCR (Advanced Project Contract Resource Management)

건설 프로젝트와 계약 관리를 위한 종합 관리 시스템입니다.

## 주요 기능

- 사용자 관리
  - 로그인/로그아웃
  - 사용자 권한 관리
  - 사용자 정보 관리
- 프로젝트 관리
  - 프로젝트 등록/수정/삭제
  - 프로젝트 현황 조회
  - 프로젝트 코드 관리
- 계약 관리
  - 계약서 등록/수정/삭제
  - 계약 현황 조회
  - 계약 코드 관리

## 설치 방법

1. Python 3.8 이상 설치
2. 프로젝트 클론
   ```bash
   git clone [repository-url]
   cd APCR
   ```
3. 가상환경 생성 및 활성화
   ```bash
   # 프로젝트 상위 디렉토리에서
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```
4. 의존성 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

## 실행 방법

```bash
# 가상환경이 활성화된 상태에서
python main.py
```

## 프로젝트 구조

```
APCR/
├── data/               # 데이터베이스 파일
├── db/                 # 데이터베이스 관련 코드
│   ├── models/        # 데이터베이스 모델
│   └── migrations/    # 데이터베이스 마이그레이션
├── UI/                # 사용자 인터페이스
│   ├── components/    # 재사용 가능한 UI 컴포넌트
│   ├── layouts/       # 레이아웃 템플릿
│   ├── screens/       # 화면 구현
│   ├── styles/        # 스타일 정의
│   └── assets/        # 리소스 파일
└── main.py           # 메인 실행 파일
```

## 파일명 규칙

1. 모든 파일명은 영문 소문자로 작성
2. 단어 구분은 언더스코어(_) 사용
3. 파일 확장자 규칙:
   - Python 파일: `.py`
   - 설정 파일: `.ini`, `.json`, `.yaml`
   - 문서 파일: `.md`, `.txt`
   - 데이터베이스: `.db`
   - 로그 파일: `.log`

4. 디렉토리명 규칙:
   - 모든 디렉토리명은 영문 소문자
   - 특수문자 사용 금지
   - 의미있는 이름 사용

5. 예시:
   - `user_management.py`
   - `project_config.json`
   - `database_schema.sql`
   - `error_log.txt`

## 개발 환경 설정

1. IDE 설정
   - Python 인터프리터: 프로젝트의 가상환경 선택
   - 코드 포맷터: black
   - 린터: flake8

2. 개발 가이드라인
   - 코드 스타일: PEP 8 준수
   - 커밋 메시지: Conventional Commits 사용
   - 브랜치 전략: Git Flow 사용

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.