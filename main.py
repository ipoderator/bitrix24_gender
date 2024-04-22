import configparser
from pprint import pprint

from fast_bitrix24 import Bitrix

from database.database import update_contact_gender
from functions import add_users, get_data


def add_bx(bx, database, user, password):
    add_users(bx)
    contacts = get_data(bx)
    pprint(contacts)
    update_contact_gender(bx, contacts,  database, user, password)


def main():
    config = configparser.ConfigParser()
    config.read('setting.ini')
    database = config.get('db', 'database')
    user = config.get('db', 'user')
    password = config.get('db', 'password')
    webhook = config.get('BITRIX24', 'webhook')
    bx = Bitrix(webhook)
    main(bx, database, user, password)


if __name__ == '__main__':
    main()
