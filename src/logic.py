import re
from typing import Any

from .models import Profile
from .strategy import Context, Name, Number
from .utils import get_profiles, main_exit, save_data


def get_choice() -> Any:
    """Функция, описывающая логику для получения выбора пользователя."""

    str_choices = '1. Добавление новой записи в справочник;\n2. Редактировать запись в справочнике;\n' \
                  '3. Вывести записи из справочника;\n4. Поиск записей; \n5. Выйти.\n'
    choice = int(input(f'Выберите, что хотите сделать (укажите цифру):\n{str_choices}\nВаш выбор: '))

    if choice == '1':
        return add_new_profile(), True
    elif choice == '2':
        return edit_profile(), True
    elif choice == '3':
        return get_profiles_with_pagination(), True
    elif choice == '4':
        return to_find(), True
    elif choice == '5':
        return main_exit(), False

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
        paginator = int(input('\nВведите сколько записей должно быть отображено за раз. '
                              '\nВаш выбор (число): '))

    if isinstance(profiles, list):
        for profile in profiles[:paginator]:
            print(profile)
            profiles.remove(profile)

    if profiles:
        choice = input('\nДалее? Ваш ответ (да или нет): ')
        if choice == 'да':
            get_profiles_with_pagination(profiles=profiles, paginator=paginator)
    else:
        print('\nВсе записи выведены.\n')


def add_new_profile() -> Any:
    """Функция, описывающая логику для создания новой записи."""

    profiles = get_profiles()
    new_profile = Profile(
        surname=input('\nВведите вашу фамилию: ').title(),
        name=input('Введите ваше имя: ').title(),
        last_name=input('Введите ваше отчество: ').title(),
        organization=input('Введите вашу компанию: ').upper(),
        work_number=input('Введите ваш рабочий номер: '),
        number=input('Введите ваш личный номер: '),
    )

    data_check = new_profile.validate()
    if isinstance(data_check, dict):
        return print(data_check['error'])

    if profiles:
        fail = [
            profile for profile in profiles
            if str(profile.number) == str(new_profile.number) or str(profile.work_number) == str(
                new_profile.work_number
            )
        ]
        if fail:
            return print(f'\nЗапись с таким личным или рабочим номером уже существует:\n{fail[0].__str__()}\n')
        profiles.append(new_profile)
    else:
        profiles = [new_profile]

    save_data(profiles)
    print('\nЗапись добавлена!\n')


def edit_profile() -> Any:
    """Функция, описывающая логику для редактирования записей."""

    profiles = get_profiles()
    if not profiles:
        return print('\nНет записей для редактирования.\n')

    number = int(input('Укажите, пожалуйста, личный номер телефона контакта, \nкоторый вы хотите редактировать: '))
    pattern = re.compile(r'^\d{11}$')
    if not pattern.match(str(number)):
        return print('\nУказан некорректный номер!\n')
    profile = [profile for profile in profiles if str(profile.number) == str(number)][0]
    if not profile:
        return print('\nНет контактов с указанным личным номером.')

    choice = input(f'\n{profile}\nЧто вы хотите изменить (фамилия, имя, отчество, организация, рабочий номер, '
                   f'личный номер): ').lower()
    if choice == 'фамилия':
        profile.surname = input('\nВведите новое значение: ')
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])
    elif choice == 'имя':
        profile.name = input('\nВведите новое значение: ')
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])
    elif choice == 'отчество':
        profile.last_name = input('\nВведите новое значение: ')
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])
    elif choice == 'организация':
        profile.organization = input('\nВведите новое значение: ')
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])
    elif choice == 'рабочий номер':
        profile.work_number = int(input('\nВведите новое значение: '))
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])
    elif choice == 'личный номер':
        profile.number = int(input('\nВведите новое значение: '))
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])
    else:
        print('\nУказан неверный вариант!')

    replace_index = profiles.index(profile)
    profiles[replace_index] = profile
    save_data(profiles)
    return print(f'\nДанные изменены:\n{profile}\n')


def to_find() -> dict | None:
    """Функция описывающая логику для поиска записей."""

    choice = input('\nПо каким данным будет производиться поиск (имя или личный номер): ').lower()
    if choice == 'имя':
        context = Context(Name())
        name = input('\nВведите имя для поиска: ')
        found = context.find(name)
        if isinstance(found, dict):
            return print(found['error'])
    elif choice == 'номер' or choice == 'личный номер':
        context = Context(Number())
        number = input('\nВведите номер для поиска: ')
        found = context.find(number)
        if isinstance(found, dict):
            return print(found['error'])
    else:
        return print('\nБыл указан некорректный вариант!\n')
    return None
