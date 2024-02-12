from src.utils import hello, get_choice, add_new_profile

CHOICES = {
    1: add_new_profile,
    2: 'Редактировать запись в справочнике.',
    3: 'Вывести записи из справочника.',
    4: 'Выйти',
}


def main() -> None:
    """Основной 'движок' программы."""

    hello()

    while True:
        CHOICES[get_choice()]()


if __name__ == '__main__':
    main()
