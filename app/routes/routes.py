from flask import Blueprint, jsonify, request, url_for
from app.models.models import Business, Review
from app.db.db_config import connect_with_connector

routes_bp = Blueprint('routes', __name__)

_, Session = connect_with_connector()
# Session = connect_with_connector()

@app.route('/')
def index():
    return "Welcome to the ReviewSpot API using MySQL!"


@routes_bp.route('/businesses', methods=['POST'])
def create_business():
    data = request.get_json()
    required_fields = ['owner_id', 'name', 'street_address', 'city', 'state', 'zip_code']
    if not all(field in data for field in required_fields):
        return jsonify({'Error': 'The request body is missing at least one of the required attributes'}), 400

    with Session() as db_session:
        business = Business.create(db_session, data)
        db_session.commit()
        response = {
            'id': business.id,
            'owner_id': int(business.owner_id),
            'name': business.name,
            'street_address': business.street_address,
            'city': business.city,
            'state': business.state,
            'zip_code': int(business.zip_code),
            'self': url_for('routes.get_business', business_id=business.id, _external=True)
        }
        return jsonify(response), 201

@routes_bp.route('/businesses', methods=['GET'])
def get_businesses():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=3, type=int)

    with Session() as db_session:
        businesses = Business.list(db_session, offset, limit)
        total_count = Business.count(db_session)

    entries = []
    for business in businesses:
        entry = {
            'id': business.id,
            'owner_id': int(business.owner_id),
            'name': business.name,
            'street_address': business.street_address,
            'city': business.city,
            'state': business.state,
            'zip_code': int(business.zip_code),
            'self': url_for('routes.get_business', business_id=business.id, _external=True)
        }
        entries.append(entry)

    response = {
        'entries': entries,
        'count': len(entries)
    }

    if offset + limit < total_count:
        response['next'] = url_for('routes.get_businesses', offset=offset + limit, limit=limit, _external=True)

    return jsonify(response), 200

@routes_bp.route('/businesses/<int:business_id>', methods=['GET'])
def get_business(business_id):
    with Session() as db_session:
        business = Business.get(db_session, business_id)
    if business:
        response = {
            'id': int(business.id),
            'owner_id': int(business.owner_id),
            'name': business.name,
            'street_address': business.street_address,
            'city': business.city,
            'state': business.state,
            'zip_code': int(business.zip_code),
            'self': url_for('routes.get_business', business_id=business.id, _external=True)
        }
        return jsonify(response), 200
    else:
        return jsonify({'Error': 'No business with this business_id exists'}), 404
    # Session().close()

@routes_bp.route('/businesses/<int:business_id>', methods=['PUT'])
def update_business(business_id):
    data = request.get_json()
    required_fields = ['owner_id', 'name', 'street_address', 'city', 'state', 'zip_code']
    if not all(field in data for field in required_fields):
        return jsonify({'Error': 'The request body is missing at least one of the required attributes'}), 400

    with Session() as db_session:
        business = Business.get(db_session, business_id)
        if business:
            business = Business.update(db_session, business_id, data)
            response = {
                'id': int(business.id),
                'owner_id': int(business.owner_id),
                'name': business.name,
                'street_address': business.street_address,
                'city': business.city,
                'state': business.state,
                'zip_code': int(business.zip_code),
                'self': url_for('routes.get_business', business_id=business.id, _external=True)
            }
            return jsonify(response), 200
        else:
            return jsonify({'Error': 'No business with this business_id exists'}), 404

@routes_bp.route('/businesses/<int:business_id>', methods=['DELETE'])
def delete_business(business_id):
    with Session() as db_session:
        business = Business.get(db_session, business_id)
        if not business:
            return jsonify({'Error': 'No business with this business_id exists'}), 404
        Review.delete_by_business_id(db_session, business_id)
        db_session.delete(business)
        db_session.commit()
        return '', 204

@routes_bp.route('/owners/<int:owner_id>/businesses', methods=['GET'])
def get_businesses_by_owner(owner_id):
    with Session() as db_session:
        businesses = Business.list_by_owner(db_session, owner_id)

    if not businesses:
        return jsonify({'Error': 'No businesses found for this owner'}), 404

    response = []
    for business in businesses:
        business_data = {
            'id': business.id,
            'owner_id': int(business.owner_id),
            'name': business.name,
            'street_address': business.street_address,
            'city': business.city,
            'state': business.state,
            'zip_code': int(business.zip_code),
            'self': url_for('routes.get_business', business_id=business.id, _external=True)
        }
        response.append(business_data)

    return jsonify(response), 200

@routes_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    required_fields = ['user_id', 'business_id', 'stars']
    if not all(field in data for field in required_fields):
        return jsonify({'Error': 'The request body is missing at least one of the required attributes'}), 400
    
    with Session() as db_session:
        if not Business.exists(db_session, data['business_id']):
            return jsonify({'Error': 'No business with this business_id exists'}), 404
        
        if Review.exists_by_user_business(db_session, data['user_id'], data['business_id']):
            return jsonify({'Error': 'You have already submitted a review for this business. You can update your previous review, or delete it and submit a new review'}), 409
        
        review_data = {
            'user_id': data['user_id'],
            'business_id': data['business_id'],
            'stars': data['stars'],
            'review_text': data.get('review_text', '')
        }
        review_id = Review.create(db_session, review_data)
        review = Review.get(db_session, review_id)
        
        response = {
            'id': review.id,
            'user_id': review.user_id,
            'business_id': review.business_id,
            'stars': review.stars,
            'review_text': review.review_text,
            'self': url_for('routes.get_review', review_id=review.id, _external=True),
            'business': url_for('routes.get_business', business_id=review.business_id, _external=True)
        }
        
        return jsonify(response), 201

@routes_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    with Session() as db_session:
        review = Review.get(db_session, review_id)
        if not review or not review.business:
            return jsonify({'Error': 'No review with this review_id exists'}), 404
        
        response = {
            'id': review.id,
            'user_id': review.user_id,
            'business_id': review.business_id,
            'stars': review.stars,
            'review_text': review.review_text or '',
            'self': url_for('routes.get_review', review_id=review.id, _external=True),
            'business': url_for('routes.get_business', business_id=review.business_id, _external=True)
        }
        
        return jsonify(response), 200

@routes_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    if 'stars' not in data:
        return jsonify({'Error': 'The request body is missing at least one of the required attributes'}), 400
    
    with Session() as db_session:
        review = Review.get(db_session, review_id)
        if not review:
            return jsonify({'Error': 'No review with this review_id exists'}), 404
        
        review.stars = data['stars']
        review.review_text = data.get('review_text', review.review_text)
        db_session.commit()
        
        response = {
            'id': review.id,
            'user_id': review.user_id,
            'business_id': review.business_id,
            'stars': review.stars,
            'review_text': review.review_text,
            'self': url_for('routes.get_review', review_id=review.id, _external=True),
            'business': url_for('routes.get_business', business_id=review.business_id, _external=True)
        }
        
        return jsonify(response), 200

@routes_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    with Session() as db_session:
        review = Review.get(db_session, review_id)
        if not review:
            return jsonify({'Error': 'No review with this review_id exists'}), 404
        
        db_session.delete(review)
        db_session.commit()
        
        return '', 204

@routes_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    with Session() as db_session:
        reviews = Review.list_by_user(db_session, user_id)
        if not reviews:
            return jsonify({'Error': 'No reviews found for this user'}), 404
        response = []
        for review in reviews:
            review_data = {
                'id': review.id,
                'user_id': review.user_id,
                'business_id': review.business_id,
                'stars': review.stars,
                'review_text': review.review_text or '',
                'self': url_for('routes.get_review', review_id=review.id, _external=True),
                'business': url_for('routes.get_business', business_id=review.business_id, _external=True)
            }
            response.append(review_data)
    
        return jsonify(response), 200