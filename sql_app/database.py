
# 导入 SQLAlchemy 部件
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建数据库连接引擎-SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 创建数据库连接引擎-MySQL
# SQLALCHEMY_DATABASE_URL="mysql+pymysql://root:123456@localhost:3306/sql_app"

# 创建数据库连接引擎-PostgreSQL
# SQLALCHEMY_DATABASE_URL="postgresql://user:password@postgresserver/db"

# 创建数据库连接引擎-SQLServer
# SQLALCHEMY_DATABASE_URL="mssql+pymssql://scott:tiger@hostname:port/sql_app"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建数据库会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基本映射类
Base = declarative_base()

# 创建函数get_db，它返回一个数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()