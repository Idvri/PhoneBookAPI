from src import get_choice, hello


def main() -> None:
    """Основной 'движок' программы."""

    hello()
    process = True

    while process:
        choice, process = get_choice()


if __name__ == '__main__':
    main()
