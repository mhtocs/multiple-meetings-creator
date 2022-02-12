from dotenv import load_dotenv
import os
import redis

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret")

    SESSION_TYPE = "redis"
    SESSION_PERMANANT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(
        os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"))
