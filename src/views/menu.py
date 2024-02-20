from helpers.authentication_helper import AuthenticateHelper
from helpers.user_helper import UserHelper
from helpers.event_helper import EventHelper
from settings.config import constants, menu, prompts
from utils import logs

class Menu:
    
    def __init__(self):
        self.auth_helper = AuthenticateHelper()
        self.user_helper = UserHelper()
        self.event_helper = EventHelper()
    
    
    def navigate_check_role(self, details):
        if details[1] == constants["ADMIN"]:
            self.admin_menu(details[0])
            return
        elif details[1] == constants["CUSTOMER"]:
            self.customer_menu(details[0]) 
            return
        else:
            self.manager_menu(details[0])
            return
        
        
    def start_view(self): 
        while True:
            print(menu["START_VIEW"])
            choice = input()
            if choice == constants["ONE"]:
                details = self.auth_helper.login()
                if details:
                    self.navigate_check_role(details)    
                else:
                    print(prompts["WRONG_CREDENTIALS"])
                    continue
            elif choice == constants["TWO"]:
                user_role = constants["CUSTOMER"]
                self.user_helper.signup(user_role)
            elif choice == constants["THREE"]:
                logs.exit_app()
                break
            else:
                print(prompts["WRONG_INPUT"])

            
    def admin_menu(self, username):
        while True:
            print(menu["ADMIN_MENU"])
            choice = input()
            if choice == constants["ONE"]:
                user_role = constants["MANAGER"]
                self.user_helper.signup(user_role)
            elif choice == constants["TWO"]:
                self.user_helper.remove_manager()
            elif choice == constants["THREE"]:
                self.update_account_menu(username)
            elif choice == constants["FOUR"]:
                self.customer_menu(username)
            elif choice == constants["FIVE"]:
                break
            else:
                print(prompts["WRONG_INPUT"])


    def manager_menu(self, username):
        while True:
            print(menu["MANAGER_MENU"])
            choice = input()
            if choice == constants["ONE"]:
                self.event_helper.add_event(username)
            elif choice == constants["TWO"]:
                self.event_helper.remove_event(username)
            elif choice == constants["THREE"]:
                self.event_helper.list_events(username)
            elif choice == constants["FOUR"]:
                self.update_event_menu(username)
            elif choice == constants["FIVE"]:
                self.update_account_menu(username)
            elif choice == constants["SIX"]:
                break
            else:
                print(prompts["WRONG_INPUT"])
                

    def update_event_menu(self, username):
        print(menu["UPDATE_EVENT"])
        while True:
            ch = input()
            if ch in constants.values():
                self.event_helper.update_event(username, ch)
                return
            else:
                print(prompts["WRONG_INPUT"])
                print(menu["UPDATE_EVENT"])
                
                
    def update_account_menu(self, username):
        print(menu["UPDATE_ACCOUNT"])
        while True:
            ch = input()
            if ch in constants.values():
                self.user_helper.update_account(username, ch)
                return
            else:
                print(prompts["WRONG_INPUT"])
                print(menu["UPDATE_ACCOUNT"])
              
              
    def customer_menu(self, username):
        while True:
            print(menu["CUSTOMER_MENU"])
            choice = input()
            if choice == constants["ONE"]:
                self.event_helper.list_all_events()
            elif choice == constants["TWO"]:
                self.event_helper.view_event()
            elif choice == constants["THREE"]:
                self.event_helper.book_event(username)
            elif choice == constants["FOUR"]:
                self.event_helper.filter_event()
            elif choice == constants["FIVE"]:
                self.event_helper.search_event()
            elif choice == constants["SIX"]:
                self.event_helper.view_booked_event(username)
            elif choice == constants["SEVEN"]:
                self.update_account_menu(username)
            elif choice == constants["EIGHT"]:
                break
            else:
                print(prompts["WRONG_INPUT"])