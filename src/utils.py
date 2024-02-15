from re import Pattern
from typing import Any

from .models import Profile


def hello() -> Any:
    """Функция для приветствия."""

    return print('Добрый день!\n')


def get_exit() -> Any:
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


def check_data(profile: Profile) -> Any:
    """Функция для проверки данных записи в классе профиля."""

    data_check = profile.validate()
    if isinstance(data_check, dict):
        print(data_check['error'])
        return False
    return True


def get_checked_value(pattern: Pattern, data: str) -> Any:
    """Функция для проверки введённых данных согласно паттерну и возврата только правильного значения."""

    counter = 3
    while counter > 0:
        counter -= 1
        if counter >= 2:
            value = input('\nВведите новое значение: ')
        else:
            value = input('Введите новое значение: ')
        checker = pattern.match(value)
        if counter == 0 and not checker or counter == 0 and value == data:
            error = '\nВы истратили кол-во попыток для изменения данных!\n'
            return error, False
        elif counter > 0 and not checker or counter > 0 and value == data:
            print('\nВведенные данные некорректны! Попробуйте ещё раз.\n')
            continue
        return value, True
