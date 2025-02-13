from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

##########################################################################
# MODELS
##########################################################################

# Association table for many-to-many relationship
user_group = db.Table(
    'user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

# User Model
class User(db.Model):
    def __repr__(self):
        return f'<User {self.username}>'
    
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user_icon = db.Column(db.LargeBinary)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    groups = db.relationship('Group', secondary=user_group, back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# Group Model
class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    group_icon = db.Column(db.LargeBinary)
    group_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    users = db.relationship('User', secondary=user_group, back_populates='groups')
    events = db.relationship('Event', back_populates='group', cascade="all, delete-orphan")

# Event Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.Text)
    event_icon = db.Column(db.LargeBinary)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))
    cost_to_attend = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    location = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    photos = db.Column(db.LargeBinary)
    visibility = db.Column(db.Enum('Public', 'Private', name='visibility'))
    category = db.Column(db.Enum('Category1', 'Category2', 'Category3', 'Category4', 'Category5', name='category'))
    id_discussion_thread = db.Column(db.Integer, db.ForeignKey('discussion_thread.id'))

    # Foreign key to tie the event to a group
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    # Define relationship
    group = db.relationship('Group', back_populates='events')

    # One-to-Many Relationship with Expense
    expenses = db.relationship('Expense', back_populates='event', cascade="all, delete-orphan")


# Expense Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    amount = db.Column(db.Float)
    amount_paid = db.Column(db.Float)
    amount_remaining = db.Column(db.Float)
    currency = db.Column(db.String(10))

    # Foreign Key to Event
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    # Foreign Key for Expense Owner (User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    event = db.relationship('Event', back_populates='expenses')
    owner = db.relationship('User', backref='owned_expenses')

# ExpenseSplit Model
class ExpenseSplit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_owed = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, default=0)
    algorithm_used = db.Column(db.Enum('equally', 'percentage', 'custom', name='algorithm_type'))

    # Add explicit constraint names
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_expensesplit_user"), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id', name="fk_expensesplit_expense"), nullable=False)

    # Relationships
    user = db.relationship('User', backref='expense_splits')
    expense = db.relationship('Expense', backref='splits')


# Notification Model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    message = db.Column(db.Text)
    is_viewed = db.Column(db.Boolean, default=False)

# Discussion Thread Model
class DiscussionThread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='thread', lazy=True)

# Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('discussion_thread.id'))

##########################################################################
# ROUTES
##########################################################################

# USER ROUTES
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User {data['username']} created successfully!"}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by ID"""
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "email": user.email})
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user.username} deleted successfully!"})
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    old_user_name = user.username
    data = request.json

    # Update username (if provided)
    if "username" in data:
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already exists"}), 400
        user.username = data["username"]

    # Update email (if provided)
    if "email" in data:
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already in use"}), 400
        user.email = data["email"]

    # Update password (if provided)
    if "password" in data:
        user.password_hash = generate_password_hash(data["password"])

    # Commit changes to the database
    db.session.commit()

    return jsonify({
        "message": f"User {old_user_name} updated successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "updated_at": user.updated_at
        }
    }), 200

######################################################################################
# GROUP ROUTES

@app.route('/groups', methods=['POST'])
def create_group():
    """Create a new group"""
    data = request.json
    group = Group(group_name=data['group_name'], description=data.get('description'))
    db.session.add(group)
    db.session.commit()
    return jsonify({"message": f"Group {data['group_name']} created successfully!", "group_id": group.id}), 201

@app.route('/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """Retrieve a group by ID"""
    group = Group.query.get(group_id)
    if group:
        group_dict = {key: value for key, value in group.__dict__.items() if not key.startswith('_')}
        return jsonify(group_dict)
    return jsonify({"error": "Group not found"}), 404

@app.route('/groups/<int:group_id>/add_users', methods=['POST'])
def add_users_to_group(group_id):
    """Add multiple users to a group"""
    data = request.json
    user_ids = data.get('user_ids', [])

    if not user_ids:
        return jsonify({"error": "No user IDs provided"}), 400

    group = Group.query.get(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    added_users = []
    already_in_group = []

    # Iterate over the user_ids and attempt to add them
    for user_id in user_ids:
        user = User.query.get(user_id)

        if not user:
            continue  # Skip invalid user IDs

        if user in group.users:
            already_in_group.append(user.username)
        else:
            group.users.append(user)
            added_users.append(user.username)

    if added_users:
        db.session.commit()

    response = {}

    if added_users:
        response["added_users"] = added_users
    if already_in_group:
        response["already_in_group"] = already_in_group

    if not added_users and not already_in_group:
        return jsonify({"error": "No valid users to add"}), 400

    return jsonify(response), 200

@app.route('/groups/<int:group_id>/members', methods=['GET'])
def get_group_members(group_id):
    """Retrieve all users in a group"""
    group = Group.query.get(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    members = [
        {"id": user.id, "username": user.username, "email": user.email}
        for user in group.users
    ]

    return jsonify({"group_id": group.id, "group_name": group.group_name, "members": members}), 200

######################################################################################
# EVENTS ROUTES

@app.route('/groups/<int:group_id>/events', methods=['POST'])
def create_event_for_group(group_id):
    """Create an event for a specific group"""
    group = Group.query.get(group_id)
    
    if not group:
        return jsonify({"error": "Group not found"}), 404

    data = request.json
    event = Event(
        event_name=data['event_name'],
        description=data['description'],
        event_type=data.get('event_type'),
        location=data.get('location'),
        visibility = data.get('visibility'),
        date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'),
        group_id=group.id
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        "message": f"Event created for group {group.group_name}!",
        "event_id": event.id
    }), 201

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Retrieve an event by ID"""
    event = Event.query.get(event_id)
    if event:
        event_dict = {key: value for key, value in event.__dict__.items() if not key.startswith('_')}

        # add group_name field
        join_result = db.session.query(Event, Group.group_name)\
                                .join(Group, Event.group_id == Group.id)\
                                .filter(Event.id == event_id)\
                                .first()
        event_dict["group_name"] = join_result[1]

        return jsonify(event_dict)
    return jsonify({"error": "Event not found"}), 404

@app.route('/groups/<int:group_id>/events', methods=['GET'])
def get_group_events(group_id):
    """Retrieve all events for a given group"""
    group = Group.query.get(group_id)

    if not group:
        return jsonify({"error": "Group not found"}), 404

    events = [
        {
            "id": event.id,
            "event_name": event.event_name,
            "description": event.description,
            "event_type": event.event_type,
            "location": event.location,
            "visibility": event.visibility,
            "date": event.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        for event in group.events
    ]

    return jsonify({
        "group_id": group.id,
        "group_name": group.group_name,
        "events": events
    }), 200

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an existing event"""
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.json

    # Update only the fields provided in the request
    if "event_name" in data:
        event.event_name = data["event_name"]
    if "description" in data:
        event.description = data["description"]
    if "event_type" in data:
        event.event_type = data["event_type"]
    if "location" in data:
        event.location = data["location"]
    if "date" in data:
        try:
            event.date = datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400
    if "cost_to_attend" in data:
        event.cost_to_attend = data["cost_to_attend"]
    if "visibility" in data:
        event.visibility = data["visibility"]
    if "category" in data:
        event.category = data["category"]

    # Save updates to database
    db.session.commit()

    return jsonify({
        "message": f"Event {event.id} updated successfully!",
        "event": {
            "id": event.id,
            "event_name": event.event_name,
            "description": event.description,
            "event_type": event.event_type,
            "location": event.location,
            "date": event.date.strftime('%Y-%m-%d %H:%M:%S'),
            "cost_to_attend": event.cost_to_attend,
            "visibility": event.visibility,
            "category": event.category
        }
    }), 200

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event by ID"""
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": f"Event {event_id} deleted successfully!"}), 200

# Route to invite a user to an event
@app.route('/events/<int:event_id>/invite', methods=['POST'])
def invite_user_to_event(event_id):
    """ To add a user to the group tied to the event"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    user = User.query.get(user_id)
    event = Event.query.get(event_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    elif not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Get the group tied to the event
    group = event.group
    
    if user in group.users:
        return jsonify({"message": f"User {user.username} is already in the event"})
    
    group.users.append(user)
    db.session.commit()
    return jsonify({"message": f"User {user.username} invited successfully to event {event.event_name}"})


# Route to get all events a user has joined
@app.route('/users/<int:user_id>/events', methods=['GET'])
def get_user_events(user_id):
    """Get all the groups tied to events where a user is"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    events = []
    for group in user.groups:
        if group.events:
            for event in group.events:
                events.append({
                    "id": event.id,
                    "event_name": event.event_name,
                    "description": event.description,
                    "date": event.date.strftime('%Y-%m-%d %H:%M:%S'),
                    "location": event.location
                })
    
    return jsonify({"events": events})

######################################################################################
# EXPENSES ROUTES

@app.route('/events/<int:event_id>/expenses', methods=['POST'])
def create_expense(event_id):
    """Create an expense tied to an event"""
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.json

    # Fetch the user tied to the expense
    owner_id = data['owner_id']
    owner = User.query.get(owner_id)
    if not owner:
        return jsonify({"error": f"User to tie to expense not found, ID {owner_id} invalid"}), 404

    expense = Expense(
        description=data['description'],
        amount=data['amount'],
        currency=data['currency'],
        amount_paid=data.get('amount_paid', 0),
        amount_remaining=data.get('amount', 0) - data.get('amount_paid', 0),
        event_id=event.id,  # Link expense to event
        owner=owner    
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify({
        "message": f"Expense created for event {event_id} on user {owner.username}!",
        "expense_id": expense.id
    }), 201

@app.route('/expenses/<int:expense_id>/split', methods=['POST'])
def create_expense_split(expense_id):
    """Create an expense split for users tied to the event"""
    expense = Expense.query.get(expense_id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    # Get event associated with the expense
    event = Event.query.get(expense.event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Get the group associated with the event
    group = event.group

    # Get the instance of the owner of the expense
    owner = expense.owner

    data = request.json
    # Get the list of user IDs involved in this expense split
    user_ids = data.get('user_ids')
    if not user_ids:
        return jsonify({"error": "User IDs are required"}), 400

    # Ensure that all user IDs are valid and belong to the group
    users_in_group = [user.id for user in group.users]
    invalid_users = [user_id for user_id in user_ids if user_id not in users_in_group]
    
    if invalid_users:
        return jsonify({"error": f"The following users are not part of the group: {', '.join(map(str, invalid_users))}"}), 400

    # Ensure the algorithm is provided and valid
    algorithm = data.get('algorithm')
    if algorithm not in ['equally', 'percentage', 'custom']:
        return jsonify({"error": "Invalid algorithm. Use 'equally', 'percentage', or 'custom'."}), 400

    total_amount = expense.amount
    total_paid = expense.amount_paid
    remaining_amount = total_amount - total_paid

    if algorithm == 'equally':
        # Split the remaining amount equally among the users
        split_amount = remaining_amount / len(user_ids)
        for user_id in user_ids:
            if user_id == owner.id:
                # The owner of the expense has already paid his own
                amount_paid = split_amount
                expense.amount_remaining -= split_amount
                expense.amount_paid += split_amount
            
            else:
                amount_paid = 0

            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount_owed=split_amount,
                amount_paid = amount_paid,
                algorithm_used=algorithm
            )
            db.session.add(split)

    elif algorithm == 'percentage':
        # Users will provide their percentage for the split
        total_percentage = 100
        for user_data in data.get('user_data', []):  # user_data should include 'user_id' and 'percentage'
            user_id = user_data.get('user_id')
            percentage = user_data.get('percentage')
            if user_id not in user_ids:
                return jsonify({"error": f"User {user_id} is not in the concerned user list"}), 400
            if percentage < 0 or percentage > 100:
                return jsonify({"error": f"Invalid percentage {percentage} for user {user_id}"}), 400
            amount_owed = (percentage / total_percentage) * remaining_amount

            if user_id == owner.id:
                # The owner of the expense has already paid his own
                amount_paid = amount_owed
                expense.amount_remaining -= amount_paid
                expense.amount_paid += amount_paid
            
            else:
                amount_paid = 0
            
            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount_owed=amount_owed,
                amount_paid = amount_paid,
                algorithm_used=algorithm
            )
            db.session.add(split)

    elif algorithm == 'custom':
        # Users will provide their custom amounts for the split
        for user_data in data.get('user_data', []):  # user_data should include 'user_id' and 'amount'
            user_id = user_data.get('user_id')
            amount = user_data.get('amount')
            if user_id not in user_ids:
                return jsonify({"error": f"User {user_id} is not in the concerned user list"}), 400
            if amount < 0 or amount > remaining_amount:
                return jsonify({"error": f"Invalid amount {amount} for user {user_id}"}), 400
            
            if user_id == owner.id:
                # The owner of the expense has already paid his own
                amount_paid = amount
                expense.amount_remaining -= amount
                expense.amount_paid += amount
            
            else:
                amount_paid = 0

            split = ExpenseSplit(
                expense_id=expense.id,
                user_id=user_id,
                amount_owed=amount,
                amount_paid = amount_paid,
                algorithm_used=algorithm
            )
            db.session.add(split)

    db.session.commit()

    return jsonify({
        "message": "Expense split created successfully!",
        "expense_id": expense.id,
        "user_ids": user_ids,
        "algorithm_used": algorithm
    }), 201


# Route to get what each user owes
@app.route('/expenses/<int:expense_id>/split_summary', methods=['GET'])
def get_expense_split(expense_id):
    """Retrieve the split details for an expense"""
    expense = Expense.query.get(expense_id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    
    # Fetch the owner of the Expense
    owner = expense.owner
    splits = ExpenseSplit.query.filter_by(expense_id=expense_id).all()

    split_summary = [
        {
            "user_id": split.user_id,
            "amount_owed": split.amount_owed,
            "amount_paid": split.amount_paid,
            "algorithm_used": split.algorithm_used,
            "owed_to": owner.username
        }
        for split in splits
    ]

    return jsonify({
        "expense_id": expense.id,
        "total_amount": expense.amount,
        "split_summary": split_summary
    }), 200

@app.route('/expenses/<int:expense_id>/user/<int:user_id>/split', methods=['GET'])
def get_user_split_for_expense(expense_id, user_id):
    """Retrieve how much a specific user owes in a specific expense"""
    expense = Expense.query.get(expense_id)

    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    
     # Fetch the owner of the Expense
    owner = expense.owner

    # Find the specific expense split for the user
    split = ExpenseSplit.query.filter_by(expense_id=expense_id, user_id=user_id).first()

    if not split:
        return jsonify({"error": "User has not been assigned a split for this expense"}), 404

    return jsonify({
        "expense_id": expense.id,
        "user_id": user_id,
        "amount_owed": split.amount_owed,
        "amount_paid": split.amount_paid,
        "amount_to_pay": split.amount_owed - split.amount_paid,
        "algorithm_used": split.algorithm_used,
        "owed_to": owner.username
    }), 200

@app.route('/expenses/<int:expense_id>/user/<int:user_id>/pay', methods=['POST'])
def pay_expense(expense_id, user_id):
    """Allow a user to pay part or all of their owed amount for an expense"""
    data = request.get_json()
    payment_amount = data.get("amount")

    if payment_amount is None or payment_amount <= 0:
        return jsonify({"error": "Invalid payment amount"}), 400

    # Fetch the expense
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    
    # Fetch the owner of the Expense among users
    owner = expense.owner

    # Fetch the expense split record for the user
    split = ExpenseSplit.query.filter_by(expense_id=expense_id, user_id=user_id).first()
    if not split:
        return jsonify({"error": "User has not been assigned a split for this expense"}), 404

    # Check if the user is trying to overpay
    if payment_amount > split.amount_owed:
        return jsonify({"error": "Payment exceeds amount owed"}), 400

    # Deduct the payment from user's owed amount
    split.amount_owed -= payment_amount
    split.amount_paid += payment_amount

    # Deduct from total remaining expense amount
    expense.amount_remaining -= payment_amount
    expense.amount_paid += payment_amount

    # Commit changes to database
    db.session.commit()

    return jsonify({
        "message": f"Payment successful to {owner.username}",
        "expense_id": expense.id,
        "user_id": user_id,
        "amount_paid": payment_amount,
        "remaining_amount_owed": split.amount_owed,
        "total_remaining_expense": expense.amount_remaining,
        "paying_to": owner.username
    }), 200


@app.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """Retrieve an expense by ID"""
    expense = Expense.query.get(expense_id)
    if expense:
        owner = User.query.get(expense.owner.id)
        return jsonify({"id": expense.id, "description": expense.description,"owner": owner.username , "amount_remaining": expense.amount_remaining, "amount_paid":expense.amount_paid})
    return jsonify({"error": "Expense not found"}), 404

##########################################
# TWILLIO ROUTES FOR REMINDER EMAIL

@app.route('/send-reminder/expenses/<int:expense_id>/users/<int:user_id>', methods=['POST'])
def send_expense_reminder(expense_id, user_id):
    """Send an email reminder to a user about their pending expense to pay."""
    
    # Fetch the expense
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    
    # Fetch the Owner of the expense
    owner = expense.owner
    if not owner:
        return jsonify({"error": "Expense has no Owner"}), 404
    
    sender_id = owner.id  # The ID of the user sending the reminder (in the body)

    # Fetch the user being reminded
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetch the sender (group member who is triggering the reminder)
    sender = User.query.get(sender_id)
    if not sender:
        return jsonify({"error": "Sender not found"}), 404

    # Ensure the sender and recipient are in the same group (linked via the event)
    group = expense.event.group
    if sender not in group.users or user not in group.users:
        return jsonify({"error": "Both sender and recipient must be in the same group"}), 403

    # Fetch the user's split from the ExpenseSplit table
    expense_split = ExpenseSplit.query.filter_by(expense_id=expense_id, user_id=user_id).first()
    if not expense_split:
        return jsonify({"error": "No expense split found for this user"}), 404

    amount_owed = expense_split.amount_owed - expense_split.amount_paid  # Remaining balance

    if amount_owed <= 0:
        return jsonify({"message": "User has no pending balance."}), 200

    # Email Content
    subject = "Expense Payment Reminder"
    content = f"""
    Hello {user.username},

    {sender.username} is reminding you that you owe ${amount_owed:.2f} for the expense: "{expense.description}".

    Please settle this payment as soon as possible.

    Best regards,  
    {sender.username}
    """

    # Send Email via SendGrid
    message = Mail(
        from_email=sender.email,  # Sender's email (a group member)
        to_emails=user.email,  # Recipient's email
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return jsonify({"message": f"Reminder email sent successfully to {user.email}!", "status_code": response.status_code}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send reminder email to {user.email} - {str(e)}"}), 500

@app.route('/')
def index():
    return "Hello, Flask with PostgreSQL!"


if __name__ == '__main__':
    app.run(debug=True)


