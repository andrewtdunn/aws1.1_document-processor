from flask_login import UserMixin
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resource and table
# Ensure you have AWS credentials configured in your environment or code
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
table = dynamodb.Table('DocunosisUsers') 

class DocunosisUser(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    # Override the get_id method to return the correct attribute
    def get_id(self):
        return str(self.username) # Ensure the ID is returned as a string (unicode in Python 2)

    @staticmethod
    def get(user_id):
        """Retrieves a user from DynamoDB by user ID."""
        response = table.query(
            KeyConditionExpression=Key('id').eq(user_id)
        )
        if response['Count'] == 0:
            return None
        
        # Extract user data from the response
        user_data = response['Items'][0]
        user = User(
            id=user_data['id'],
            email=user_data['email'],
            password=user_data['password'] # Note: Passwords should be hashed in a real app
        )
        return user
    
    @staticmethod
    def create(username, email, password):
        """Creates a new user in DynamoDB."""
        table.put_item(
            Item={
                'username': username,
                'email': email,
                'password': password # Store the hashed password
            }
        )
        return DocunosisUser(username, email, password)

