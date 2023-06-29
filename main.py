from db import DB
from centrex import Centrex

db = DB()
centrex = Centrex()

allEmails = db.findAllPendingEmails()

for row in allEmails:
    email = row[0]     
    response = centrex.searchContactsByEmail(email=email)
    contacts = response['results']
    for contact in contacts:
        id = contact['id']
        result= centrex.updateContactStatus(id, statusID=centrex.nuture_unsuscribed_id)
        x = 0
    db.updateAsProcessed(email=email, processed=1)
    x = 0