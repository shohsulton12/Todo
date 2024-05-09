import utils
from db import cur, conn
from models import User, UserRole, UserStatus
from session import Session
from db import commit
from dto import UserRegisterDTO
from validators import check_validators
from utils import is_authenticated
from models import TodoType

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
        return utils.ResponseData('User has been blocked😒', False)

    if not utils.match_password(password, user.password):
        update_user_try_count = '''update users set login_try_count = login_try_count + 1 where username = %s;'''
        cur.execute(update_user_try_count, (username,))
        return utils.ResponseData('Bad credentials', False)

    session.add_session(user)
    return utils.ResponseData('User Successfully logged in', True)


@commit
def register(dto: UserRegisterDTO) -> utils.ResponseData:
    try:
        check_validators(dto)
        check_username_by_query = '''select * from users where username = %s;'''
        cur.execute(check_username_by_query, (dto.username,))
        user = cur.fetchone()
        if user:
            return utils.ResponseData('This user already registered', False)

        insert_user_query = '''insert into users(username,password,role,status,login_try_count) values (%s,%s,%s,%s,%s);'''
        insert_data_params = (
            dto.username, utils.hash_password(dto.password), UserRole.USER.value, UserStatus.INACTIVE.value, 0)
        cur.execute(insert_user_query, insert_data_params)
        return utils.ResponseData('User Successfully registered', True)


    except AssertionError as e:
        return utils.ResponseData(e, False)


def logout() -> utils.ResponseData:
    global session
    if session.session:
        session.session = None
    return utils.ResponseData('User Successfully logged out', True)


@is_authenticated
@commit
def add_todo(title: str):
    insert_todo_query = '''insert into todos(title,todo_type,user_id) values (%s,%s,%s);'''
    insert_data_params = (title, TodoType.PERSONAL.value, session.session.id)
    cur.execute(insert_todo_query, insert_data_params)
    return utils.ResponseData('Todo Successfully added', True)


@commit
def delete_todo(user_id: int) -> utils.ResponseData:
    delete_user_query = '''delete from users where id = %s;'''
    cur.execute(delete_user_query, (user_id,))
    return utils.ResponseData('User deleted successfully', True)


@commit
def edit_todo(user_id: int, new_username: str, new_password: str) -> utils.ResponseData:
    update_user_query = '''update users set username = %s, password = %s where id = %s;'''
    cur.execute(update_user_query, (new_username, utils.hash_password(new_password), user_id))
    return utils.ResponseData('User updated successfully', True)


def view_todo(user_id: int) -> utils.ResponseData:
    get_user_query = '''select * from users where id = %s;'''
    cur.execute(get_user_query, (user_id,))
    user_data = cur.fetchone()
    if not user_data:
        return utils.ResponseData('User not found', False)
    user = User.from_tuple(user_data)
    return utils.ResponseData(user.to_dict(), True)
