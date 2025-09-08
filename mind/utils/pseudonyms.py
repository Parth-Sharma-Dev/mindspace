import hmac, hashlib
from django.conf import settings

ADJECTIVES = ["Calm", "Bright", "Gentle", "Kind", "Silver", "Brave"]
ANIMALS = ["Otter", "Fox", "Sparrow", "Dolphin", "Panda", "Hedgehog"]


def pseudonym_for(user_id: int, context_id: str) -> str:
    msg = f"{user_id}:{context_id}".encode()
    digest = hmac.new(settings.SECRET_KEY.encode(), msg, hashlib.sha256).digest()
    adj = ADJECTIVES[digest[0] % len(ADJECTIVES)]
    ani = ANIMALS[digest[1] % len(ANIMALS)]
    tag = hashlib.sha256(digest).hexdigest()[:4]
    return f"{adj} {ani} #{tag}"


def anon_id(user_id: int) -> str:
    """Generates a unique anonymous ID from user_id"""
    return hashlib.sha256(str(user_id).encode()).hexdigest()
