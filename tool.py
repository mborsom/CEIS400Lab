class Tool:
    def __init__(self, tool_id="", tool_name="", barcode=""):
        # Basic tool properties
        self.tool_id = tool_id
        self.barcode = barcode  # Used for scanning
        self.tool_name = tool_name
        self.category = ""  # Like "Hand Tools" or "Power Tools"
        # Status can be: available, checked_out, maintenance
        self.status = "available"  # Default to available when created
        # Condition can be: good, damaged, broken
        self.condition = "good"    # Default to good condition
        self.checked_out_to = ""   # Employee ID who has it
    
    def scan_barcode(self, scanned_code):
        # Simulate barcode scanning
        # In real system this would connect to actual scanner
        if scanned_code == self.barcode:
            print(f"Barcode scan successful for {self.tool_name}")
            return True
        else:
            print("Barcode scan failed")
            return False
        
    def check_availability(self):
        # Make sure tool can be checked out
        # Remember: only available tools can be checked out
        if self.status == "available":
            print(f"{self.tool_name} is available for checkout")
            return True
        else:
            print(f"{self.tool_name} is not available - status: {self.status}")
            return False
        
    def update_status(self, new_status, employee_id=""):
        # Change tool status and track who has it
        # This is important for accountability
        self.status = new_status
        if new_status == "checked_out":
            self.checked_out_to = employee_id  # Remember who took it
            print(f"{self.tool_name} checked out to employee {employee_id}")
        elif new_status == "available":
            self.checked_out_to = ""  # Clear the assignment
            print(f"{self.tool_name} returned and available")