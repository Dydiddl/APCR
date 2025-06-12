# API 문서

## 데이터베이스 관리자 (DatabaseManager)

### 사용자 관리

#### add_user(user_data)
새로운 사용자를 추가합니다.

**Parameters:**
- `user_data` (dict): 사용자 정보
  - `username` (str): 사용자 이름
  - `password_hash` (str): 해시된 비밀번호
  - `salt` (str): 비밀번호 솔트
  - `email` (str, optional): 이메일 주소
  - `role` (str): 사용자 역할

#### get_user(username)
사용자 정보를 조회합니다.

**Parameters:**
- `username` (str): 조회할 사용자 이름

**Returns:**
- `dict`: 사용자 정보 또는 None

### 프로젝트 관리

#### add_project(project_data)
새로운 프로젝트를 추가합니다.

**Parameters:**
- `project_data` (dict): 프로젝트 정보
  - `code` (str): 프로젝트 코드
  - `name` (str): 프로젝트 이름
  - `client` (str): 클라이언트
  - `contract_date` (str): 계약일
  - `amount` (float): 계약금액
  - `status` (str): 프로젝트 상태
  - `location` (str, optional): 프로젝트 위치
  - `description` (str, optional): 프로젝트 설명

#### get_project(project_id)
프로젝트 정보를 조회합니다.

**Parameters:**
- `project_id` (int): 조회할 프로젝트 ID

**Returns:**
- `dict`: 프로젝트 정보 또는 None

### 계약 관리

#### add_contract(contract_data)
새로운 계약을 추가합니다.

**Parameters:**
- `contract_data` (dict): 계약 정보
  - `code` (str): 계약 코드
  - `name` (str): 계약 이름
  - `contractor` (str): 계약자
  - `contract_date` (str): 계약일
  - `amount` (float): 계약금액
  - `status` (str): 계약 상태
  - `description` (str, optional): 계약 설명

#### get_contract(contract_id)
계약 정보를 조회합니다.

**Parameters:**
- `contract_id` (int): 조회할 계약 ID

**Returns:**
- `dict`: 계약 정보 또는 None 