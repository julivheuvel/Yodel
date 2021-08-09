from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import yodel


import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# =====================================================


class User: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.yodels = []
    # ================================================


    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters long!")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters long!")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email is not valid!")
            is_valid = False
        if len(data['username']) < 3:
            flash("Username must be at least 3 characters long!")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid
    

    # =======================================================
    # GET ONE USER
    # =======================================================

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('yodel_schema').query_db(query, data)
        return cls(results[0])


    # =======================================================
    # GET ONE USER BY USERNAME
    # =======================================================

    @classmethod
    def get_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL('yodel_schema').query_db( query, data )
        if len(results) < 1:
            return False
        return cls(results[0])


    # =======================================================
    # CREATE USER
    # =======================================================

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , username, password, created_at, updated_at ) VALUES ( %(first_name)s, %(last_name)s,  %(email)s, %(username)s, %(password)s, NOW() , NOW() );"
        return connectToMySQL('yodel_schema').query_db( query, data )
    
