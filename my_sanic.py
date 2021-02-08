import jwt
import functools
from typing import Dict

from jwt import InvalidSignatureError
from sanic.log import logger
from sanic import Sanic, request, response

JWT_SIGN_ALGORITHM = 'HS256'
SECRET = 'blabla'
USER_FILENAME = 'users.txt'
USERS_DB = {}

app = Sanic('q2')


def generate_jwt_token(payload: Dict) -> str:
    token = jwt.encode(payload, SECRET, algorithm=JWT_SIGN_ALGORITHM)
    return token


def decode_jwt_token(token) -> Dict:
    return jwt.decode(token, SECRET, algorithms=JWT_SIGN_ALGORITHM)


def load_users(filename: str) -> Dict:
    """
        read the user db, and yes i know it is not encrypted or anything
    """
    logger.info(f'about to read users file {filename}')
    users = {}
    with open(filename) as fh:
        for row in fh:
            username, password = row.strip().split('/')
            users[username] = password
    logger.info(f'read {len(users)} users')
    return users


def verify_token(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            token = args[0].headers['token']
            permissions = decode_jwt_token(token)
            return func(*args, **kwargs)
        except KeyError:
            return response.json({'error': 'missing token header'}, status=403)
        except InvalidSignatureError:
            return response.json({'error': 'bad token'}, status=403)

    return wrapper_decorator


@app.post("/login")
async def login(request: request) -> response:
    try:
        data = request.json
        username = data['username']
        password = data['password']
        if username in USERS_DB:
            if USERS_DB[username] == password:
                token = generate_jwt_token({'user': username})
                return response.json({'token': token})
        else:
            return response.json({'error': 'bad username/password'}, status=403)
    except:
        return response.json({'error': 'bad input / missing required keys'}, status=400)


@app.post("/normalize")
@verify_token
async def nomralize(request: request) -> response:
    try:
        data = request.json
        parsed = {rec['name']: [rec[val] for val in rec if 'Val' in val][0] for rec in data}
        return response.json(parsed)
    except:
        return response.json({'error': 'bad input / missing required keys'})


USERS_DB = load_users(USER_FILENAME)
app.run(host="0.0.0.0", port=5000)
