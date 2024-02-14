from typing import Any

from .models import Profile


def hello() -> Any:
    """Функция для приветствия."""

    return print('Добрый день!\n')


def main_exit() -> Any:
    """Функция для выхода"""

    return print('\nХорошего дня!\n')


def get_profiles() -> list[Profile] | None:
    """Функция для получения данных из файла."""

    try:
        with open('src/data.txt', encoding='utf-8') as data:
            nums = data.read()
            if nums:
                nums_list = nums.split('\n')
                if nums_list[-1] != '':
                    nums_list.append('')
                list_nums = [Profile(*num.split(', ')) for num in nums_list[:-1]]
                return list_nums
            return None
    except FileNotFoundError:
        return None


def get_list_to_str(profiles: list[Profile]) -> str:
    """Функция для получения единой строки записей, которая состоит из данных профайлов."""

    string = ''
    for profile in profiles:
        string = string + f'{profile.__str__()}\n'
    return string


def save_data(profiles: list[Profile]) -> None:
    """Функция для сохранения данных в файл."""

    with open('src/data.txt', 'w', encoding='utf-8') as data:
        data.write(get_list_to_str(profiles))
