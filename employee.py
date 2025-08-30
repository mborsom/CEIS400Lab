class Employee:
    def __init__(self):
        # Basic employee info - remember these match the database fields
        self.employee_id = ""
        self.username = ""
        self.password = ""  # Note: in real system this would be encrypted
        self.name = ""
        self.skill_level = ""
        self.department = ""
        self.is_logged_in = False  # Track if user is currently logged in
    
    def login(self, username, password):
        # This method isn't used anymore since we moved login to database
        # Keeping it here just in case we need it for testing
        # Maybe remove this later when everything is working
        print("Login method - use web interface for actual authentication")
        return False
        
    def logout(self):
        # Simple logout - just set flag to false
        self.is_logged_in = False
        print("User logged out")
        
    def get_profile(self):
        # Return basic info about the employee
        # Could add more fields later if needed
        return f"Employee: {self.name}, ID: {self.employee_id}"