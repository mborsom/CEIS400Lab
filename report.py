from datetime import datetime  # Need this for timestamps on reports

class Report:
    def __init__(self):
        # Basic report properties
        self.report_id = ""         # Unique ID for each report
        self.report_type = ""       # What kind of report (checkout, tools, etc.)
        self.date_generated = ""    # When was this report created
        self.report_data = []       # Could store report data here if needed later
    
    def generate_checkout_report(self, transactions):
        # Generate report showing all checkout transactions
        # Takes list of transactions as input
        self.report_id = f"RPT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.report_type = "Checkout Report"
        self.date_generated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n=== {self.report_type} ===")
        print(f"Generated: {self.date_generated}")
        print(f"Report ID: {self.report_id}")
        print("-" * 50)  # Nice separator line shout out Prof. Rick Bird! 
        
        if not transactions:
            print("No transactions found")
            return
            
        # Count different types of transactions
        checkout_count = 0
        return_count = 0
        
        for transaction in transactions:
            if transaction.type == "checkout":
                checkout_count += 1
                # Show status - has it been returned yet?
                status = "RETURNED" if transaction.return_date else "CHECKED OUT"
                print(f"Employee: {transaction.employee_id} | Tool: {transaction.tool_id} | Date: {transaction.checkout_date} | Status: {status}")
            elif transaction.type == "return":
                return_count += 1
                
        # Summary totals at bottom
        print("-" * 50)
        print(f"Total Checkouts: {checkout_count}")
        print(f"Total Returns: {return_count}")
        print(f"Currently Out: {checkout_count - return_count}")  # Still outstanding
        
    def generate_tool_status_report(self, tools):
        # Report showing current status of all tools
        # Useful for management to see what's available
        self.report_id = f"RPT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.report_type = "Tool Status Report"
        self.date_generated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n=== {self.report_type} ===")
        print(f"Generated: {self.date_generated}")
        print(f"Report ID: {self.report_id}")
        print("-" * 60)
        
        if not tools:
            print("No tools found")
            return
            
        # Count tools by status
        available_count = 0
        checked_out_count = 0
        maintenance_count = 0
        
        for tool in tools:
            # Show who has it if it's checked out
            checked_out_to = f" (to {tool.checked_out_to})" if tool.checked_out_to else ""
            print(f"ID: {tool.tool_id} | Name: {tool.tool_name} | Status: {tool.status.upper()} | Condition: {tool.condition}{checked_out_to}")
            
            # Count by status for summary
            if tool.status == "available":
                available_count += 1
            elif tool.status == "checked_out":
                checked_out_count += 1
            elif tool.status == "maintenance":
                maintenance_count += 1
                
        # Summary totals
        print("-" * 60)
        print(f"Available: {available_count} | Checked Out: {checked_out_count} | Maintenance: {maintenance_count}")
        
    def generate_employee_usage_report(self, transactions, employee_id):
        # Report for specific employee showing their tool usage
        # Good for tracking who uses what tools
        self.report_id = f"RPT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.report_type = f"Employee Usage Report - {employee_id}"
        self.date_generated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n=== {self.report_type} ===")
        print(f"Generated: {self.date_generated}")
        print(f"Report ID: {self.report_id}")
        print("-" * 50)
        
        # Filter transactions for just this employee
        employee_transactions = [t for t in transactions if t.employee_id == employee_id]
        
        if not employee_transactions:
            print(f"No transactions found for employee {employee_id}")
            return
            
        # Show each transaction for this employee
        for transaction in employee_transactions:
            status = "RETURNED" if transaction.return_date else "STILL OUT"
            print(f"Tool: {transaction.tool_id} | Checkout: {transaction.checkout_date} | Status: {status}")
            if transaction.notes:
                print(f"  Notes: {transaction.notes}")  # Indent notes
                
        print("-" * 50)
        print(f"Total transactions: {len(employee_transactions)}")
        
    def export_data(self, filename=""):
        # Export report data to file
        # TODO: Actually implement file writing later if we have time
        if not filename:
            filename = f"report_{self.report_id}.txt"
            
        print(f"Report would be exported to: {filename}")
        print("(File export not implemented in this basic version)")