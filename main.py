from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (
            isinstance(value, str) and value.isdigit() and len(value) == 10
        ):
            raise ValueError("Phone number must be a 10-digit string of numbers.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def add_birthday(self, birthday):
        if isinstance(birthday, str):
            self.birthday = Birthday(birthday)
        elif isinstance(birthday, Birthday):
            self.birthday = birthday

    def remove_phone(self, phone_number):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone_number} not found.")

    def edit_phone(self, old_phone_number, new_phone_number):
        phone_to_edit = self.find_phone(old_phone_number)
        if phone_to_edit:
            phone_to_edit.value = Phone(new_phone_number).value
        else:
            raise ValueError(f"Phone number {old_phone_number} not found.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones = f"phones: {'; '.join(p.value for p in self.phones)}"
        birthday_info = ""
        if self.birthday:
            birthday_info = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        return f"Contact name: {self.name.value}, {phones}{birthday_info}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)

                delta_days = (birthday_this_year - today).days

                if 0 <= delta_days <= 7:
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() >= 5:
                        congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays


def main():
    book = AddressBook()
    separator = "-" * 20

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("02.11.1985")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)
    print(separator)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(f"John's record after editing phone: {john}")
    print(separator)

    found_phone = john.find_phone("5555555555")
    print(f"Found phone for John: {found_phone}")
    print(separator)

    book.delete("Jane")
    print("All records after deleting Jane's record:")
    for name, record in book.data.items():
        print(record)
    print(separator)

    print("Upcoming birthdays:")
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        for birthday_info in upcoming:
            print(f"Congratulate {birthday_info['name']} on {birthday_info['congratulation_date']}")
    else:
        print("No upcoming birthdays in the next week.")


if __name__ == "__main__":
    main()
