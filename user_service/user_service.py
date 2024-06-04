import uuid
import json
import bcrypt
import jwt
from nameko.rpc import rpc
from nameko.web.handlers import http
from nameko_redis import Redis

JWT_SECRET = "myjwtsecret"
JWT_ALGORITHM = "HS256"

class UserService:
    name = "user_service"
    redis = Redis('development')

    @rpc
    def create_user(self, username, password):
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        user_id = uuid.uuid4().hex
        self.redis.set(f"user:{username}", json.dumps({"user_id": user_id, "password": hashed_pw.decode('utf8')}))
        return user_id

    @rpc
    def login(self, username, password):
        user_data = self.redis.get(f"user:{username}")
        if not user_data:
            return None
        user_data = json.loads(user_data)
        hashed_pw = user_data['password'].encode('utf8')
        if bcrypt.checkpw(password.encode('utf8'), hashed_pw):
            token = jwt.encode({"user_id": user_data["user_id"]}, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return token
        return None
