import sqlite3
from employee import Employee
from tool import Tool
from transaction import Transaction

class CheckoutSystem:
    def __init__(self):
        self.system_id = "ECS_001"
        self.current_user = None
        self.tools = []
        self.transactions = []
        self.db_name = 'equipment_checkout.db'
        
        # Load tools from database
        self.load_tools_from_database()
    
    def load_tools_from_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('SELECT tool_id, tool_name, barcode, category, status, condition_status, checked_out_to FROM tools')
            tools_data = cursor.fetchall()
            conn.close()
            
            self.tools = []
            for tool_data in tools_data:
                tool = Tool(tool_data[0], tool_data[1], tool_data[2])
                tool.category = tool_data[3]
                tool.status = tool_data[4]
                tool.condition = tool_data[5]
                tool.checked_out_to = tool_data[6]
                self.tools.append(tool)
            
            print(f"Loaded {len(self.tools)} tools from database")
        except:
    # If database doesn't exist, create empty list
            print("Database not found - run database_setup.py first")
            self.tools = []
        
    def authenticate_user(self, username, password):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT employee_id, username, name, skill_level, department 
                FROM employees 
                WHERE username = ? AND password = ? AND is_active = 1
            ''', (username, password))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                employee = Employee()
                employee.employee_id = result[0]
                employee.username = result[1]
                employee.name = result[2]
                employee.skill_level = result[3]
                employee.department = result[4]
                employee.is_logged_in = True
                self.current_user = employee
                print(f"Login successful for {employee.name}")
                return True
            else:
                print("Login failed - invalid credentials")
                return False
        except:
            # If database fails, use simple login
            employee = Employee()
            if employee.login(username, password):
                self.current_user = employee
                return True
            return False
        
    def find_tool_by_barcode(self, barcode):
        for tool in self.tools:
            if tool.barcode == barcode:
                return tool
        return None
        
    def process_checkout(self, barcode):
        if not self.current_user or not self.current_user.is_logged_in:
            print("Error: User must be logged in to checkout tools")
            return False
            
        tool = self.find_tool_by_barcode(barcode)
        if not tool:
            print("Error: Tool not found")
            return False
            
        if not tool.check_availability():
            return False
            
        transaction = Transaction()
        transaction_id = transaction.create_checkout(self.current_user.employee_id, tool.tool_id)
        
        tool.update_status("checked_out", self.current_user.employee_id)
        self.transactions.append(transaction)
        
        print(f"Checkout successful! Transaction ID: {transaction_id}")
        return True
        
    def process_return(self, barcode, condition="good", notes=""):
        if not self.current_user or not self.current_user.is_logged_in:
            print("Error: User must be logged in to return tools")
            return False
            
        tool = self.find_tool_by_barcode(barcode)
        if not tool:
            print("Error: Tool not found")
            return False
            
        if tool.checked_out_to != self.current_user.employee_id:
            print("Error: Tool is not checked out to this user")
            return False
            
        checkout_transaction = None
        for transaction in self.transactions:
            if (transaction.tool_id == tool.tool_id and 
                transaction.employee_id == self.current_user.employee_id and 
                transaction.type == "checkout" and 
                not transaction.return_date):
                checkout_transaction = transaction
                break
                
        if not checkout_transaction:
            print("Error: No checkout transaction found")
            return False
            
        checkout_transaction.process_return(condition, notes)
        tool.condition = condition
        tool.update_status("available")
        
        print("Return successful!")
        return True
        
    def list_available_tools(self):
        print("\n=== Available Tools ===")
        for tool in self.tools:
            if tool.status == "available":
                print(f"ID: {tool.tool_id}, Name: {tool.tool_name}, Barcode: {tool.barcode}")