from collections import UserDict

#Базовий клас для полів запису.
class Field:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, contact_name):
        self.contact_name = contact_name
        print("cheking name")
        
    def check_name(self):
        if len(self.contact_name) >= 2:
            print(f"cheking name returne :{self.contact_name}")
            return self.contact_name
        else:
            print("Name is too short")
            raise "Name is too short"
        
# Клас для зберігання номера телефону. Має валідацію формату (10 цифр)
class Phone(Field):
    def __init__(self, phone_number):
        self.phone = phone_number
    def check_phone_number(self):
        if len(self.phone) == 10 and self.phone.isdigit():
            return self.phone
        else:
            print("The number is incorrect. The phone number must consist of 10 digits ")
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
        self.b_day = value
        try:
            print("here")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")           

# Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, record_name, record_list):
        self.name = Name(record_name).check_name()
        self.phones = record_list
        self.birthday = None
        
    def add_phone(self, phone):
        if phone not in self.phones:
            print(f"Phone list :{self.phones}")
            self.phones.append(phone)
            print(f'Phone {phone} has been successfully added from contact {self.name}') 
        else:
            print(f"Phone {phone} already recorded for a contact {self.name}")
            raise "conflict of types"
    
    def remove_phone(self, phone):
        if phone in [p.value for p in self.phones]:
            self.phones = [p for p in self.phones if p.value != phone]
            print(f'Phone {phone} removed from contact {self.name}')
        else:
            print(f"Phone {phone} not found for contact {self.name}")
    
    def edit_phone(self, old_phone, new_pnone):
        if old_phone in [p.value for p in self.phones]:
            for phone in self.phones:
                if phone.value == old_phone: 
                    phone.value = new_pnone
            print(f'Phone nomber has been successfully modified')
        else:
            print(f"Phone {old_phone} not found for contact {self.name}")
    
    def find_phone(self, phone:Phone):
        if phone in [ph.value for ph in self.phones]:
            print(f'{self.name}: {phone}')
        else:
            print(f"Phone {phone} not found for contact {self.name}")
    

# Виведення всіх записів у книзі
    #def __str__(self):
    #    print("check __str__")
    #    return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"

 # Створення нової адресної книги
 # Додавання/видалення запису до адресної книги
class AddressBook(UserDict):
    def __init__(self, initial=None):
        if initial is None:
            self.address_book = dict()
        else:
            self.address_book = dict()
		
    def add_record(self, contact:Record):
        if contact.name not in [key for key in self.address_book]:
            self.address_book[contact.name] = contact.phones
            print("The contact has been saved")
        else:
            print(f"A contact {contact.name} already exists in the contact book")
    
    def find(self, name):
        if name in [key for key in self.address_book]:
            print(f"Contact name: {name}, phones: {self.address_book[name]}")
            return self.address_book[name]

                  
    def delete(self, name):
        if name in [key for key in self.address_book]:
            self.address_book.pop(name)
            print(f"Contact name: {name}, has been deleted")
        else:
            print(f"Contact: {name} are not exist)")
        pass
    
    
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please. "
        except KeyError:
            return "Give me correct name please."
        except TypeError:
            return "Give me correct name and phone please."
        except IndexError:
            return "Give me name and phone please. Wrong index"

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    add_contact_name, phone, *_ = args
    record = book.find(add_contact_name)
    chek_in_number=Phone(phone).check_phone_number()# перевіряємо перед записом чи номер введений правильно
    print(f"find record: {record}")
    if record == None:
        record = Record(add_contact_name,[])
        record.add_phone(chek_in_number)
        book.add_record(record)
        message = "Contact added."
    elif phone:
        #print("cheking phone number")
        #print(type(chek_in_number), chek_in_number)
        #print(f"old record: {type(record)}, {record}")
        record_rwr = Record(add_contact_name, record)
        record_rwr.add_phone(chek_in_number)
        message = "Contact updated."
    return message

@input_error
def check_contact(args, contacts):
        name = args
        return f"Phone nomber: {contacts[name[0]]}"

@input_error
def change_contact_number(args, contacts):
    name, phone = args
    if name in contacts.keys():
        contact_list[name] = phone
        return "Number chenging"
    else:
        return f"Contact Name: \"{name}\" - doesn't exist. Please check the Name and try again"      


@input_error    
def all_contacts(book: AddressBook):
    list=''
#    if book.address_book == None:
#        return "Phone book is empty"
    book_test = book.address_book
#    for key in book_test.keys():
 #           list+= f"Name: \"{book_test.keys[key]}\" Phone: {book_test.values[key]}\n"
    print(book_test)
    return book.__dict__       

def main():
    print("Welcome to the assistant bot!")
    while True:
        global contact_list 
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
            
        elif command == "all":
            print(all_contacts(book))  
              
        elif command == "phone":
            print(check_contact(args, contact_list))
            
        elif command == "change":    
            print(change_contact_number(args, contact_list))   
            
        elif command == "birthdays":
            # реалізація
            pass
        elif command == "show-birthday":
            # реалізація
            pass
        elif command == "add-birthday":
            # реалізація
            pass
        else:
            print("Invalid command.")
            
            
if __name__ == "__main__":
    book = AddressBook()
    main()