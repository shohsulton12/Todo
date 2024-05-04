from typing import Optional, Any

import bcrypt


def hash_password(raw_password: Optional[str] = None):
    assert raw_password, 'Raw Password can not be empty'
    return bcrypt.hashpw(raw_password.encode(), salt=bcrypt.gensalt())


def match_password(raw_password: Optional[str] = None,
                   encoded_password: Optional[str] = None) -> bool:
    assert raw_password, 'Raw Password can not be empty'
    assert encoded_password, 'Encoded Password can not be empty'

    return bcrypt.checkpw(raw_password.encode(), encoded_password.encode())


class ResponseData:
    def __init__(self, data: Any, status: Optional[bool] = None):
        self.data = data
        self.status = status or False
