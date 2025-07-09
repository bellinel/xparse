from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Подключение к SQLite (файл xpars.db в корне проекта)
SQLALCHEMY_DATABASE_URL = "sqlite:///xpars.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from .orm import Post  # Импортируем модель, чтобы она зарегистрировалась в metadata
    Base.metadata.create_all(bind=engine)
