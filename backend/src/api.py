import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

# manager new: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNFYWpVclc4RFZubFIta1U4b2QwRyJ9.eyJpc3MiOiJodHRwczovL3VuMWNvcm4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzE4NmRiZDJmMWNkMDAzN2VmZDMyNiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1OTg0MTUwMDYsImV4cCI6MTU5ODQyMjIwNiwiYXpwIjoiYkV3UFJKYnNwN3ZnNmZxREQ1NFZVM3ZOc3BTQ05zRzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.VirehqKaHftVX4-1kmWSPy-ZVYaLsoouFmHqew8CRYFVnBi3yJ2o7X5iAPisjuzuGrBnjU6cN9WjlPRQXmINFybf67fm7iHgUReR-t3X-dlLa_8UBjk45Fz7tt3vj_uTghsGPRcJUbXvF2rcT9LPVUqYAxofhUkTCFUE6IjGuzoOT9sqshT4LM5Cb_JtSInsK5BYay-ZQHDIM05wImnGaAP9-NsBUJ249EYIl5WbPvs1fkz1M0OQc1kUB4M4dDnP9zFkc2CT3XifvmHaSCpT8KaRIQkko1YwgEyynWkcDlAiBg5QWbNs1x3nnMPiOvyS4voSm29X92Wc1QHhSHI17g
# barista new: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNFYWpVclc4RFZubFIta1U4b2QwRyJ9.eyJpc3MiOiJodHRwczovL3VuMWNvcm4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDQ3MmQ1OWM1MTA2MDA2ZGUxMzQzNiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1OTg0MjExNjIsImV4cCI6MTU5ODQyODM2MiwiYXpwIjoiYkV3UFJKYnNwN3ZnNmZxREQ1NFZVM3ZOc3BTQ05zRzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.XJE4X8_tBrqFaV6-2ubjge9gmi3devqzjC80UWX6w_x-5bhraaHBfnUXpfNz0-jBmECJMCADpiS7OVgM89ksVHkcl3vs58y9lsSk9NaeeIdgVPnFjFOloJBb5IqQO76NSnwtzYiKNcQE5N8ThLQJox4jvfhq4CekjoKKrbLTK7vvHuXBHCWhrt_sv9dulUX8gzYxBYOMgvQzNwt-m7x8Dh0DcBrDh9dT-pQ5Bk7UJ9wgtzD-FqVTOE5ZpFzYTsmYoUXTP4c3FgCkt-EAGLupyjvwnl6Iy0hGDT6gKMlpS3dI7KOXy9TcWFDpYxIrUW8a7eqlcrMbr8cIFCva-56_cQ
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
        'drinks': short_drink
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
def drinks(token):
    # getting all the drinks from the database
    drinks = Drink.query.all()

    if(len(drinks) == 0):
        abort(404)

    long_drinks = []

    # getting the long representation for each drink and adding it to a list of short_drinks
    for drink in drinks:
        long_drinks.append(drink.long())

    return jsonify({
        'success': True,
        'drinks': long_drink      
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
def drinks(token):
    # getting the json response body
    body = request.get_json()

    # getting each element from the body
    new_recipe = body.get('recipe')
    new_title = body.get('title')

    # attempting to add the new drink, else throw an unprocessable error
    try:
        drink = Drink(recipe=new_recipe, title=new_title)
        drink.insert()

        # getting the long representation of the drink
        long_drink = drink.long()

        return jsonify({
            'success': True,
            'drinks': long_drink    
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
def drinks(token, drink_id):
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
        # checking to see 
        if (new_recipe):
            drink.recipe = new_recipe
        if (new_title):
            drink.title = new_title
    except:
        abort(400)
   
    drink.update()

    long_drink = drink.long()

    return jsonify({
        'success': True,
        'drinks': long_drink
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
def drinks(token, drink_id):
    # attempting to get the drink to delete
    try:
      drink = Drink.query.filter_by(id=drink).one_or_none()

      if drnk is None:
        abort(404)
      
      # delete the question if it exists and redisplay the questions
      drink.delete()

      return jsonify({
        'success': True,
        'deleted': drink_id,
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
        'message': get_error_message(AuthError.error, "Authentication failure")
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