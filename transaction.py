from datetime import datetime  # Need this for timestamps

class Transaction:
    def __init__(self):
        # Transaction tracking fields
        self.transaction_id = ""    # Unique ID for this transaction
        self.employee_id = ""       # Who did the transaction
        self.tool_id = ""          # What tool was involved
        self.checkout_date = ""     # When it was checked out
        self.return_date = ""       # When it was returned (empty if still out)
        self.type = ""             # "checkout" or "return"
        self.notes = ""            # Any comments about condition, etc.
    
    def create_checkout(self, employee_id, tool_id):
        # Create a new checkout transaction
        # Generate unique ID using current timestamp
        self.transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.employee_id = employee_id
        self.tool_id = tool_id
        # Store exact time of checkout - this is important for tracking
        self.checkout_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.type = "checkout"
        
        # Print confirmation so we know it worked
        print(f"Checkout transaction created: {self.transaction_id}")
        print(f"Employee {employee_id} checked out tool {tool_id}")
        return self.transaction_id
        
    def process_return(self, condition="good", notes=""):
        # Update transaction when tool is returned
        # TODO: Maybe save this back to database later
        self.return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.type = "return"  # Change type to show it's been returned
        self.notes = notes    # Save any notes about condition
        
        print(f"Return processed for transaction {self.transaction_id}")
        print(f"Tool returned in {condition} condition")
        if notes:
            print(f"Notes: {notes}")  # Show notes if there are any
        
    def get_history(self):
        # Return formatted string with transaction details
        # Useful for reports and debugging
        history = f"Transaction ID: {self.transaction_id}\n"
        history += f"Employee: {self.employee_id}\n"
        history += f"Tool: {self.tool_id}\n"
        history += f"Checkout: {self.checkout_date}\n"
        if self.return_date:
            history += f"Return: {self.return_date}\n"
        return history