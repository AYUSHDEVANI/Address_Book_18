import os
import sqlite3
DATABASE_PATH = "Contact List/data/addressbook.db"

class AddressDatabase(object):

    def __init__(self,db_path = DATABASE_PATH):
        self._db_conn = None
        self._db_path = db_path
        

    def __enter__(self):
        self.open_db()
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self._db_conn.close

    def open_db(self):

        path_exists = os.path.exists(self._db_path)

        self._db_conn = sqlite3.connect(self._db_path)

        # If the path didn`t exist then we`ve created a new database file
        if not path_exists:
            self.createdb()

        return path_exists

    def createdb(self):

        with self._db_conn:
            # Create contacts table
            self._db_conn.execute('''CREATE TABLE IF NOT EXISTS contacts
                                    ( contact_id INTEGER PRIMARY KEY,
                                    first_name TEXT,
                                    last_name TEXT
                                    )''')
            self._db_conn.commit()

            # Create address, phone and email table
            self._db_conn.execute('''CREATE TABLE IF NOT EXISTS address
                                    ( address_id INTEGER PRIMARY KEY,
                                    contact_id INTEGER,
                                    street TEXT,
                                    address_2 TEXT,
                                    address_3 TEXT,
                                    town TEXT,
                                    country TEXT,
                                    postcode TEXT,
                                    FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
                                     )''')

            self._db_conn.execute('''CREATE TABLE IF NOT EXISTS phone
                                    ( phone_id INTEGER PRIMARY KEY,
                                    contact_id INTEGER,
                                    phone_number TEXT,
                                    type TEXT,
                                    FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
                                     )''')

            self._db_conn.execute('''CREATE TABLE IF NOT EXISTS email
                                    ( email_id INTEGER PRIMARY KEY,
                                    contact_id INTEGER,
                                    email_address TEXT,
                                    type TEXT,
                                    FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
                                     )''')

            self._db_conn.commit()



    def table_exists(self,table_name):
        cursor = self._db_conn.cursor()
        exists = False

        # Check for the table
        cursor.execute('''SELECT name FROM sqlite_master WHERE type="table" AND name='?';'''),table_name


        if cursor.rowcount > 0:
            exists = True

        return exists


    def update_contact(self,contact):

        cursor = self._db_conn.cusor()
        cursor.execute('''UPDATE contacts SET first_name = ?, SET last_name = ? WHERE contact_id =?''',
                        (contact["first_name"],contact["last_name"],contact["id"]))

        self._db_conn.commit()

    def insert_contact(self,contact):
        cursor = self._db_conn.cursor()
        cursor.execute('''INSERT INTO contacts(first_name, last_name) VALUES(?,?)''',
                        (contact['first_name'], contact['last_name']))

        self._db_conn.commit()

        return cursor.lastrowid

    def remove_contact(self,contact_id):
        pass

    def insert_email(self,contact_id,email_details):

        cursor = self._db_conn.cursor()
        cursor.execute('''INSERT INTO email(contact_id, email_address, type) VALUES(?,?,?)''',
                        (contact_id,email_details["email_address"], email_details["type"]))

        self._db_conn.commit()

        return cursor.lastrowid

    
    def update_email(self,email_details):
        cursor = self._db_conn.cursor()
        cursor.execute('''UPDATE email SET email_address = ?, SET type = ? WHERE email_id = ?''',
                        (email_details["email_address"], email_details["type"], conemail_detailstact["id"]))
        self._db_conn.commit()

        return cursor.lastrowid
        pass

    def remove_email(self,email_id):
        pass


    def insert_address(self,contact_id,address_details):
        pass

    def update_address(self,address_details):
        pass

    def remove_address(self,address_id):
        pass

    def insert_phone(self,contact_id,phone_details):
        pass

    def update_phone(self,phone_details):
        pass

    def remove_phone(self,phone_id):
        pass 


    def get_contact_by_name(self,contact_name):

        contact = None
        result = {}
        success = False

        cursor = self._db_conn.cursor()
        print(contact_name["first_name"],contact_name['last_name'])
        cursor.execute('''SELECT * FROM contacts WHERE first_name LIKE ? AND last_name LIKE ?''',
                        (contact_name["first_name"],contact_name["last_name"]))
        
        rows = cursor.fetchall()

        num_rows = len(rows)
        result["rows"] = rows
        result["num_rows"] = num_rows

        # If we just one contact returned get the contact_id
        if num_rows == 1:
            contact = rows[0]
            success = True
        
        result["success"] = success
        result["contact"] = contact

        return result

    @property
    def addressbook(self):
        pass

    @property
    def num_contacts(Self):
        pass

    @property
    def contacts(self):
        pass

def main():
    # a = AddressDatabase()
    # a.createdb()

    with AddressDatabase() as addressbook:
        addressbook.createdb()
        if addressbook.table_exists("contacts"):
            print("contacts table exists")

        new_contact = {}
        new_email = {}
        new_contact["first_name"] = "Ayush"
        new_contact["last_name"] = "Devani"
        new_email["email_address"] = "email@gmail.com"
        new_email["type"] = "home"
        contact_id = addressbook.insert_contact(new_contact)
        addressbook.remove_contact(1)
        print(contact_id)
        print(addressbook.insert_email(contact_id, new_email))
        print(addressbook.get_contact_by_name(new_contact))
     

if __name__ == "__main__":
    # a.createdb()
    main()