import json 
from subprocess import call
import sys
from time import sleep

######################################################

class ContactBook:
    def __init__(self,log_file):
        self.log_file = log_file
        self.name = 'N/A'
        self.phone = 'N/A'
        self.email = 'N/A'
        self.address = 'N/A'
        self.notes = []
        
    def log_contact(self):
        contact_info = {
            "name":self.name,
            "phone":self.phone,
            "email":self.email,
            "address":self.address,
            "notes":self.notes}
        file = open(self.log_file,'r')
        data = json.load(file)
        data["contacts"].append(contact_info)
        file.close()
        update_file = open(self.log_file,'w')
        json_data = json.dumps(data,indent=4)
        update_file.write(json_data)
        update_file.close()
        
    def pull_contacts(self):
        file = open(self.log_file)
        data = json.load(file)
        file.close()
        return data['contacts']

######################################################

contact_file = 'contact_info.json'
passkey = 'root'

######################################################
### Dev Commands ###          

def dev_menu():
    call('clear')
    print(' [sudo] Enter 1 to fill contact book.')
    print(' [sudo] Enter 2 to wipe all contacts.')
    select = input(' [sudo] ')
    if select == '1':
        fill_contacts()
    elif select == '2':
        deleted_all_contacts()
 
def fill_contacts():
    contact_count = input(' [sudo] Enter number of test contacts to add: ')
    for i in range(1, int(contact_count)):
        contact = ContactBook(contact_file)
        contact.name = 'Test Contact ' + str(i)
        contact.phone = 'Test Contact ' + str(i)
        contact.email = 'Test Contact ' + str(i)
        contact.address = 'Test Contact ' + str(i)
        contact.log_contact()
    print(f' [sudo] Added {str(contact_count)} test contacts.')
    print(' [sudo] Process completed.')

def deleted_all_contacts():
    call('clear')
    print(' [sudo] Are you sure you want to delete all contacts?')
    print(' [sudo] Enter dev password to wipe json file.')
    confirm = input(' [sudo] ')
    if confirm == passkey:
        new_dict = {"contacts":[]}
        file = open(contact_file,'w')
        new = json.dumps(new_dict)
        file.write(new)
        file.close()
        call('clear')
        print(' [sudo] Contact information erased.')
    else:
        call('clear')
        print(' [sudo] Denied. Redirecting...')
        sleep(3)
        home_ui()

######################################################

def create_contact():
    call('clear')
    new_contact = ContactBook('contact_info.json')
    print(' [+] Enter info below to add contact.')
    print(' [+] Leave blank to skip.')
    print(' [+] (Press enter to confirm)\n')
    name = input(' [+] Contact name: ')
    if name: new_contact.name = name.strip()
    phone = input(' [+] Phone number: ')
    if phone: new_contact.phone = phone.strip()
    email = input(' [+] Email address: ')
    if email: new_contact.email = email.strip()
    address = input(' [+] Personal address: ')
    if address: new_contact.address = address.strip()
    notes = input(' [+] Note for contact: ')
    if notes: new_contact.notes.append(notes)
    
    new_contact.log_contact()
    
def view_contacts():
    call('clear')
    contacts = ContactBook(contact_file)
    all_contact_objs = contacts.pull_contacts()
    print('\n ------------------------------ \n')
    for obj in all_contact_objs:
        print('- Name : ' + obj['name'])
        print('- Phone: ' + obj['phone'])
        print('- Email: ' + obj['email'])
        print('- Address: ' + obj['address'])
        if obj['notes']:
            print(' - Notes: ')
            print('\t - ' + note for note in obj['notes'])
        else:
            print(' - No notes. ')
        print('\n ------------------------------ \n')
   
def find_contact():
    call('clear')
    # List to store all objects with matching parameters.
    found_contacts = []
    # Create object to load JSON data.
    contacts = ContactBook(contact_file)
    all_contacts = contacts.pull_contacts()
    # Input to take in which attribute we're searching for.
    print(" [!] How do you want to search for this contact?")
    print(" [!] (By name, phone, etc.)\n")
    search_char = input(' [>] ')
    # Input for the value the target attr has to match.
    print('\n [!] What value do you want to seach for under "' + search_char + '"?')
    value = input(' [>] ')
    call('clear')
    print(' [!] Searching for contacts...')
    for contact in all_contacts:
        try:
            # If the target value matches the attr,
            # append object to found_contacts list.
            sample = contact[search_char.lower()]
            if value.lower() in sample:
                found_contacts.append(contact)
        except KeyError:
            # If the user inputs an attribute that isn't in the object,
            # retry input.
            # There's a fuckin bug here that I don't know how to fix yet.
            # Incorrect value error persists even after reset and correct 
            # attr value is added. 
            call('clear')
            print(f' [X] Error: "{search_char.lower()}" is not a searchable option.')
            # 
            # input(' [!] Press enter to retry.')
            # find_contact()
            print(" [X] Because I can't fix this recursion bug,\n the program will now exit.")
            sys.exit()

            
    call('clear')
    # Redirect if found_contacts list is empty.
    if not found_contacts:
        print(f' [!] No contacts found with {search_char.lower()} = "{value.lower()}" ')
        input(' [!] Press enter to return home.')
        home_ui()
    # If multiple objects found, each object is given an 
    # ID and user selects object with input.
    elif len(found_contacts) > 1:
        print(f" [!] Contacts found: {str(len(found_contacts))}.")
        input(' [!] Press enter to view details.')
        print('\n ------------------------------ \n')
        # Target each object in the "found" list.
        for i in range(0,len(found_contacts)):
            target_contact = found_contacts[i]
            # Assign the temporary ID
            target_contact["id"] = str(i + 1)
            print(' [!] Contact #' + target_contact['id'])
            # If searched for "name", display name and phone.
            if search_char.lower() != "name":
                print('\n\t - Name: ' + target_contact['name'])
                print(f'\t - {search_char[0].upper() + search_char[1:].lower()}: {target_contact[search_char.lower()]}')
            # If searched for anything else, display name and searched attr.
            else:
                print('\n\t - Name: ' + target_contact['name'])
                print('\t - Phone: ' + target_contact['phone'])
            print('\n ------------------------------ \n')
        # User selects object by temporary ID.
        print(' [!] Enter a contact number to see its details.')
        while True:
            selected_contact = input(' [>] ')
            # Find and return 
            for x in found_contacts:
                return x if x["id"] == selected_contact
            print(' [X] Error: not a valid ID number.')
            print(' [X] Try again.')
        
######################################################

def home_ui():
    call('clear')
    print('# Contact Book #')
    print('- Version: 1.0')
    
    print(' [N] - Create new contact')
    print(' [V] - View all contacts.')
    print(' [S] - Search in contacts.')
    
    select = input('\n[>] ')
    select = select.lower()
    if select == 'test':
        testing()
    elif select == 'n':
        create_contact()
    elif select == 'v':
        view_contacts()
    elif select == 's':
        find_contact()
    elif select == 'sudo':
        password = input(' [sudo] ')
        if password == passkey:
            dev_menu()
        else:
            home_ui()
    else:
        home_ui()
            
 
######################################################
# Testing #
def testing():
    print(' ### TESTING ###')
    
 
######################################################

if __name__ == '__main__':
    try:
        call('clear')
        home_ui()
    except KeyboardInterrupt:
        print('\n [!] Proccess cancelled.')
        

######################################################