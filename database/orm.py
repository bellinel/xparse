from sqlalchemy import Column, Integer, String
from database.engine import Base
from database.engine import SessionLocal

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    tweet = Column(String, nullable=False)
    image = Column(String, nullable=True)
    date = Column(String, nullable=True)

def add_post(nickname: str, tweet: str, image: str, date: str):
    session = SessionLocal()
    try:
        exists = session.query(Post).filter_by(nickname=nickname, tweet=tweet).first()
        if exists:
            print(f"Пост {nickname} уже существует")
            return None
        post = Post(nickname=nickname, tweet=tweet, image=image, date=date)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post
    finally:
        session.close()
