from .models import Profile


def hello() -> None:
    """Функция для приветствия."""

    print('Добрый день!\n')


def get_profiles() -> list[Profile] | None:
    """Функция для получения данных из файла."""

    with open('src/data.txt', 'r', encoding='utf-8') as data:
        nums = data.read()
        if nums:
            nums = nums.split('\n')
            nums = [Profile(*num.split(', ')) for num in nums[:-1]]
            return nums
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
