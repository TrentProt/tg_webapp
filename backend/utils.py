import hmac
import hashlib
from urllib.parse import parse_qsl

def validate_init_data(init_data: str, bot_token: str) -> bool:
    data = dict(parse_qsl(init_data, keep_blank_values=True))
    hash_received = data.pop("hash", None)

    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret = hashlib.sha256(bot_token.encode()).digest()
    hash_calculated = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()

    return hash_calculated == hash_received