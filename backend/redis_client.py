import redis
from dotenv import load_dotenv
import os

load_dotenv()

# zhi shi redis client
redis_client = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)
