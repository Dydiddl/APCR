from datetime import datetime
import hashlib
import os

class User:
    def __init__(self, user_data=None):
        self.user_id = user_data.get('user_id') if user_data else None
        self.username = user_data.get('username', '')
        self.password_hash = user_data.get('password_hash', '')
        self.salt = user_data.get('salt', '')
        self.email = user_data.get('email', '')
        self.role = user_data.get('role', 'user')  # admin, manager, user
        self.is_active = user_data.get('is_active', True)
        self.last_login = user_data.get('last_login')
        self.created_at = user_data.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.updated_at = user_data.get('updated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'last_login': self.last_login,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def generate_salt():
        """랜덤 솔트 생성"""
        return os.urandom(32).hex()

    def set_password(self, password):
        """비밀번호 해시 생성"""
        self.salt = self.generate_salt()
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        """비밀번호 해시"""
        return hashlib.sha256((password + self.salt).encode()).hexdigest()

    def verify_password(self, password):
        """비밀번호 검증"""
        return self.password_hash == self.hash_password(password)

    def validate(self):
        """데이터 유효성 검증"""
        errors = []
        if not self.username:
            errors.append("사용자명은 필수입니다.")
        if not self.email:
            errors.append("이메일은 필수입니다.")
        if not self.password_hash:
            errors.append("비밀번호는 필수입니다.")
        return errors 