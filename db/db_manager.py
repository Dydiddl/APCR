import sqlite3
import os
from datetime import datetime
from .models.user import User

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'construction.db')
        self.init_db()
        
    def init_db(self):
        """데이터베이스 초기화"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 사용자 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')
            
            # 공사 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number TEXT NOT NULL,
                    name TEXT NOT NULL,
                    contract_date TEXT NOT NULL,
                    supply_amount REAL NOT NULL,  -- 공급가액
                    tax_amount REAL NOT NULL,     -- 부가세 (공급가액의 10%)
                    total_amount REAL NOT NULL,   -- 계약금액 (공급가액 + 부가세)
                    client TEXT NOT NULL,
                    note TEXT,
                    status TEXT DEFAULT 'ongoing'
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"데이터베이스 초기화 중 오류 발생: {str(e)}")
            
    def get_all_projects(self):
        """모든 공사 목록 조회"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects")
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'id': row[0],
                'number': row[1],
                'name': row[2],
                'contract_date': row[3],
                'supply_amount': row[4],
                'tax_amount': row[5],
                'total_amount': row[6],
                'client': row[7],
                'note': row[8],
                'status': row[9]
            } for row in rows]
        except Exception as e:
            print(f"공사 목록 조회 중 오류 발생: {str(e)}")
            return []
            
    def add_project(self, number, name, contract_date, supply_amount, client, note):
        """공사 추가"""
        try:
            tax_amount = supply_amount * 0.1  # 부가세 계산 (공급가액의 10%)
            total_amount = supply_amount + tax_amount  # 계약금액 계산
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO projects (
                    number, name, contract_date, supply_amount, tax_amount,
                    total_amount, client, note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (number, name, contract_date, supply_amount, tax_amount,
                 total_amount, client, note)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"공사 추가 중 오류 발생: {str(e)}")
            raise
            
    def update_project(self, project_id, number, name, contract_date, supply_amount, client, note):
        """공사 수정"""
        try:
            tax_amount = supply_amount * 0.1  # 부가세 계산 (공급가액의 10%)
            total_amount = supply_amount + tax_amount  # 계약금액 계산
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE projects SET
                    number = ?, name = ?, contract_date = ?, supply_amount = ?,
                    tax_amount = ?, total_amount = ?, client = ?, note = ?
                WHERE id = ?
                """,
                (number, name, contract_date, supply_amount, tax_amount,
                 total_amount, client, note, project_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"공사 수정 중 오류 발생: {str(e)}")
            raise
            
    def delete_project(self, project_id):
        """공사 삭제"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"공사 삭제 중 오류 발생: {str(e)}")
            raise
            
    def update_project_status(self, project_id, status):
        """공사 진행 상태 업데이트"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 프로젝트 존재 여부 확인
            cursor.execute("SELECT id FROM projects WHERE id = ?", (project_id,))
            if not cursor.fetchone():
                raise ValueError(f"프로젝트 ID {project_id}가 존재하지 않습니다.")
            
            # 상태 업데이트
            cursor.execute(
                "UPDATE projects SET status = ? WHERE id = ?",
                (status, project_id)
            )
            
            # 변경사항 확인
            if cursor.rowcount == 0:
                raise ValueError(f"프로젝트 상태 업데이트 실패: ID {project_id}")
                
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"공사 상태 업데이트 중 오류 발생: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            raise

    def get_connection(self):
        """데이터베이스 연결 반환"""
        return self.conn
        
    # 사용자 관련 메서드
    def add_user(self, user_data):
        """사용자 추가"""
        try:
            now = datetime.now().isoformat()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (
                    username, password_hash, salt, email, role,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['username'],
                user_data['password_hash'],
                user_data['salt'],
                user_data.get('email'),
                user_data['role'],
                now, now
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"사용자 추가 중 오류 발생: {str(e)}")
            raise
        
    def get_user(self, username):
        """사용자 조회"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'password_hash': row[2],
                    'salt': row[3],
                    'email': row[4],
                    'role': row[5],
                    'is_active': bool(row[6]),
                    'last_login': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                }
            return None
        except Exception as e:
            print(f"사용자 조회 중 오류 발생: {str(e)}")
            return None
        
    def update_user(self, user_id, user_data):
        """사용자 정보 수정"""
        try:
            now = datetime.now().isoformat()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET
                    email = ?,
                    role = ?,
                    is_active = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (
                user_data.get('email'),
                user_data.get('role'),
                user_data.get('is_active', True),
                now,
                user_id
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"사용자 정보 수정 중 오류 발생: {str(e)}")
            raise
        
    def delete_user(self, user_id):
        """사용자 삭제"""
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        
    def get_all_users(self):
        """모든 사용자 조회"""
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        return [{
            'id': row[0],
            'username': row[1],
            'password_hash': row[2],
            'salt': row[3],
            'email': row[4],
            'role': row[5],
            'is_active': bool(row[6]),
            'last_login': row[7],
            'created_at': row[8],
            'updated_at': row[9]
        } for row in rows]
        
    def verify_user(self, username, password):
        """사용자 인증: username과 password가 맞는지 확인"""
        user = self.get_user(username)
        if not user:
            return False
        import hashlib
        password_hash = hashlib.sha256((password + user['salt']).encode('utf-8')).hexdigest()
        return password_hash == user['password_hash']

    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close() 