from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE 
from flask import flash

class Armadillo:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['points']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data): #Adds a User to play
        query = """
        INSERT INTO armadillos (name, points)
        VALUES ( %(name)s, %(points)s )
        """

        return  connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query="""
        SELECT * FROM armadillos
        ORDER BY points DESC
        """
        return  connectToMySQL(DATABASE).query_db(query)

    @classmethod
    def validator(cls, data):
        is_valid = True
        if len(data['name']) < 1:
            flash("Name required... This isn't the Good, the Bad, and the Ugly!", 'reg')
            is_valid = False
        
        return is_valid