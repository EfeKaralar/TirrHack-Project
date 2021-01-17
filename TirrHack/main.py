import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.recycleview import RecycleView
from firebaseHelper import FireBaseHelper
from registeredDB import DataBase
import pyrebase

familyDB = FireBaseHelper()
familyKey = ""

class FirstScreen(Screen):
    name: "firstScreen"

    def regFamButton(self):
        sm.current = "enterFamily"

    def createButton(self):
        sm.current = "create"

    def registerButton(self):
        sm.current = "registry"

class Registry(Screen):
    familyID: ObjectProperty(None)
    password: ObjectProperty(None)

    def mainButton(self):
        sm.current = "firstScreen"

    def ifFamExists(self):

        global familyKey

        if(self.familyID.text != "") and (self.password.text != ""):
            if(self.familyID.text.isdigit() == True):

                checkEnt = familyDB.login_to_family(int(self.familyID.text), self.password.text)

                if(checkEnt == "ID not found!"):
                    errorPopup = Popup(title='Error!', content=Label(text='ID not found'), size_hint=(None, None), size=(400, 400))
                    errorPopup.open()
                elif(checkEnt == "WRONG_PASSWORD"):
                    errorPopup = Popup(title='Error!', content=Label(text='Wrong Password'), size_hint=(None, None), size=(400, 400))
                    errorPopup.open()
                else:
                    familyKey = checkEnt
                    sm.current = "family"
            else:
                errorPopup = Popup(title='Error!', content=Label(text='ID Should be an Integer!'), size_hint=(None, None), size=(400, 400))
                errorPopup.open()
        else:
            errorPopup = Popup(title='Error!', content=Label(text='Please Fill Out All Spaces!'), size_hint=(None, None), size=(400, 400))
            errorPopup.open()


class Create(Screen):
    newFam: ObjectProperty(None)
    newID: ObjectProperty(None)
    newPass: ObjectProperty(None)
    newPassRep: ObjectProperty(None)

    def mainButton(self):
        sm.current = "firstScreen"

    def addFamily(self):

        if(self.newFam.text != "") and (self.newID.text != "") and (self.newPass.text != "") and (self.newPassRep.text != ""):
            if(self.newID.text.isdigit() == True):
                if(self.newPass.text == self.newPassRep.text):

                    check = familyDB.create_family(self.newFam.text, int(self.newID.text), self.newPass.text)

                    if(check == "ID_ALREADY_EXISTS"):
                        errorPopup = Popup(title='Error!', content=Label(text='ID Already Exists'), size_hint=(None, None), size=(400, 400))
                        errorPopup.open()

                    print(self.newFam.text, self.newPass.text)
                    self.newPass.text = ""
                    self.newID.text = ""
                    self.newFam.text = ""
                    self.newPassRep.text = ""
                else:
                    errorPopup = Popup(title='Error!', content=Label(text='Passwords do not match!'), size_hint=(None, None), size=(400, 400))
                    errorPopup.open()
            else:
                errorPopup = Popup(title='Error!', content=Label(text='ID should be an integer!'), size_hint=(None, None), size=(400, 400))
                errorPopup.open()
        else:
            errorPopup = Popup(title='Error!', content=Label(text='Please Fill Out All Spaces!'), size_hint=(None, None), size=(400, 400))
            errorPopup.open()

class EnterFamily(Screen):

    def mainButton(self):
        sm.current = "firstScreen"

    def on_enter(self, *args):
        for index,cha in enumerate(registeredDB.):
            cha = Button(text = cha, size_hint = (0.5, 0.1), pos_hint ={'x': 0.25, 'y': 0.75-(index*0.14)})
            self.add_widget(cha)

famName = []
famName.append("lelor")

class FamilyWindow(Screen):
    pass

class NotesWindow(Screen):

    def on_enter(self, *args):

        global familyKey
        noteList = familyDB.get_stickynotes(familyKey)

        for index, note in enumerate(noteList):
            cha = Button(text=note.val()["title"], size_hint=(0.5, 0.1), pos_hint={'x': 0.25, 'y': 0.75 - (index*0.14)}, on_press=lambda x: self.show_note(note))
            self.add_widget(cha)


    def show_note(self, *args):

        for arg in args:
            print(arg)

        popup = Popup(title=args[0].val()["title"], content=Label(text=args[0].val()["desc"]), size_hint=(None, None), size=(400, 400))
        popup.open()

class AddNotesWindow(Screen):
    note_title = ObjectProperty(None)
    note = ObjectProperty(None)

    def add_note_button(self):
        notes_list.append(self.note_title.text)
        notes_dict[self.note_title.text] = self.note.text
        self.note_title.text = ""
        self.note.text = ""

    def get_title(self):
        return self.note_title.text


class FridgeWindow(Screen):
    food: ObjectProperty(None)
    exp_date: ObjectProperty(None)

    def btn(self):
        print("Food name:", self.food.text, "Days to eat:", self.exp_date.text)

        food_list.append(self.food.text)
        exp_list.append(self.exp_date.text)

        self.food.text = ""
        self.exp_date.text = ""

class ViewFridgeWindow(Screen):
    food: ObjectProperty(None)
    exp_date: ObjectProperty(None)

    def switchtofridgewindow(self):
        sm.current = "fridge"

    def switchtodeletewindow(self):
        sm.current = "deleteWindow"

    def on_enter(self, *args):

        # self.add_widget(Label(text= "Food Name" , font_size=30, size_hint = (0.4, 0.1), pos_hint ={'x': 0.1, 'y': 0.9}))
        # self.add_widget(Label(text="Exp Date", font_size=30, size_hint=(0.4, 0.1), pos_hint={'x': 0.5, 'y': 0.9}))

        for i, c in enumerate(food_list):
            self.label1 = Label(text=c, font_size=30, size_hint=(0.4, 0.1),
                                pos_hint={'x': 0.1, 'y': 0.8 - (i * 0.1 + i * 0.04)})
            self.add_widget(self.label1)

        for i, c in enumerate(exp_list):

            if exp_list[-1] == "1":
                self.label2 = Label(text=c + " day", font_size=30, size_hint=(0.4, 0.1),
                                    pos_hint={'x': 0.5, 'y': 0.8 - (i * 0.1 + i * 0.04)})
                self.add_widget(self.label2)
            else:
                self.label2 = Label(text=c + " days", font_size=30, size_hint=(0.4, 0.1),
                                    pos_hint={'x': 0.5, 'y': 0.8 - (i * 0.1 + i * 0.04)})
                self.add_widget(self.label2)

        # self.delete_food = Button(text="Delete Food", font_size=30, size_hint = (0.4, 0.1), pos_hint ={'x': 0.3, 'y': 0.1})
        # self.add_widget(self.delete_food

class DeleteWindow(Screen):

    deletefood: ObjectProperty(None)

    def delete_food(self, *args):
        if str(self.deletefood.text) not in food_list:
            popup = Popup(title='Name Error', content=Label(text='No foods named: ' + str(self.deletefood.text)), size_hint=(None, None), size=(300, 300))
            popup.open()
        else:
            food_list.remove(str(self.deletefood.text))
            print((food_list))
            self.deletefood.text = ""


class SpecialDatesWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase()

sm.add_widget(FirstScreen(name="firstScreen"))
sm.add_widget(Registry(name="registry"))
sm.add_widget(Create(name="create"))
sm.add_widget(EnterFamily(name="enterFamily"))
sm.add_widget(FamilyWindow(name="family"))
sm.add_widget(NotesWindow(name="notes"))
sm.add_widget(AddNotesWindow(name="addnotes"))
sm.add_widget(FridgeWindow(name="fridge"))
sm.add_widget(ViewFridgeWindow(name="viewfridge"))
sm.add_widget(DeleteWindow(name="deleteWindow"))
sm.add_widget(SpecialDatesWindow(name="specialdates"))


screens = [Screen(name='firstScreen'), Screen(name='registry'), Screen(name='create'), \
           Screen(name='enterFamily'), Screen(name='family'), Screen(name='notes'), \
           Screen(name='addnotes'), Screen(name='fridge'), Screen(name='viewfridge'),\
           Screen(name='specialdates')]

notes_list = []
notes_dict = {}
button_names_list = []

fam_dict = {}
food_list = []
exp_list = []

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()
