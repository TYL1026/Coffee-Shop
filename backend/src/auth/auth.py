import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# manager JWT (erinlouise11): eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNFYWpVclc4RFZubFIta1U4b2QwRyJ9.eyJpc3MiOiJodHRwczovL3VuMWNvcm4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzE4NmRiZDJmMWNkMDAzN2VmZDMyNiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1OTgzMjIwOTYsImV4cCI6MTU5ODMyOTI5NiwiYXpwIjoiYkV3UFJKYnNwN3ZnNmZxREQ1NFZVM3ZOc3BTQ05zRzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.GVE0i7bS-opa98NB9Knhu9c8Aqq_c1CX30Dm3yPLkJdxFUU7qFWC6awsDqXdZpEagQeXZLRqFu6t_YE_bwEKG074v4pLCXMRhI_RwWzQLHK82yIkEpBD1PcK8epwKgAcOMi9R9ZQDxmtU6MmfjFezsN_G6bgighH8ZUK_vTwMSzUMdA45nKpsHA39x2bSkEtNezbyE_HqYHtJwGZU9dbTvJ6ZneqBw4mLvviLD88GSNYDzwICSVliRy5melrlER_CSVIAjKPa9M2WGSu4jQvGZ5F5fdmMiRpGwViQ2ZTJiayROSE2myRohv-wVl8grp89WKnGEbOQ2nbl6QWw2krJA
# barista JWT (murphyerinlouise): eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNFYWpVclc4RFZubFIta1U4b2QwRyJ9.eyJpc3MiOiJodHRwczovL3VuMWNvcm4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNDQ3MmQ1OWM1MTA2MDA2ZGUxMzQzNiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1OTgzMjI5NDMsImV4cCI6MTU5ODMzMDE0MywiYXpwIjoiYkV3UFJKYnNwN3ZnNmZxREQ1NFZVM3ZOc3BTQ05zRzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.MKtb1EYBMKKkGoRHIjh75mP_OcVoQ02_semHKTx_LXHNjJ_LDcns_eOkD5j9iest11Qxf5ePlfgWnv4r8N_YbGjFasU_AHFZHex1r0yh8NV7v4Mhh8NlkX2yHRcvWkxiZSdnxFBEJzgPWCtf1C9CkRwe8eS3CyH5LkM3q3Y6p3lQnAaAKNR1Yrwx0-v3LNfQRuaju8SmoYY0-r3AkdCxzX53nEpQC4iu6hF2hJiQ_Mi3xI9mJsVu-CT658WjeMUdjpfqkNiOB5EvPKp7cpvuLGsTwTrDLNWeSpe2_hwsYOt6YwaJbo9BUj5IXEFgm3jKmtqgRbLoADki6sG_hVc7IA

AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'dev'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
   raise Exception('Not Implemented')

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    raise Exception('Not Implemented')

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    raise Exception('Not Implemented')

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator