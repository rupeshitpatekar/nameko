import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
import jwt

JWT_SECRET = "myjwtsecret"
JWT_ALGORITHM = "HS256"

class GatewayService:
    name = 'gateway'
    airports_rpc = RpcProxy('airports_service')
    trips_rpc = RpcProxy('trips_service')
    user_rpc = RpcProxy('user_service')

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    @http('GET', '/airport/<string:airport_id>')
    def get_airport(self, request, airport_id):
        token = request.headers.get('Authorization').split(' ')[1]
        self.validate_token(token)
        airport = self.airports_rpc.get(airport_id)
        return json.dumps({'airport': airport})

    @http('POST', '/airport')
    def post_airport(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        self.validate_token(token)
        data = json.loads(request.get_data(as_text=True))
        airport_id = self.airports_rpc.create(data['airport'])
        return airport_id

    @http('GET', '/trip/<string:trip_id>')
    def get_trip(self, request, trip_id):
        token = request.headers.get('Authorization').split(' ')[1]
        self.validate_token(token)
        trip = self.trips_rpc.get(trip_id)
        return json.dumps({'trip': trip})

    @http('POST', '/trip')
    def post_trip(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        self.validate_token(token)
        data = json.loads(request.get_data(as_text=True))
        trip_id = self.trips_rpc.create(data['airport_from'], data['airport_to'])
        return trip_id

    @http('POST', '/create_user')
    def http_create_user(self, request):
        data = json.loads(request.get_data(as_text=True))
        username = data['username']
        password = data['password']
        user_id = self.user_rpc.create_user(username, password)
        return json.dumps({"user_id": user_id})

    @http('POST', '/login')
    def http_login(self, request):
        data = json.loads(request.get_data(as_text=True))
        username = data['username']
        password = data['password']
        token = self.user_rpc.login(username, password)
        if token:
            return json.dumps({"token": token})
        return json.dumps({"error": "Invalid credentials"}), 401