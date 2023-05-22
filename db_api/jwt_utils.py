import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv

load_dotenv()


def generate_token(email):
    secret_key = os.environ["API_KEY"]
    print(secret_key)
    expiration_time = datetime.utcnow() + timedelta(hours=10)

    payload = {"email": email, "exp": expiration_time}

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return (token, expiration_time)
