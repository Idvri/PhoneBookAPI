from .models import Profile


def hello() -> None:
    """Функция для приветствия."""

    print('Добрый день!\n')


def get_choice() -> int:
    """Функция для получения выбора пользователя."""

    str_choices = '1. Добавление новой записи в справочник,\n2. Редактировать запись в справочнике,\n' \
                  '3. Вывести записи из справочника.\n'
    choice = int(input(f'Выберите, что хотите сделать (укажите цифру):\n{str_choices}\nВаш выбор: '))
    return choice


def get_profiles() -> list[Profile] | list:
    """Функция для получения данных из файла."""

    with open('src/data.txt', 'r', encoding='utf-8') as data:
        nums = data.read()
        if nums:
            nums = nums.split('\n')
            nums = [Profile(*num.split(', ')) for num in nums[:-1]]
            return nums
        return []


def add_new_profile() -> None:
    """Функция для создания новой записи."""

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

    fail = [
        profile for profile in profiles
        if str(profile.number) == str(new_profile.number) or str(profile.work_number) == str(new_profile.work_number)
    ]
    if fail:
        return print(f'\nЗапись с таким личным или рабочим номером уже существует:\n{fail[0].__str__()}\n')

    profiles.append(new_profile)
    save_data(profiles)
    print('\nЗапись добавлена!\n')


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
