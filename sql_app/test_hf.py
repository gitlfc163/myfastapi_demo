# 实现一个使用sqlalchemy框架的数据库连接类

# 导入模块
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 定义数据库连接类
class DB_CONN():
    def __init__(self, db_type, db_host, db_port, db_user, db_pwd, db_name):
        # 定义数据库连接信息
        self.db_type = db_type
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_pwd = db_pwd
        self.db_name = db_name
        
    def get_engine(self):
        # 定义数据库连接引擎
        engine = create_engine(
            self.db_type +
            "://" +
            self.db_user +
            ":" +
            self.db_pwd +
            "@" +
            self.db
            
        )
        return engine

    def get_session(self):
        # 定义数据库连接会话
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


    