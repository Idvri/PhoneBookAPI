from typing import Any

import src

from .models import PATTERNS, Profile
from .utils import check_data, get_checked_value, get_exit, get_profiles, save_data


def get_choice() -> Any:
    """Функция, описывающая логику для получения выбора пользователя."""

    str_choices = '1. Добавление новой записи в справочник;\n2. Редактировать запись в справочнике;\n' \
                  '3. Вывести записи из справочника;\n4. Поиск записей; \n5. Выйти.\n'
    choice = input(f'Выберите, что хотите сделать (укажите цифру):\n{str_choices}\nВаш выбор: ')

    if choice == '1':
        return add_profile(), True
    elif choice == '2':
        return edit_profile(), True
    elif choice == '3':
        return get_profiles_with_pagination(), True
    elif choice == '4':
        return find_profile(), True
    elif choice == '5':
        return get_exit(), False
    else:
        return print('\nВы указали неверный вариант. Попробуйте ещё раз!\n'), True


def get_profiles_with_pagination(
        profiles: list[Profile] | None = None, paginator: int = 0, from_found: bool = False
) -> Any:
    """Функция, описывающая логику для вывода строк из справочника."""

    if not profiles and not from_found:
        profiles = get_profiles()
        if not profiles:
            return print('\nНет записей.\n')
    elif not profiles and from_found:
        return print('\nНет записей.\n')

    if paginator == 0:
        try:
            paginator = int(input('\nВведите сколько записей должно быть отображено за раз. '
                                  '\nВаш выбор (число): '))
        except ValueError:
            return print('\nНужно ввести кол-во выводимых строк в виде числа.\n')

    if isinstance(profiles, list):
        for profile in profiles[:paginator]:
            print(profile)
            profiles.remove(profile)

    if profiles:
        choice = input('\nДалее? Ваш ответ (да или нет): ')
        if choice == 'да' or choice == '':
            get_profiles_with_pagination(profiles=profiles, paginator=paginator)
        else:
            print('\nВозвращаемся к главному меню.\n')
    else:
        print('\nВсе записи выведены.\n')


def add_profile() -> Any:
    """Функция, описывающая логику для создания новой записи."""

    profiles = get_profiles()
    counter = 3
    new_profile = None
    checker = False
    while counter > 0:
        counter -= 1
        new_profile = Profile(
            surname=input('\nВведите вашу фамилию: ').title(),
            name=input('Введите ваше имя: ').title(),
            last_name=input('Введите ваше отчество: ').title(),
            organization=input('Введите вашу компанию: ').upper(),
            work_number=input('Введите ваш рабочий номер: '),
            number=input('Введите ваш личный номер: '),
        )
        checker = check_data(new_profile)
        if not checker and counter > 0:
            print('Попробуйте ещё раз корректно ввести данные.')
            continue
        break

    if not checker:
        return print('Попытки для корректного ввода данных были исчерпаны!\n')

    if profiles and isinstance(new_profile, Profile):
        fail = [
            profile for profile in profiles
            if str(profile.number) == str(new_profile.number) or str(profile.work_number) == str(
                new_profile.work_number
            )
        ]
        if fail:
            return print(f'\nЗапись с таким личным или рабочим номером уже существует:\n{fail[0].__str__()}\n')
        profiles.append(new_profile)
        save_data(profiles)
    elif not profiles and isinstance(new_profile, Profile):
        profiles = [new_profile]
        save_data(profiles)

    print('\nЗапись добавлена!\n')


def edit_profile() -> Any:
    """Функция, описывающая логику для редактирования записей."""

    profiles = get_profiles()
    if not profiles:
        return print('\nНет записей для редактирования.\n')

    number = input('Укажите, пожалуйста, личный номер телефона контакта, \nкоторый вы хотите редактировать: ')
    pattern = PATTERNS['numbers']
    if not pattern.match(number):
        return print('\nУказан некорректный номер!\n')
    profiles_list = [profile for profile in profiles if str(profile.number) == number]
    if len(profiles_list) > 0:
        profile = profiles_list[0]
    else:
        return print('\nНет контактов с таким личным номером.\n')

    choice = input(f'\n{profile}\nЧто вы хотите изменить (фамилия, имя, отчество, организация, рабочий номер, '
                   f'личный номер): ').lower()

    if choice == 'фамилия':
        value, status = get_checked_value(PATTERNS['strings'], profile.surname)
        if status:
            profile.surname = value
        else:
            return print(value)
    elif choice == 'имя':
        value, status = get_checked_value(PATTERNS['strings'], profile.name)
        if status:
            profile.name = value
        else:
            return print(value)
    elif choice == 'отчество':
        value, status = get_checked_value(PATTERNS['strings'], profile.last_name)
        if status:
            profile.last_name = value
        else:
            return print(value)
    elif choice == 'организация':
        profile.organization = input('\nВведите новое значение: ')
    elif choice == 'рабочий номер':
        value, status = get_checked_value(PATTERNS['numbers'], profile.work_number)
        if status:
            profile.work_number = value
        else:
            return print(value)
    elif choice == 'личный номер':
        value, status = get_checked_value(PATTERNS['numbers'], profile.number)
        if status:
            profile.number = value
        else:
            return print(value)
    else:
        print('\nУказан неверный вариант!')

    replace_index = profiles.index(profile)
    profiles[replace_index] = profile
    save_data(profiles)
    return print(f'\nДанные изменены:\n{profile}\n')


def find_profile() -> dict | None:
    """Функция описывающая логику для поиска записей."""

    profiles = get_profiles()
    if profiles is None:
        return print('\nНет записей для поиска.\n')

    choice = input('\nПо каким данным будет производиться поиск (имя или личный номер): ').lower()
    if choice == 'имя':
        context = src.Context(src.Name())
        name = input('\nВведите имя для поиска: ')
        found = context.find(name)
        if isinstance(found, dict):
            return print(found['error'])
    elif choice == 'номер' or choice == 'личный номер':
        context = src.Context(src.Number())
        number = input('\nВведите номер для поиска: ')
        found = context.find(number)
        if isinstance(found, dict):
            return print(found['error'])
    else:
        return print('\nБыл указан некорректный вариант!\n')
    return None
