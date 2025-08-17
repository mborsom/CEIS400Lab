class Inventory:
    def __init__(self):
        self.inventory_id = ""
        self.tool_id = ""
        self.quantity = 0
        self.available = 0
        self.reserved = 0
        self.inventory_items = {}  # Dictionary to track all tools
    
    def add_tool_to_inventory(self, tool_id, quantity):
        if tool_id in self.inventory_items:
            self.inventory_items[tool_id]['quantity'] += quantity
            self.inventory_items[tool_id]['available'] += quantity
        else:
            self.inventory_items[tool_id] = {
                'quantity': quantity,
                'available': quantity,
                'reserved': 0
            }
        print(f"Added {quantity} of tool {tool_id} to inventory")
    
    def update_quantity(self, tool_id, change):
        if tool_id in self.inventory_items:
            if change < 0:  # Tool checked out
                if self.inventory_items[tool_id]['available'] >= abs(change):
                    self.inventory_items[tool_id]['available'] += change
                    self.inventory_items[tool_id]['reserved'] -= change
                    print(f"Inventory updated: {tool_id} available count changed by {change}")
                    return True
                else:
                    print(f"Error: Not enough {tool_id} available")
                    return False
            else:  # Tool returned
                self.inventory_items[tool_id]['available'] += change
                self.inventory_items[tool_id]['reserved'] -= change
                print(f"Inventory updated: {tool_id} returned to available")
                return True
        else:
            print(f"Error: Tool {tool_id} not found in inventory")
            return False
        
    def check_stock(self, tool_id):
        if tool_id in self.inventory_items:
            item = self.inventory_items[tool_id]
            print(f"Tool {tool_id}: Total={item['quantity']}, Available={item['available']}, Reserved={item['reserved']}")
            return item['available']
        else:
            print(f"Tool {tool_id} not found in inventory")
            return 0
        
    def reserve_tool(self, tool_id):
        if tool_id in self.inventory_items:
            if self.inventory_items[tool_id]['available'] > 0:
                self.inventory_items[tool_id]['available'] -= 1
                self.inventory_items[tool_id]['reserved'] += 1
                print(f"Tool {tool_id} reserved successfully")
                return True
            else:
                print(f"Tool {tool_id} not available for reservation")
                return False
        else:
            print(f"Tool {tool_id} not found in inventory")
            return False
    
    def get_inventory_summary(self):
        print("\n=== Inventory Summary ===")
        if not self.inventory_items:
            print("No items in inventory")
            return
            
        for tool_id, item in self.inventory_items.items():
            print(f"{tool_id}: Total={item['quantity']}, Available={item['available']}, Out={item['reserved']}")