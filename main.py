from src import hello, get_choice, add_new_profile, get_profiles_with_pagination, edit_profile

CHOICES = {
    1: add_new_profile,
    2: edit_profile,
    3: get_profiles_with_pagination,
    4: 'exit',
}


def main() -> None:
    """Основной 'движок' программы."""

    hello()

    while True:
        try:
            CHOICES[get_choice()]()
        except KeyError:
            print('\nВы указали неверный вариант. Попробуйте ещё раз!\n')
        except TypeError:
            print('\nХорошего дня!\n')
            break


if __name__ == '__main__':
    main()
