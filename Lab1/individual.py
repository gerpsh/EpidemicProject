#individual class represents a lab member

class Individual:

    #constructor method
    def __init__(self, idear):
        self.id = idear
        self.contacts = []
        self.infected = False

    #appends list of contacts to own list of contacts
    def addContacts(self, newContacts):
        presentContacts = self.contacts + newContacts
        self.contacts = presentContacts
