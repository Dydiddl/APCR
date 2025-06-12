from datetime import datetime

class Project:
    def __init__(self, project_data=None):
        if project_data:
            self.project_id = project_data.get('project_id')
            self.project_code = project_data.get('project_code')
            self.project_name = project_data.get('project_name')
            self.client_name = project_data.get('client_name')
            self.contract_date = project_data.get('contract_date')
            self.start_date = project_data.get('start_date')
            self.end_date = project_data.get('end_date')
            self.contract_amount = project_data.get('contract_amount')
            self.status = project_data.get('status')
            self.location = project_data.get('location')
            self.description = project_data.get('description')
            self.created_at = project_data.get('created_at')
            self.updated_at = project_data.get('updated_at')
        else:
            self.project_id = None
            self.project_code = None
            self.project_name = None
            self.client_name = None
            self.contract_date = None
            self.start_date = None
            self.end_date = None
            self.contract_amount = None
            self.status = None
            self.location = None
            self.description = None
            self.created_at = None
            self.updated_at = None

    def to_dict(self):
        """프로젝트 데이터를 딕셔너리로 변환"""
        return {
            'project_id': self.project_id,
            'project_code': self.project_code,
            'project_name': self.project_name,
            'client_name': self.client_name,
            'contract_date': self.contract_date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'contract_amount': self.contract_amount,
            'status': self.status,
            'location': self.location,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def from_db_row(row):
        """데이터베이스 행을 Project 객체로 변환"""
        if not row:
            return None
        
        return Project({
            'project_id': row[0],
            'project_code': row[1],
            'project_name': row[2],
            'client_name': row[3],
            'contract_date': row[4],
            'start_date': row[5],
            'end_date': row[6],
            'contract_amount': row[7],
            'status': row[8],
            'location': row[9],
            'description': row[10],
            'created_at': row[11],
            'updated_at': row[12]
        })

    def validate(self):
        """프로젝트 데이터 유효성 검사"""
        errors = []
        
        if not self.project_code:
            errors.append("공사번호는 필수입니다.")
        if not self.project_name:
            errors.append("공사명은 필수입니다.")
        if not self.client_name:
            errors.append("발주처는 필수입니다.")
        if not self.contract_date:
            errors.append("계약일자는 필수입니다.")
        if not self.contract_amount:
            errors.append("계약금액은 필수입니다.")
        if not self.status:
            errors.append("상태는 필수입니다.")
            
        return errors 