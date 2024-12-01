import json
import csv
import os
from datetime import datetime

NOTES_FILE = 'notes.json'
TASKS_FILE = 'tasks.json'
CONTACTS_FILE = 'contacts.json'
FINANCE_FILE = 'finance.json'

class Note:
    def __init__(self, id, title, content, timestamp):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Note(
            id=data['id'],
            title=data['title'],
            content=data['content'],
            timestamp=data['timestamp']
        )

class Task:
    def __init__(self, id, title, description, done, priority, due_date):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            done=data['done'],
            priority=data['priority'],
            due_date=data['due_date']
        )

class Contact:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    @staticmethod
    def from_dict(data):
        return Contact(
            id=data['id'],
            name=data['name'],
            phone=data['phone'],
            email=data['email']
        )

class FinanceRecord:
    def __init__(self, id, amount, category, date, description):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

    @staticmethod
    def from_dict(data):
        return FinanceRecord(
            id=data['id'],
            amount=data['amount'],
            category=data['category'],
            date=data['date'],
            description=data['description']
        )

def main_menu():
    while True:
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Выберите действие: ")
        if choice == '1':
            notes_menu()
        elif choice == '2':
            tasks_menu()
        elif choice == '3':
            contacts_menu()
        elif choice == '4':
            finance_menu()
        elif choice == '5':
            calculator()
        elif choice == '6':
            print("Спасибо за использование приложения")
            break
        else:
            print("Неверный ввод. Введите целое число от 1 до 6.")

def notes_menu():
    while True:
        print("\nУправление заметками")
        print("1. Создать новую заметку")
        print("2. Посмотреть список заметок")
        print("3. Посмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Импорт заметок из CSV")
        print("7. Экспорт заметок в CSV")
        print("8. Назад в главное меню")

        choice = input("Выберите действие: ")
        if choice == '1':
            create_note()
        elif choice == '2':
            list_notes()
        elif choice == '3':
            view_note()
        elif choice == '4':
            edit_note()
        elif choice == '5':
            delete_note()
        elif choice == '6':
            import_notes_csv()
        elif choice == '7':
            export_notes_csv()
        elif choice == '8':
            break
        else:
            print("Неверный ввод. Введите целое число от 1 до 8")

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [Note.from_dict(note) for note in data]

def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as file:
        json.dump([note.to_dict() for note in notes], file, ensure_ascii=False, indent=4)

def create_note():
    notes = load_notes()
    note_id = max([note.id for note in notes], default=0) + 1
    title = input("Введите заголовок заметки: ").strip()
    if not title:
        print("Заголовок не может быть пустым.")
        return
    content = input("Введите содержимое заметки: ")
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    note = Note(id=note_id, title=title, content=content, timestamp=timestamp)
    notes.append(note)
    save_notes(notes)
    print("Заметка успешно создана.")

def list_notes():
    notes = load_notes()
    if not notes:
        print("Список заметок пуст.")
        return
    print("\nСписок заметок:")
    for note in notes:
        print(f"ID: {note.id}, Заголовок: {note.title}, Дата: {note.timestamp}")

def view_note():
    note_id = input("Введите ID заметки для просмотра: ")
    notes = load_notes()
    for note in notes:
        if str(note.id) == note_id:
            print(f"\nЗаголовок: {note.title}")
            print(f"Содержимое: {note.content}")
            print(f"Дата: {note.timestamp}")
            return
    print("Заметка не найдена.")

def edit_note():
    note_id = input("Введите ID заметки для редактирования: ")
    notes = load_notes()
    for note in notes:
        if str(note.id) == note_id:
            title = input(f"Введите новый заголовок (текущий: {note.title}): ").strip()
            if not title:
                print("Заголовок не может быть пустым.")
                return
            content = input("Введите новое содержимое: ")
            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            note.title = title
            note.content = content
            note.timestamp = timestamp
            save_notes(notes)
            print("Заметка успешно обновлена.")
            return
    print("Заметка не найдена.")

def delete_note():
    note_id = input("Введите ID заметки для удаления: ")
    notes = load_notes()
    notes = [note for note in notes if str(note.id) != note_id]
    save_notes(notes)
    print("\nЗаметка успешно удалена.")

def import_notes_csv():
    filename = input("Введите имя CSV-файла для импорта: ")
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            notes = load_notes()
            for row in reader:
                note = Note(
                    id=int(row['id']),
                    title=row['title'],
                    content=row['content'],
                    timestamp=row['timestamp']
                )
                notes.append(note)
            save_notes(notes)
            print("Импорт завершен успешно.")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")

def export_notes_csv():
    filename = input("Введите имя CSV-файла для экспорта: ")
    notes = load_notes()
    if not notes:
        print("Нет заметок для экспорта.")
        return
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'content', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for note in notes:
            writer.writerow(note.to_dict())
    print("Экспорт завершен успешно.")

def tasks_menu():
    while True:
        print("\nУправление задачами")
        print("1. Добавить новую задачу")
        print("2. Просмотреть список задач")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Импорт задач из CSV")
        print("7. Экспорт задач в CSV")
        print("8. Фильтрация задач")
        print("9. Назад в главное меню")

        choice = input("Выберите действие: ")
        if choice == '1':
            create_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            mark_task_done()
        elif choice == '4':
            edit_task()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            import_tasks_csv()
        elif choice == '7':
            export_tasks_csv()
        elif choice == '8':
            filter_tasks()
        elif choice == '9':
            break
        else:
            print("Неверный ввод. Введите целое число от 1 до 9")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [Task.from_dict(task) for task in data]

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as file:
        json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)

def create_task():
    tasks = load_tasks()
    task_id = max([task.id for task in tasks], default=0) + 1
    title = input("Введите название задачи: ").strip()
    if not title:
        print("Описание задачи не может быть пустым.")
        return
    description = input("Введите подробное описание задачи: ")
    priority = input("Установите приоритет задачи (Высокий/Средний/Низкий): ")
    if priority not in ['Высокий', 'Средний', 'Низкий']:
        print("Некорректный приоритет. Установлен приоритет по умолчанию: Средний.")
        priority = 'Средний'
    due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")
    try:
        datetime.strptime(due_date, '%d-%m-%Y')
    except ValueError:
        print("Некорректный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    task = Task(id=task_id, title=title, description=description, done=False, priority=priority, due_date=due_date)
    tasks.append(task)
    save_tasks(tasks)
    print("Задача успешно создана.")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Список задач пуст.")
        return
    print("\nСписок задач:")
    for task in tasks:
        status = 'Выполнена' if task.done else 'Не выполнена'
        print(f"ID: {task.id}, Описание: {task.title}, Статус: {status}, Приоритет: {task.priority}, Срок: {task.due_date}")

def mark_task_done():
    task_id = input("Введите ID задачи для отметки как выполненной: ")
    tasks = load_tasks()
    for task in tasks:
        if str(task.id) == task_id:
            task.done = True
            save_tasks(tasks)
            print("Задача отмечена как выполненная.")
            return
    print("Задача не найдена.")

def edit_task():
    task_id = input("Введите ID задачи для редактирования: ")
    tasks = load_tasks()
    for task in tasks:
        if str(task.id) == task_id:
            title = input(f"Введите новое название (текущее: {task.title}): ")
            if not title:
                print("Описание задачи не может быть пустым.")
                return
            description = input("Введите новое подробное описание: ")
            priority = input(f"Установите новый приоритет (текущий: {task.priority}): ")
            if priority not in ['Высокий', 'Средний', 'Низкий']:
                print("Некорректный приоритет. Приоритет не изменен.")
            else:
                task.priority = priority
            due_date = input(f"Введите новый срок выполнения (текущий: {task.due_date}): ")
            try:
                datetime.strptime(due_date, '%d-%m-%Y')
                task.due_date = due_date
            except ValueError:
                print("Некорректный формат даты. Срок выполнения не изменен.")
            task.title = title
            task.description = description
            save_tasks(tasks)
            print("Задача успешно обновлена.")
            return
    print("Задача с введённым ID не найдена.")

def delete_task():
    task_id = input("Введите ID задачи для удаления: ")
    tasks = load_tasks()
    tasks = [task for task in tasks if str(task.id) != task_id]
    save_tasks(tasks)
    print("Задача успешно удалена.")

def import_tasks_csv():
    filename = input("Введите имя CSV-файла для импорта: ")
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = load_tasks()
            for row in reader:
                task = Task(
                    id=int(row['id']),
                    title=row['title'],
                    description=row['description'],
                    done=row['done'] == 'True',
                    priority=row['priority'],
                    due_date=row['due_date']
                )
                tasks.append(task)
            save_tasks(tasks)
            print("Импорт завершен успешно.")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")

def export_tasks_csv():
    filename = input("Введите имя CSV-файла для экспорта: ")
    tasks = load_tasks()
    if not tasks:
        print("Нет задач для экспорта.")
        return
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'description', 'done', 'priority', 'due_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task.to_dict())
    print("Экспорт завершен успешно.")

def filter_tasks():
    print("\nФильтрация задач")
    print("1. По статусу")
    print("2. По приоритету")
    print("3. По сроку выполнения")
    choice = input("Выберите фильтр: ")
    tasks = load_tasks()
    if not tasks:
        print("Список задач пуст.")
        return
    if choice == '1':
        status = input("Введите статус (Выполнена/Не выполнена): ")
        status = True if status == 'Выполнена' else False
        filtered_tasks = [task for task in tasks if task.done == status]
    elif choice == '2':
        priority = input("Введите приоритет (Высокий/Средний/Низкий): ")
        filtered_tasks = [task for task in tasks if task.priority == priority]
    elif choice == '3':
        due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
        filtered_tasks = [task for task in tasks if task.due_date == due_date]
    else:
        print("Некорректный выбор.")
        return
    if not filtered_tasks:
        print("Нет задач, соответствующих критериям фильтрации.")
        return
    for task in filtered_tasks:
        status = 'Выполнена' if task.done else 'Не выполнена'
        print(f"ID: {task.id}, Описание: {task.title}, Статус: {status}, Приоритет: {task.priority}, Срок: {task.due_date}")

def contacts_menu():
    while True:
        print("\nУправление контактами")
        print("1. Добавить новый контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Импорт контактов из CSV")
        print("6. Экспорт контактов в CSV")
        print("7. Назад в главное меню")

        choice = input("Выберите действие: ")
        if choice == '1':
            create_contact()
        elif choice == '2':
            search_contact()
        elif choice == '3':
            edit_contact()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            import_contacts_csv()
        elif choice == '6':
            export_contacts_csv()
        elif choice == '7':
            break
        else:
            print("Неверный ввод. Введите целое число от 1 до 7")

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [Contact.from_dict(contact) for contact in data]

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as file:
        json.dump([contact.to_dict() for contact in contacts], file, ensure_ascii=False, indent=4)

def create_contact():
    contacts = load_contacts()
    contact_id = max([contact.id for contact in contacts], default=0) + 1
    name = input("Введите имя контакта: ").strip()
    if not name:
        print("Имя не может быть пустым.")
        return
    phone = input("Введите номер телефона: ")
    email = input("Введите адрес электронной почты: ")
    contact = Contact(id=contact_id, name=name, phone=phone, email=email)
    contacts.append(contact)
    save_contacts(contacts)
    print("Контакт успешно добавлен.")

def search_contact():
    query = input("Введите имя или номер телефона для поиска: ").strip()
    contacts = load_contacts()
    found_contacts = [contact for contact in contacts if query.lower() in contact.name.lower() or query in contact.phone]
    if not found_contacts:
        print("Контакты не найдены.")
        return
    print("\nНайденные контакты:")
    for contact in found_contacts:
        print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, Email: {contact.email}")

def edit_contact():
    contact_id = input("Введите ID контакта для редактирования: ")
    contacts = load_contacts()
    for contact in contacts:
        if str(contact.id) == contact_id:
            name = input(f"Введите новое имя (текущее: {contact.name}): ").strip()
            if not name:
                print("Имя не может быть пустым.")
                return
            phone = input(f"Введите новый телефон (текущий: {contact.phone}): ")
            email = input(f"Введите новый email (текущий: {contact.email}): ")
            contact.name = name
            contact.phone = phone
            contact.email = email
            save_contacts(contacts)
            print("Контакт успешно обновлен.")
            return
    print("Контакт не найден.")

def delete_contact():
    contact_id = input("Введите ID контакта для удаления: ")
    contacts = load_contacts()
    contacts = [contact for contact in contacts if str(contact.id) != contact_id]
    save_contacts(contacts)
    print("Контакт успешно удален.")

def import_contacts_csv():
    filename = input("Введите имя CSV-файла для импорта: ")
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            contacts = load_contacts()
            for row in reader:
                contact = Contact(
                    id=int(row['id']),
                    name=row['name'],
                    phone=row['phone'],
                    email=row['email']
                )
                contacts.append(contact)
            save_contacts(contacts)
            print("Импорт завершен успешно.")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")

def export_contacts_csv():
    filename = input("Введите имя CSV-файла для экспорта: ")
    contacts = load_contacts()
    if not contacts:
        print("Нет контактов для экспорта.")
        return
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'phone', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact.to_dict())
    print("Экспорт завершен успешно.")

def finance_menu():
    while True:
        print("\nУправление финансовыми записями")
        print("1. Добавить новую запись")
        print("2. Просмотреть записи")
        print("3. Генерация отчёта")
        print("4. Подсчёт общего баланса")
        print("5. Импорт финансовых записей из CSV")
        print("6. Экспорт финансовых записей в CSV")
        print("7. Назад в главное меню")

        choice = input("Выберите действие: ")
        if choice == '1':
            create_finance_record()
        elif choice == '2':
            list_finance_records()
        elif choice == '3':
            generate_finance_report()
        elif choice == '4':
            calculate_balance()
        elif choice == '5':
            import_finance_csv()
        elif choice == '6':
            export_finance_csv()
        elif choice == '7':
            break
        else:
            print("Неверный ввод. Введите целое число от 1 до 7")

def load_finance_records():
    if not os.path.exists(FINANCE_FILE):
        return []
    with open(FINANCE_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return [FinanceRecord.from_dict(record) for record in data]

def save_finance_records(records):
    with open(FINANCE_FILE, 'w', encoding='utf-8') as file:
        json.dump([record.to_dict() for record in records], file, ensure_ascii=False, indent=4)

def create_finance_record():
    records = load_finance_records()
    record_id = max([record.id for record in records], default=0) + 1
    amount = input("Введите сумму операции (положительное число для дохода, отрицательное для расхода): ")
    try:
        amount = float(amount)
    except ValueError:
        print("Некорректная сумма.")
        return
    category = input("Введите категорию операции: ")
    date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
    try:
        datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        print("Некорректный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    description = input("Введите описание операции: ")
    record = FinanceRecord(id=record_id, amount=amount, category=category, date=date, description=description)
    records.append(record)
    save_finance_records(records)
    print("Финансовая запись успешно добавлена.")

def list_finance_records():
    records = load_finance_records()
    if not records:
        print("Список финансовых записей пуст.")
        return
    print("\nСписок финансовых записей:")
    for record in records:
        print(f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")

def generate_finance_report():
    start_date = input("Введите начальную дату периода (ДД-ММ-ГГГГ): ")
    end_date = input("Введите конечную дату периода (ДД-ММ-ГГГГ): ")
    try:
        start = datetime.strptime(start_date, '%d-%m-%Y')
        end = datetime.strptime(end_date, '%d-%m-%Y')
    except ValueError:
        print("Некорректный формат даты. Используйте ДД-ММ-ГГГГ.")
        return
    records = load_finance_records()
    filtered_records = [record for record in records if start <= datetime.strptime(record.date, '%d-%m-%Y') <= end]
    if not filtered_records:
        print("Нет записей за указанный период.")
        return
    total_income = sum(record.amount for record in filtered_records if record.amount > 0)
    total_expense = sum(record.amount for record in filtered_records if record.amount < 0)
    print(f"\nОтчет с {start_date} по {end_date}:")
    print(f"Общий доход: {total_income}")
    print(f"Общий расход: {total_expense}")
    print(f"Баланс: {total_income + total_expense}")

def calculate_balance():
    records = load_finance_records()
    balance = sum(record.amount for record in records)
    print(f"Текущий общий баланс: {balance}")

def import_finance_csv():
    filename = input("Введите имя CSV-файла для импорта: ")
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            records = load_finance_records()
            for row in reader:
                record = FinanceRecord(
                    id=int(row['id']),
                    amount=float(row['amount']),
                    category=row['category'],
                    date=row['date'],
                    description=row['description']
                )
                records.append(record)
            save_finance_records(records)
            print("Импорт завершен успешно.")
    except Exception as e:
        print(f"Ошибка при импорте: {e}")

def export_finance_csv():
    filename = input("Введите имя CSV-файла для экспорта: ")
    records = load_finance_records()
    if not records:
        print("Нет финансовых записей для экспорта.")
        return
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'amount', 'category', 'date', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_dict())
    print("Экспорт завершен успешно.")

def calculator():
    print("\nКалькулятор")
    expression = input("Введите выражение (например, 2 + 2): ")
    try:
        allowed_chars = set('0123456789+-*/(). ')
        if not set(expression).issubset(allowed_chars):
            raise ValueError("Использованы недопустимые символы.")
        result = eval(expression, {'__builtins__': None}, {})
        print(f"Результат: {result}")
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль.")
    except Exception as e:
        print(f"Ошибка в выражении: {e}")

if __name__ == "__main__":
    main_menu()