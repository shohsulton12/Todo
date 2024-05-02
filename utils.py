import bcrypt


def hash_password(raw_password):
    encoded_password = raw_password.encode('utf-8')
    salt = bcrypt.gensalt(4)
    return bcrypt.hashpw(encoded_password, salt)


def check_password(raw_password, hashed_password):
    pass
