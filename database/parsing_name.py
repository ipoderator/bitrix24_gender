from bs4 import BeautifulSoup
from requests import RequestException, Response
import logging
from typing import Optional

from database.constants import MAIN_DOC_URL
from exceptions import ParserFindTagException


def get_response(session, url: str) -> Optional[Response]:
    try:
        response = session.get(MAIN_DOC_URL)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def list_names(session) -> list:
    try:
        response = get_response(session)
        if response is None:
            return None
        soup = BeautifulSoup(response.text, features='lxml')
        data_names = soup.find_all('a', class_="blue")
        list_names = [names.text for names in data_names]
        list_names.sort()
        return list_names
    except ParserFindTagException:
        return None
