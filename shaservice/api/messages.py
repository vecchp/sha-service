import hashlib
import json
from shaservice.config import redis_client


# Lighweight looking table
# In the future this can be a database or fast key/value store

def get(digest):
    message = redis_client.get(digest)
    return (json.loads(message.decode()), 200) if message else ('Not found', 404)


def post(message):
    encoded_message = message['message'].encode()
    sha_256_digest = hashlib.sha256(encoded_message).hexdigest()
    redis_client.set(sha_256_digest, json.dumps(message).encode())
    return {'digest': sha_256_digest}, 201
