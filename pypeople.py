import json 
from subprocess import call
import sys
from time import sleep
from ContactBook import ContactBook

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

    
def view_all_contacts():
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
            for note in obj['notes']:
                print('    * ' + note)
        else:
            print(' - No notes. ')
        print('\n ------------------------------ \n')
    input(' [!] Press enter to return to menu.')
    home_ui()

   
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
            if value.lower() in sample.lower():
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
    elif len(found_contacts) == 1:
        display_contact(found_contacts[0])
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
                if x["id"] == selected_contact:
                    display_contact(x)
            print(' [X] Error: not a valid ID number.')
            print(' [X] Try again.')


def display_contact(contact_dict):
    call('clear')
    obj = contact_dict
    # Display contact 
    print('\n ------------------------------ \n')
    print(' - Name : ' + obj['name'])
    print(' - Phone: ' + obj['phone'])
    print(' - Email: ' + obj['email'])
    print(' - Address: ' + obj['address'])
    # Display all notes store, if there are any
    if obj['notes']:
        print(' - Notes: ')
        for note in obj['notes']:
            print('   * ' + note)
    else:
        print(' - No notes. ')
    print('\n ------------------------------ \n')
    # User options to edit/delete/return home
    print(' [!] Select an option: ')
    print(' [E] - Edit, [D] - Delete, [ENTER] - Return to menu \n')
    select = input(' [>] ')
    # Route user dependent on selection
    if select.lower() == 'e':
        edit_contact(contact_dict)
    elif select.lower() == 'd':
        delete_contact(contact_dict)
    else:
        home_ui()
    
    
def edit_contact(contact_dict):
    call('clear')
    contactbook = ContactBook(contact_file)
    all_contacts = contactbook.pull_contacts()
    target_contact_index = all_contacts.index(contact_dict)
    original_obj = all_contacts[target_contact_index]
    obj = contact_dict
    print(f' [!] Enter the attribute for {contact_dict["name"]} you\'d like to change.')
    target_attr = input(' [>] ')
    try:
        original_attr = obj[target_attr]
    except KeyError:
        print('[X] Error: "' + target_attr + '" is not a defined attribute.')
        print(' [X] Press enter to try again.')
        input()
        edit_contact(obj)
    call('clear')
    print(f'[!] The original {target_attr.lower()} for {obj["name"]} is {original_attr}.')
    print(' [!] Enter the new value and press enter.')
    new_value = input(f' [+] New {target_attr.lower()}: ')
    obj[target_attr] = new_value
    call('clear')
    print(f' [+] Press enter to save new {target_attr.lower()} for {original_obj["name"]}')
    input(f' [+] New {target_attr.lower()}: ' + new_value + ' ')
    print(' [+] Saving...')
    all_contacts[target_contact_index] = obj
    contactbook.update_contacts(all_contacts)
    print(' [+] Changes saved!')
        

def delete_contact(contact_dict):
    call('clear')
    print(' [!] WARNING ')
    print(' [!] Deleting a contact cannot be reversed and all data will be lost from program data.')
    print(f' [!] Are you sure you want to delete all data for {contact_dict["name"]}?')
    print(' [!] Type DELETE to proceed. \n')
    confirm = input(' [X] ')
    if confirm == 'DELETE':
        call('clear')
        print(' [-] Confirmed.')
        print(f' [-] Deleting data for {contact_dict["name"]}...')
        contactbook = ContactBook(contact_file)
        print(' ... ')
        all_contacts = contactbook.pull_contacts()
        print(' ... ')
        all_contacts.remove(contact_dict)
        print(' ... ')
        contactbook.update_contacts(all_contacts)
        print(' ... ')
        print(f' [!] {contact_dict["name"]} removed.')
        input(' [>] Press enter to return to the menu.')
        home_ui()
    else:
        print(' [X] Denied.')
        input(' [X] Press enter to return to the menu.')
        home_ui()
        
    
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
        view_all_contacts()
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
    test_dict = {
            "name": "test1",
            "phone": "test2",
            "email": "test3",
            "address": "test4",
            "notes": ["test5","test6","test7"]
        }
    edit_contact(test_dict)
    
######################################################

if __name__ == '__main__':
    try:
        call('clear')
        home_ui()
    except KeyboardInterrupt:
        print('\n [!] Proccess cancelled.')
        
######################################################