import pandas as pd
import os
import sys
from datetime import datetime
import logging
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from database.db_manager import DatabaseManager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration.log'),
        logging.StreamHandler()
    ]
)

def migrate_excel_to_sqlite():
    """
    Excel 파일의 데이터를 SQLite 데이터베이스로 마이그레이션합니다.
    """
    try:
        # Excel 파일 경로 설정
        excel_path = os.path.join(project_root, 'resources', '1_data', '1_construction', 'construction.xlsx')
        
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel 파일을 찾을 수 없습니다: {excel_path}")

        # 데이터베이스 매니저 초기화
        db = DatabaseManager()
        
        # 테이블 생성
        db.init_db()
        logging.info("데이터베이스 테이블 생성 완료")

        # Excel 파일 읽기
        df = pd.read_excel(excel_path)
        logging.info(f"Excel 파일 읽기 완료: {len(df)} 행")

        # 각 행을 데이터베이스에 추가
        success_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # 프로젝트 데이터 준비
                project_data = {
                    'code': str(row.get('프로젝트코드', '')),
                    'name': str(row.get('프로젝트명', '')),
                    'client': str(row.get('발주처', '')),
                    'contract_date': str(row.get('계약일자', '')),
                    'amount': float(row.get('계약금액', 0)),
                    'status': str(row.get('상태', '진행중')),
                    'location': str(row.get('위치', '')),
                    'description': str(row.get('설명', '')),
                }

                # 데이터베이스에 추가
                db.add_project(project_data)
                success_count += 1
                logging.info(f"프로젝트 추가 성공: {project_data['name']}")

            except Exception as e:
                error_count += 1
                logging.error(f"행 {index + 2} 처리 중 오류 발생: {str(e)}")

        # 마이그레이션 결과 로깅
        logging.info(f"마이그레이션 완료: 성공 {success_count}건, 실패 {error_count}건")

    except Exception as e:
        logging.error(f"마이그레이션 중 오류 발생: {str(e)}")
        raise

if __name__ == "__main__":
    migrate_excel_to_sqlite() 