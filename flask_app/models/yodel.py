from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import yodel

# =======================================================

class Yodel:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.public = data['public']
        self.recipient = data['recipient']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.posted_by = {}

    # =======================================================

    @staticmethod
    def validate_yodel(data):
        is_valid = True
        if len(data['content']) > 500:
            flash("Cannot be over 500 characters long!")
            is_valid = False
        return is_valid


    # =======================================================
    # SAVE yodels
    # =======================================================
    @classmethod
    def save(cls, data):
        query = "INSERT INTO yodels ( recipient, content, public, user_id, created_at, updated_at ) VALUES (%(recipient)s, %(content)s, %(public)s, %(user_id)s, NOW(), NOW() );"
        return connectToMySQL('yodel_schema').query_db( query, data )


    # =======================================================
    # GET ALL PUBLIC YODELS
    # =======================================================

    @classmethod
    def all_public_yodels(cls):
        query ="SELECT * FROM yodels JOIN users ON users.id = user_id WHERE public = 'yes' ORDER BY yodels.created_at DESC;"
        results = connectToMySQL('yodel_schema').query_db( query )
        
        yodel = []

        for one_yodel in results:
            yodel.append(cls(one_yodel))
        return yodel


    # =======================================================
    # DELETE SHOW
    # =======================================================
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM yodels WHERE id = %(id)s;"
        results = connectToMySQL('yodel_schema').query_db( query, data )
        return results
