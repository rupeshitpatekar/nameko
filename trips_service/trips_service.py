import json
import uuid
from nameko.rpc import rpc
from nameko_redis import Redis

class TripsService:
    name = "trips_service"
    redis = Redis('development')

    @rpc
    def get(self, trip_id):
        trip = self.redis.get(trip_id)
        if trip:
            return json.loads(trip)
        return None

    @rpc
    def create(self, airport_from_id, airport_to_id):
        trip_id = uuid.uuid4().hex
        trip_data = {
            "from": airport_from_id,
            "to": airport_to_id
        }
        self.redis.set(trip_id, json.dumps(trip_data))
        return trip_id
