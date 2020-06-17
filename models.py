from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, Float, ForeignKey
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB"}

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Asin(BaseModel):
    asin = Column(VARCHAR(10), nullable=False, unique=True)

    def __init__(self, asin):
        self.asin = asin


class ProductInfo(BaseModel):
    __tablename__ = 'product_info'

    asin_id = Column(Integer, ForeignKey(Asin.__name__.lower() + ".id", ondelete="CASCADE"), nullable=False, index=True)
    asin = relationship(Asin.__name__)
    title = Column(VARCHAR(1000), nullable=False)
    rating = Column(Float, nullable=False)
    ratings_count = Column(Integer, nullable=False)

    def __init__(self, asin, title, rating, ratings_count):
        self.asin = asin
        self.title = title
        self.rating = rating
        self.ratings_count = ratings_count


class Review(BaseModel):
    asin_id = Column(Integer, ForeignKey(Asin.__name__.lower() + ".id", ondelete="CASCADE"), nullable=False, index=True)
    asin = relationship(Asin.__name__)
    total_reviews = Column(Integer, nullable=False)
    positive_reviews = Column(Integer, nullable=False)
    answered_questions = Column(Integer, nullable=False)

    def __init__(self, asin, total_reviews, positive_reviews, answered_questions):
        self.asin = asin
        self.total_reviews = total_reviews
        self.positive_reviews = positive_reviews
        self.answered_questions = answered_questions

