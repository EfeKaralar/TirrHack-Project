import pyrebase

#bu ikisinin proje basina konulmasi lazim
firebaseConfig = {
    'apiKey': "AIzaSyDBUL_GE-3iqmBMXWW6_xSZJVRrbTF4Sl8",
    'authDomain': "tirrhack-project.firebaseapp.com",
    'databaseURL': "https://tirrhack-project-default-rtdb.firebaseio.com/",
    'projectId': "tirrhack-project",
    'storageBucket': "tirrhack-project.appspot.com",
    'messagingSenderId': "211531752224",
    'appId': "1:211531752224:web:44ba9e904ba2797339ad45"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

#Family authentication

def create_family(name, familyId, password):
    families = db.child("families").order_by_child("id").equal_to(familyId).get()

    if families.val() != []:
        return "ID_ALREADY_EXISTS"
        
    db.child("families").push({
        "name": name,
        "id": familyId,
        "password": password,
    })

    return db.child("families").order_by_child("id").equal_to(familyId).get()[0].key()

def login_to_family(familyId, password):
    families = db.child("families").get()
    for family in families.each():
        if (family.val()["id"]) == familyId:
            print("Evet boyle bir aile var!")
            if (family.val()["password"]) == password:
                key = family.key()
                print("Successfully logged in to family ")
                return key
            else:
                return "WRONG_PASSWORD"
            
    print("ID not found!")
            

#in-family methods

def post_stickynote(key, text, date):
    data = db.child("families").child(key).child("stickynotes").get()
    newId = get_next_id(data)
    db.child("families").child(key).child("stickynotes").child(newId).set({
        "text": text,
        "date": date
    })

def get_stickynotes(key):
    return db.child("families").child(key).child("stickynotes").get().val()

def post_food_item(key, text, date):
    data = db.child("families").child(key).child("fooditems").get()
    newId = get_next_id(data)
    db.child("families").child(key).child("fooditems").child(newId).set({
        "name": text,
        "date": date
    })

def get_food_items(key):
    return db.child("families").child(key).child("fooditems").get().val()

def post_day(key, text, date):
    data = db.child("families").child(key).child("days").get()
    newId = get_next_id(data)
    db.child("families").child(key).child("days").child(newId).set({
        "description": text,
        "date": date
    })

def get_days(key):
    return db.child("families").child(key).child("days").get().val()

#get next available id

def get_next_id(database):
    #next_id = 0;
    #for i in database.each():
        #print(i.key(), " BU KEY")
        #print(next_id, " BU DA ID")
        #if int(i.key()) != next_id:
            #return next_id
        #next_id += 1
    #return next_id
    if database.val() == None:
        return 0
    last = database[-1].key()
    return last + 1

print(login_to_family(111111, "ALKFJA"))

    

