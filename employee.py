class Employee:
    def __init__(self):
        self.employee_id = ""
        self.username = ""
        self.password = ""
        self.name = ""
        self.skill_level = ""
        self.department = ""
        self.is_logged_in = False
    
    def login(self, username, password):
        # This method is now handled by the database in checkout_system.py
        # Keeping for compatibility but not used in web interface
        print("Login method - use web interface for actual authentication")
        return False
    
    def logout(self):  
        self.is_logged_in = False
        print("User logged out")
        
    def get_profile(self):  
        return f"Employee: {self.name}, ID: {self.employee_id}"