import os, sys, getopt, json

FILE_PATH = "Contact List/data/contacts.json"

def open_addressbook(filepath):

    path_exists = os.path.exists(filepath)
    addressbook = None

    if path_exists:
        with open(filepath,"r") as infile:
            addressbook = json.load(infile)

    return addressbook

def list_contacts(filepath):

    addressbook = open_addressbook(filepath=filepath)

    if addressbook:
        for contact in addressbook["contacts"]:
            print(f"Name: "+contact["name"], "Telephone: "+contact["phone"], "Address: "+contact["address"] ,sep="\t",end='\n')

    else:
        print("No address book found!")

def retrieve_contact(filepath,name):
    contact_details = None
    addressbook = open_addressbook(filepath=filepath)
    print("Finding ",name)

    if addressbook:
        for contact in addressbook["contacts"]:
            if contact["name"] == name:
                contact_details = contact
                break

    else:
        print("No address book found!")

    print("Name: "+contact_details["name"], "Telephone: "+contact_details["phone"], "Address: "+contact_details["address"],sep='\t',end="\n")
    return contact_details  


def add_contact(filepath):
    new_contact = {}
    fullname = input("Please enter the contact name: ")
    print(fullname)

    # Have we got a name to add?
    if fullname:
        new_contact["name"] = fullname
        new_contact["phone"] = str(input("Please enter their phone number: "))
        new_contact["address"] = input("please enter their address: ")

        # try to open the current addressbook
        addressbook = open_addressbook(filepath=filepath)

        if addressbook is None:
            # If there was no addressbook create one
            print("Creating new address book")
            contacts = []
            addressbook = {"filetype":"Addressbook",
                            "application":"address-cli.py",
                            "contacts":contacts}
            
        print(new_contact)
        with open(filepath,"w") as outfile:
            # Write the output file with the new contact
            addressbook["contacts"].append(new_contact)
            json.dump(addressbook,outfile)

def remove_contact(filepath,name):

    # Have we got a name to remove?
    if name:
        # try to open the current addressbook and find the contact index
        addressbook = open_addressbook(filepath)
        contact = retrieve_contact(filepath=filepath,name=name)

        if contact:
            with open(filepath,"w") as outfile:
                # If contact was found delete it
                addressbook["contacts"].remove(contact)
                json.dump(addressbook,outfile)
                print(f"Contact: {contact} removed.\n")


def help():
    cmd_help = 'address-cli.py -h -i <input file> -l -a -r -f <contact to find>"'
    print(cmd_help)

def process_options(argv,inputfile):

    action = ""
    contact = ""
    options = {}

    try:
        opts, args = getopt.getopt(argv,"hi:lar:f:", ["help","ifile=","list","add","remove","find="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()

        elif opt in ("-i","--ifile"):
            inputfile = arg
        
        elif opt in ("-l", "--list"):
            action = "list"

        elif opt in ("-a","--add"):
            action = "add"

        elif opt in ("-r","--remove"):
            action = "remove"

        elif opt in ("-f","--find"):
            action = "find"
            contact = arg
    
    if action == "":
        # If there are no actions display the help and quit the program
        help()
        sys.exit(2)

    options["filepath"] = inputfile
    options["action"] = action
    options["contact"] = contact
    
    return options


def main(argv):
    options = process_options(argv,FILE_PATH)

    # Process the actions
    if options["action"] == "list":
        list_contacts(options["filepath"])
    
    elif options["action"] == "add":
        add_contact(options["filepath"])

    elif options["action"] == "remove":
        remove_contact(options["filepath"],options["contact"])

    elif options["action"] == "find":
        retrieve_contact(options["filepath"],options["contact"])


if __name__ == "__main__":
    main(sys.argv[1:])