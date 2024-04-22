def get_gender(bx, id, gender):
    """Получение гендера по id"""
    params = {
        'ID': id,
        "fields":
            {'UF_CRM_GENDER': gender}
    }
    gen = bx.call('crm.contact.update', params)
    return gen
