import json 

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