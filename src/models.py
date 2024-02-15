import re

PATTERNS = {
    'strings': re.compile(r'^[A-ZА-Я][a-zа-я]+$'),
    'numbers': re.compile(r'^\d{11}$'),
}


class Profile:

    def __init__(
            self,
            surname: str,
            name: str,
            last_name: str,
            organization: str,
            work_number: str,
            number: str,
    ) -> None:
        self.surname = surname
        self.name = name
        self.last_name = last_name
        self.organization = organization
        self.work_number = work_number
        self.number = number

    def __str__(self) -> str:
        return f'{self.surname}, {self.name}, {self.last_name}, {self.organization}, {self.work_number}, {self.number}'

    def validate(self) -> dict | bool:
        """Функция для валидации данных."""

        pattern = PATTERNS['strings']
        if not pattern.match(self.surname):
            error = '\nУказана неверная фамилия!\n'
            return {'status': False, 'error': error}
        elif not pattern.match(self.name):
            error = '\nУказано неверное имя!\n'
            return {'status': False, 'error': error}
        elif not pattern.match(self.last_name):
            error = '\nУказано неверное отчество!\n'
            return {'status': False, 'error': error}

        pattern = PATTERNS['numbers']
        if not pattern.match(self.work_number):
            error = '\nРабочий номер заполнен некорректно!\n'
            return {'status': False, 'error': error}
        elif not pattern.match(self.number):
            error = '\nЛичный номер заполнен некорректно!\n'
            return {'status': False, 'error': error}

        return True
