from flask import Flask,jsonify,make_response,request
from models import db,Product,Category,User,Profile,check_password_hash
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token
from flask_cors import CORS
jwt=JWTManager()
app = Flask(__name__)
CORS(app)
CORS(app, origins="http://localhost:5173")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']='ce9c319963b03c423e9de79b'

# Initialize SQLAlchemy with the Flask app
db.init_app(app)
jwt.init_app(app)
# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet directory!</h1>',
        200
    )
    return response

@app.route('/categories')
def get_categories():
    categories = Category.query.all()
    serialized_categories = [category.to_dict() for category in categories]
    response=make_response(serialized_categories,200)
    return response
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    serialized_products = [product.to_dict() for product in products]
    response = make_response(jsonify({'products': serialized_products}), 200)
    return response
@app.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = category.products
    serialized_products = [product.to_dict() for product in products]
    response=make_response(serialized_products,200)
    return response
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    fullname = data.get('fullname')
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        response="username already exists"
        return make_response(response,400)
    
    # Create new user
    user = User(username=username, password=password)
    
    # Add user to the session
    db.session.add(user)
    
    db.session.commit()
    #create user profile
    profile = Profile(fullname=fullname, user_id=user.id)
    db.session.add(profile)
    db.session.commit()
    
    return jsonify({'message': 'User and profile created successfully'}), 201
@app.route('/login',methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter(User.username==username).first()

    if user and user.password:
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        response_data = {
            'message': 'logged in',
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return make_response(jsonify(response_data), 200)
    else:
        response = 'Invalid username or password'
        return make_response(response, 401)
    
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Query the user by user_id
    user = User.query.get(user_id)
    
    # Check if the user exists
    if not user:
        response="User not found"

        return make_response(response,404)
    # Delete the user's profile
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile:
        db.session.delete(profile)
    
    # Delete the user
    db.session.delete(user)
    
    # Commit the session
    db.session.commit()
    response="User and profile deleted successfully"
    return make_response(response,200)
@app.route('/change-username/<int:user_id>', methods=['PUT'])
def change_username(user_id):
    data = request.json
    new_username = data.get('new_username')
    
    user = User.query.get(user_id)
    if not user:
        response="User not found"
        return make_response(response,404)
    
    user.username = new_username
    db.session.commit()
    response="username changed successfuly"
    return make_response(response,200)
@app.route('/add-to-favorites', methods=['POST'])
def add_to_favorites():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    user.products.append(product)
    db.session.commit()
    
    return jsonify({'message': 'Product added to favorites'}), 201

@app.route('/remove-from-favorites/<int:user_id>/<int:product_id>', methods=['DELETE'])
def remove_from_favorites(user_id, product_id):
    user = User.query.get(user_id)
    product = Product.query.get(product_id)

    if not user:
        return make_response(jsonify({'message': 'User not found'}), 404)
    if not product:
        return make_response(jsonify({'message': 'Product not found'}), 404)

    if product in user.products:
        user.products.remove(product)
        db.session.commit()
        return jsonify({'message': 'Product removed from favorites successfully'}), 200
    else:
        return make_response(jsonify({'message': 'Product is not in favorites'}), 400)
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'message': 'User not found'}), 404)
    
    serialized_user = user.to_dict()
    return make_response(jsonify(serialized_user), 200)

if __name__=="__main__":
     app.run(port=5550,)