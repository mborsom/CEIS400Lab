from datetime import datetime

class Transaction:
    def __init__(self):
        self.transaction_id = ""
        self.employee_id = ""
        self.tool_id = ""
        self.checkout_date = ""
        self.return_date = ""
        self.type = ""  # checkout or return
        self.notes = ""
    
    def create_checkout(self, employee_id, tool_id):
        # Generate simple transaction ID
        self.transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.employee_id = employee_id
        self.tool_id = tool_id
        self.checkout_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.type = "checkout"
        
        print(f"Checkout transaction created: {self.transaction_id}")
        print(f"Employee {employee_id} checked out tool {tool_id}")
        return self.transaction_id
        
    def process_return(self, condition="good", notes=""):
        self.return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.type = "return"
        self.notes = notes
        
        print(f"Return processed for transaction {self.transaction_id}")
        print(f"Tool returned in {condition} condition")
        if notes:
            print(f"Notes: {notes}")
        
    def get_history(self):
        history = f"Transaction ID: {self.transaction_id}\n"
        history += f"Employee: {self.employee_id}\n"
        history += f"Tool: {self.tool_id}\n"
        history += f"Checkout: {self.checkout_date}\n"
        if self.return_date:
            history += f"Return: {self.return_date}\n"
        return history