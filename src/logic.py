import re

from src.models import Profile
from src.utils import get_profiles, save_data


def get_choice() -> int:
    """Функция, описывающая логику для получения выбора пользователя."""

    str_choices = '1. Добавление новой записи в справочник;\n2. Редактировать запись в справочнике;\n' \
                  '3. Вывести записи из справочника;\n4. Выйти.\n'
    choice = int(input(f'Выберите, что хотите сделать (укажите цифру):\n{str_choices}\nВаш выбор: '))
    return choice


def get_profiles_with_pagination(profiles: list[Profile] = None, paginator: int = None) -> None:
    """Функция, описывающая логику для вывода строк из справочника."""

    if not profiles:
        profiles = get_profiles()
        if not profiles:
            return print('\nНет записей.\n')
    if not paginator:
        paginator = int(input('\nВведите сколько записей должно быть отображено за раз. '
                              '\nВаш выбор: '))

    for profile in profiles[:paginator]:
        print(profile)
        profiles.remove(profile)

    if profiles:
        choice = input('\nДалее? Ваш ответ (да или нет): ')
        if choice == 'да':
            get_profiles_with_pagination(profiles=profiles, paginator=paginator)
    else:
        print('\nВсе записи выведены.\n')


def add_new_profile() -> None:
    """Функция, описывающая логику для создания новой записи."""

    profiles = get_profiles()
    new_profile = Profile(
        surname=input('\nВведите вашу фамилию: ').title(),
        name=input('Введите ваше имя: ').title(),
        last_name=input('Введите ваше отчество: ').title(),
        organization=input('Введите вашу компанию: ').upper(),
        work_number=int(input('Введите ваш рабочий номер: ')),
        number=int(input('Введите ваш личный номер: ')),
    )

    data_check = new_profile.validate()
    if isinstance(data_check, dict):
        return print(data_check['error'])

    if profiles:
        fail = [
            profile for profile in profiles
            if str(profile.number) == str(new_profile.number)
            or str(profile.work_number) == str(new_profile.work_number)
        ]
        if fail:
            return print(f'\nЗапись с таким личным или рабочим номером уже существует:\n{fail[0].__str__()}\n')
        profiles.append(new_profile)
    else:
        profiles = [new_profile]

    save_data(profiles)
    print('\nЗапись добавлена!\n')


def edit_profile() -> None:
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

    choice = input(f'\n{profile}\nЧто вы хотите изменить (фамилия, имя, отчество, компания, рабочий номер, '
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
        profile.work_number = input('\nВведите новое значение: ')
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])
    elif choice == 'личный номер':
        profile.number = input('\nВведите новое значение: ')
        data_check = profile.validate()
        if isinstance(data_check, dict):
            return print(data_check['error'])

    replace_index = profiles.index(profile)
    profiles[replace_index] = profile
    save_data(profiles)
    print(f'\nДанные изменены:\n{profile}\n')


