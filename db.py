import mysql.connector

# MySQL 配置
db_config = {
    'host': 'localhost',
    'user': 'Narcisuss',
    'password': '688376',
    'database': 'student_management'
}

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None
