import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

# manager new: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNFYWpVclc4RFZubFIta1U4b2QwRyJ9.eyJpc3MiOiJodHRwczovL3VuMWNvcm4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzE4NmRiZDJmMWNkMDAzN2VmZDMyNiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1OTg0NTM3NjMsImV4cCI6MTU5ODQ2MDk2MywiYXpwIjoiYkV3UFJKYnNwN3ZnNmZxREQ1NFZVM3ZOc3BTQ05zRzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.Cv3-hZ9eMCEilUnWEECDTt_aUbTRaMkSWkuHvJmrytPtqOFJJJTE7mYCjgvi-6ZURBu2p3Z-awpofmq_qMdwMDbRJ7hwejkj90DNwxe-BhxlXrCPM-oWLxDK1CyBTVXq5xxIi_jhJ29Yg3xE2awgAASYu40E2J_xba8GaW5M-ZlcH8Eyw-XXwn5nTHJFxnvCLunupXNhn6r5bz3oFlKcGYqrea_P6nPf_pdjYjEnRKf_frxmwmTaBegOgB5v3aRCo-2WfbnFgj-RbvfVvihukCJ6fklOy3Mji_fMjF7mqF5-LCpEpempw1MoSp6nZ7YxBab_os6Qyi25erfe1dqv9A
# barista new: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNFYWpVclc4RFZubFIta1U4b2QwRyJ9.eyJpc3MiOiJodHRwczovL3VuMWNvcm4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDQ3MmQ1OWM1MTA2MDA2ZGUxMzQzNiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1OTg0NTM5NjQsImV4cCI6MTU5ODQ2MTE2NCwiYXpwIjoiYkV3UFJKYnNwN3ZnNmZxREQ1NFZVM3ZOc3BTQ05zRzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.X_qKttfZYVXIr2G0NUpjQ8jFvhm0xXhFvI_RhXUmn_EC9f4vlZJC52efzjQ301toWWBElmBiHV1hmjgCmvpYNujLeEy39_ltY-AwQEGyezKnR-C9NXi0-2jlIN1NebsqgGhMPJgkF1pXfZmEfo-qDiZwNOHp-3fcVKw8IpcDOFOJGaButr8CukxFo4jmFFagtrEqGCfjo295dc0h8RvvWSsw9CNBWzpdEvWRfqX7p5FTcEYVthq_YcZftWO7L11ncvN2U39e_tKwbLKUEqD9ZaNzU9ln5C96JNp2Wr4zKpNxpm3XdB8fcwX8zTNBfVjg5CnjqvwYBcHYbUhmSqtdsQ
app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES

@app.route('/')
def handler():
    return jsonify({
        "success": True
    })

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    # getting all the drinks from the database
    drinks = Drink.query.all()
    short_drinks = []

    # getting the short representation for each drink and adding it to a list of short_drinks
    for drink in drinks:
        short_drinks.append(drink.short())

    # return the json object
    return jsonify({
        'success': True,
        'drinks': short_drinks
    }), 200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    # getting all the drinks from the database
    drinks = Drink.query.all()

    long_drinks = []

    # getting the long representation for each drink and adding it to a list of short_drinks
    for drink in drinks:
        long_drinks.append(drink.long())

    return jsonify({
        'success': True,
        'drinks': long_drinks    
    }), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks-detail')
def create_drink(token):
    # getting the json response body
    body = request.get_json()

    # seeing if the json includes the required data
    if not ('title' in body and 'recipe' in body):
        abort(400)

    # getting each element from the body
    new_recipe = body.get('recipe')
    new_title = body.get('title')

    # attempting to add the new drink, else throw an unprocessable error
    try:
        drink = Drink(recipe=json.dumps(new_recipe), title=new_title)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]    
        }), 200    
    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, drink_id):
    # search the database for the given drink_id
    drink = Drink.query.filter_by(id=drink_id).one_or_none()

    # if the drink does not exist then abort not found
    if (drink is None):
        abort(404)

    # getting the json response body
    body = request.get_json()

    # getting each element from the body
    new_recipe = body.get('recipe')
    new_title = body.get('title')

    try:
        # checking to see which item will be affected
        if (new_recipe):
            drink.recipe = json.dumps(new_recipe)
        if (new_title):
            drink.title = new_title
    except:
        abort(400)
   
    drink.update()

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):
    # gettint the drink to delete
    drink = Drink.query.filter_by(id=drink).one_or_none()

    if drnk is None:
    abort(404)
      
    try:
      # delete the question if it exists and redisplay the questions
      drink.delete()

      return jsonify({
        'success': True,
        'deleted': drink_id
      }), 200    
    except:
      abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authentication_eror(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code

@app.errorhandler(400)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': "Bad request"
    }), 400

@app.errorhandler(401)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': "Unauthorized"
    }), 401

@app.errorhandler(403)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': "Forbidden"
    }), 403
  
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Not found"
    }), 404 

@app.errorhandler(405)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': "Method not allowed"
    }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': "Unprocessable"
    }), 422

@app.errorhandler(500)
def internal(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': "Internal server error"
    }), 500