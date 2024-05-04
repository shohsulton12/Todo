import utils
from connecting import cur, conn
from models import User
from session import Session
from connecting import commit

session = Session()


@commit
def login(username: str, password: str) -> utils.ResponseData:
    user: User | None = session.check_session()
    if user:
        return utils.ResponseData('This User already logged in😎.', False)

    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username, (username,))
    user_data = cur.fetchone()
    if not user_data:
        return utils.ResponseData('Bad credentials', False)
    user = User.from_tuple(user_data)
    if user.login_try_count >= 3:
        return utils.ResponseData('User has been blocked😒',False)

    if not utils.match_password(password, user.password):
        update_user_try_count = '''update users set login_try_count = login_try_count + 1 where username = %s;'''
        cur.execute(update_user_try_count, (username,))
        return utils.ResponseData('Bad credentials', False)

    session.add_session(user)
    return utils.ResponseData('User Successfully logged in', True)



