from mongoengine import Document, EmailField, StringField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# User document stored in the auth_db alias
class User(Document):
	meta = {"collection": "users", "db_alias": "auth_db"}
	username = StringField(required=True, unique=True)
	email = EmailField(required=True, unique=True)
	password = StringField(required=True)
	created_at = DateTimeField(default=datetime.utcnow)

	@property
	def is_authenticated(self):
		return True

	def set_password(self, raw_password):
		self.password = generate_password_hash(raw_password)

	def check_password(self, raw_password):
		return check_password_hash(self.password, raw_password)

	def to_safe_dict(self):
		# return a dict safe for JSON responses (no password)
		return {
			"id": str(self.id),
			"username": getattr(self, "username", None),
			"email": self.email,
			"created_at": self.created_at,
		}



# This is how i understood the flow :
# Register:

# Step 1 : receive raw_password    
# Step 2 : call user.set_password(raw_password) 
# Step 3 : generate_password_hash produces a hash 
# Step 4 : stored in user.password 
# Step 5 : user.save()

#Login:
# Step 1 : receive raw_password 
# Step 2 : load user by email
# Step 3 : call user.check_password(raw_password)
# Step 4 : check_password_hash(self.password, raw_password) returns True/False.