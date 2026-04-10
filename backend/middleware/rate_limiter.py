from flask import request, jsonify, g
from flask_jwt_extended import get_jwt_identity
from extensions import redis_client

RATE_LIMITS = {
    "auth": (5, 60),        # 5 req / 60 sec
    "default": (50, 60),    # 50 req / 60 sec
}

def get_identifier():
    try:
        user_id = get_jwt_identity()
        if user_id:
            return f"user:{user_id}"
    except Exception:
        pass

    return f"ip:{request.remote_addr}"


def rate_limiter():
    if request.method == "OPTIONS":
        return

    identifier = get_identifier()

    if request.path.startswith("/auth"):
        limit, window = RATE_LIMITS["auth"]
    else:
        limit, window = RATE_LIMITS["default"]

    key = f"rate:{identifier}:{request.method}:{request.path}"

    try:
        current = redis_client.get(key)

        if current is None:
            redis_client.set(key, 1, ex=window)
            remaining = limit - 1

        elif int(current) < limit:
            redis_client.incr(key)
            remaining = limit - int(current) - 1

        else:
            return jsonify({
                "error": "Too many requests. Please try again later.",
                "retry_after": redis_client.ttl(key)
            }), 429
        g.rate_limit = limit
        g.remaining = remaining

    except Exception as e:
        print("Rate limiter error:", e)
        return