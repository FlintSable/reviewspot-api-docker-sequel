from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Business(Base):
    __tablename__ = 'businesses'

    id = Column(Integer, primary_key=True)
    owner_id = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    street_address = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(5), nullable=False)

    reviews = relationship('Review', back_populates='business')

    @classmethod
    def list_by_owner(cls, db_session, owner_id):
        return db_session.query(cls).filter_by(owner_id=owner_id).all()

    @classmethod
    def create(cls, db_session, data):
        business = cls(**data)
        db_session.add(business)
        db_session.commit()
        print(business.id)
        return business

    @classmethod
    def get(cls, db_session, business_id):
        return db_session.query(cls).get(business_id)

    @classmethod
    def list(cls, db_session, offset=0, limit=10):
        return db_session.query(cls).offset(offset).limit(limit).all()

    @classmethod
    def count(cls, db_session):
        return db_session.query(cls).count()

    @classmethod
    def update(cls, db_session, business_id, data):
        business = db_session.query(cls).get(business_id)
        if business:
            for key, value in data.items():
                setattr(business, key, value)
            db_session.commit()
        return business

    @classmethod
    def delete(cls, db_session, business_id):
        business = db_session.query(cls).get(business_id)
        if business:
            db_session.delete(business)
            db_session.commit()
            return True
        return False

    @classmethod
    def exists(cls, db_session, business_id):
        return db_session.query(cls).filter_by(id=business_id).first() is not None

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    user_id = Column(String(50), nullable=False)

    business = relationship('Business', back_populates='reviews')

    @classmethod
    def create(cls, db_session, data):
        review = cls(**data)
        db_session.add(review)
        db_session.commit()
        return review.id

    @classmethod
    def exists_by_id(cls, db_session, review_id):
        return db_session.query(cls).filter_by(id=review_id).first() is not None

    @classmethod
    def exists_by_user_business(cls, db_session, user_id, business_id):
        return db_session.query(cls).filter_by(user_id=user_id, business_id=business_id).first() is not None

    @classmethod
    def get(cls, db_session, review_id):
        return db_session.query(cls).get(review_id)

    @classmethod
    def list_by_user(cls, db_session, user_id):
        return db_session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def update(cls, db_session, review_id, data):
        review = db_session.query(cls).get(review_id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            db_session.commit()
        return review

    @classmethod
    def delete(cls, db_session, review_id):
        review = db_session.query(cls).get(review_id)
        if review:
            db_session.delete(review)
            db_session.commit()
            return True
        return False

    @classmethod
    def delete_by_business(cls, db_session, business_id):
        db_session.query(cls).filter_by(business_id=business_id).delete()
        db_session.commit()