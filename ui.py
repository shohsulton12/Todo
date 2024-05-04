from service import login
from utils import ResponseData
from colorama import Fore


def print_response(response: ResponseData):
    color = Fore.GREEN if response.status else Fore.RED
    print(color + str(response.data) + Fore.RESET)


def menu():
    print('Login => 1')
    print('Register => 2')
    print('Logout => 3')
    print('Quit => q')
    return input('?: ')


def authentication():
    username = input('Username: ')
    password = input('Password: ')
    response: ResponseData = login(username, password)
    print_response(response)


if __name__ == '__main__':
    while True:
        choice = menu()
        if choice == '1':
            authentication()
        elif choice == '2':
            pass
        elif choice == 'q':
            break


