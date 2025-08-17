class Tool:
    def __init__(self, tool_id="", tool_name="", barcode=""):
        self.tool_id = tool_id
        self.barcode = barcode
        self.tool_name = tool_name
        self.category = ""
        self.status = "available"  # available, checked_out, maintenance
        self.condition = "good"    # good, damaged, broken
        self.checked_out_to = ""
    
    def scan_barcode(self, scanned_code):
        if scanned_code == self.barcode:
            print(f"Barcode scan successful for {self.tool_name}")
            return True
        else:
            print("Barcode scan failed")
            return False
        
    def check_availability(self):
        if self.status == "available":
            print(f"{self.tool_name} is available for checkout")
            return True
        else:
            print(f"{self.tool_name} is not available - status: {self.status}")
            return False
        
    def update_status(self, new_status, employee_id=""):
        self.status = new_status
        if new_status == "checked_out":
            self.checked_out_to = employee_id
            print(f"{self.tool_name} checked out to employee {employee_id}")
        elif new_status == "available":
            self.checked_out_to = ""
            print(f"{self.tool_name} returned and available")