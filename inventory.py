class Inventory:
    def __init__(self):
        # Basic inventory tracking fields
        self.inventory_id = ""    # Unique ID for inventory record
        self.tool_id = ""         # Which tool this tracks
        self.quantity = 0         # Total number we have
        self.available = 0        # How many are available now
        self.reserved = 0         # How many are checked out
        # Dictionary to track all our tools - key is tool_id, value is quantities
        self.inventory_items = {}  # This is like a mini database in memory
    
    def add_tool_to_inventory(self, tool_id, quantity):
        # Add tools to our inventory tracking
        # If tool already exists, add to the count
        if tool_id in self.inventory_items:
            self.inventory_items[tool_id]['quantity'] += quantity
            self.inventory_items[tool_id]['available'] += quantity
        else:
            # New tool - create new entry
            # Remember: available starts same as quantity
            self.inventory_items[tool_id] = {
                'quantity': quantity,    # Total we own
                'available': quantity,   # Available to checkout
                'reserved': 0           # Currently checked out
            }
        print(f"Added {quantity} of tool {tool_id} to inventory")
    
    def update_quantity(self, tool_id, change):
        # Update inventory when tools are checked out or returned
        # change is negative for checkout, positive for return
        if tool_id in self.inventory_items:
            if change < 0:  # Tool being checked out
                if self.inventory_items[tool_id]['available'] >= abs(change):
                    # We have enough available
                    self.inventory_items[tool_id]['available'] += change  # Subtract from available
                    self.inventory_items[tool_id]['reserved'] -= change   # Add to reserved
                    print(f"Inventory updated: {tool_id} available count changed by {change}")
                    return True
                else:
                    print(f"Error: Not enough {tool_id} available")
                    return False
            else:  # Tool being returned
                self.inventory_items[tool_id]['available'] += change      # Add back to available
                self.inventory_items[tool_id]['reserved'] -= change       # Remove from reserved
                print(f"Inventory updated: {tool_id} returned to available")
                return True
        else:
            print(f"Error: Tool {tool_id} not found in inventory")
            return False
        
    def check_stock(self, tool_id):
        # See how many of a tool we have available
        # Useful before allowing checkouts
        if tool_id in self.inventory_items:
            item = self.inventory_items[tool_id]
            print(f"Tool {tool_id}: Total={item['quantity']}, Available={item['available']}, Reserved={item['reserved']}")
            return item['available']
        else:
            print(f"Tool {tool_id} not found in inventory")
            return 0
        
    def reserve_tool(self, tool_id):
        # Reserve a tool for checkout (move from available to reserved)
        # TODO: This might be useful for advanced features later
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
        # Print out current status of all inventory
        # Good for debugging and reports
        print("\n=== Inventory Summary ===")
        if not self.inventory_items:
            print("No items in inventory")
            return
            
        for tool_id, item in self.inventory_items.items():
            print(f"{tool_id}: Total={item['quantity']}, Available={item['available']}, Out={item['reserved']}")