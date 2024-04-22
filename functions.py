def add_users(bx):
    """Добавление нужных полей."""
    try:
        tasks = {
            "NAME": "GENDER",
            "EDIT_FORM_LABEL": "Пол",
            "LIST_COLUMN_LABEL": "Пол",
            "ID": "string",
            "GEBDER": "GENDER",
        }
        gender = bx.call('crm.contact.userfield.add', tasks)
        return gender
    except Exception:
        pass


def get_data(bx):
    """Получение имени и id."""
    tasks = {'SELECT': ['ID', 'NAME']}
    contacts = bx.get_all('crm.contact.list', tasks)
    return contacts
