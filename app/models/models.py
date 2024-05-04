from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Business(Base):
    __tablename__ = 'businesses'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    address = Column(String(100))
    phone = Column(String(20))
    owner_id = Column(String(50), nullable=False)

    reviews = relationship('Review', back_populates='business')

    @classmethod
    def list_by_owner(cls, db, owner_id):
        return db.query(cls).filter_by(owner_id=owner_id).all()

    @classmethod
    def create(cls, db, data):
        business = cls(**data)
        db.add(business)
        db.commit()
        return business.id

    @classmethod
    def get(cls, db, business_id):
        return db.query(cls).get(business_id)

    @classmethod
    def list(cls, db):
        return db.query(cls).all()

    @classmethod
    def update(cls, db, business_id, data):
        business = db.query(cls).get(business_id)
        if business:
            for key, value in data.items():
                setattr(business, key, value)
            db.commit()
        return business

    @classmethod
    def delete(cls, db, business_id):
        business = db.query(cls).get(business_id)
        if business:
            db.delete(business)
            db.commit()
            return True
        return False

    @classmethod
    def exists(cls, db, business_id):
        return db.query(cls).filter_by(id=business_id).first() is not None

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    user_id = Column(String(50), nullable=False)

    business = relationship('Business', back_populates='reviews')

    @classmethod
    def create(cls, db, data):
        review = cls(**data)
        db.add(review)
        db.commit()
        return review.id

    @classmethod
    def exists_by_id(cls, db, review_id):
        return db.query(cls).filter_by(id=review_id).first() is not None

    @classmethod
    def exists_by_user_business(cls, db, user_id, business_id):
        return db.query(cls).filter_by(user_id=user_id, business_id=business_id).first() is not None

    @classmethod
    def get(cls, db, review_id):
        return db.query(cls).get(review_id)

    @classmethod
    def list_by_user(cls, db, user_id):
        return db.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def update(cls, db, review_id, data):
        review = db.query(cls).get(review_id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            db.commit()
        return review

    @classmethod
    def delete(cls, db, review_id):
        review = db.query(cls).get(review_id)
        if review:
            db.delete(review)
            db.commit()
            return True
        return False

    @classmethod
    def delete_by_business(cls, db, business_id):
        db.query(cls).filter_by(business_id=business_id).delete()
        db.commit()