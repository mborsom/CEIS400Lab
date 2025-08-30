import sqlite3           # SQLite database library (comes with Python)
from datetime import datetime  # For creating timestamps

def create_database():
    # Create the SQLite database file and tables
    # This only needs to be run once to set everything up
    
    # Create or connect to database file
    conn = sqlite3.connect('equipment_checkout.db')  # Creates file if it doesn't exist
    cursor = conn.cursor()
    
    # Create employees table for login credentials
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,     -- Unique employee ID
            username TEXT UNIQUE NOT NULL,    -- Login username (must be unique)
            password TEXT NOT NULL,           -- Login password (should encrypt in real system)
            name TEXT NOT NULL,               -- Full employee name
            skill_level TEXT,                 -- Employee skill level
            department TEXT,                  -- Which department they work in
            is_active BOOLEAN DEFAULT 1,      -- Can they login? (1=yes, 0=no)
            created_date TEXT                 -- When was this record created
        )
    ''')
    
    # Create tools table for all our equipment
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tools (
            tool_id TEXT PRIMARY KEY,         -- Unique tool ID
            barcode TEXT UNIQUE NOT NULL,     -- Barcode for scanning
            tool_name TEXT NOT NULL,          -- Tool name (Hammer, Drill, etc.)
            category TEXT,                    -- Tool category (Hand Tools, Power Tools)
            status TEXT DEFAULT 'available', -- Current status (available, checked_out, maintenance)
            condition_status TEXT DEFAULT 'good', -- Condition (good, damaged, broken)
            checked_out_to TEXT,              -- Employee ID who has it (if checked out)
            created_date TEXT                 -- When was this tool added
        )
    ''')
    
    # Create transactions table to track checkouts and returns
    # Should probably save our in-memory transactions here too
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,  -- Unique transaction ID
            employee_id TEXT NOT NULL,        -- Who did the transaction
            tool_id TEXT NOT NULL,            -- What tool was involved
            transaction_type TEXT NOT NULL,   -- "checkout" or "return"
            checkout_date TEXT,               -- When was it checked out
            return_date TEXT,                 -- When was it returned (NULL if still out)
            condition_on_return TEXT,         -- Condition when returned
            notes TEXT                        -- Any notes about the transaction
        )
    ''')
    
    # Insert test employees for login testing
    # Remember: In real system passwords would be encrypted!
    employees_data = [
        ('EMP001', 'employee1', 'password123', 'John Smith', 'Level 2', 'Maintenance', 1, datetime.now().isoformat()),
        ('EMP002', 'employee2', 'password456', 'Jane Doe', 'Level 3', 'Maintenance', 1, datetime.now().isoformat()),
        ('MGR001', 'manager1', 'manager123', 'Bob Johnson', 'Manager', 'Management', 1, datetime.now().isoformat())
    ]
    
    # Insert or replace (so we can run this script multiple times safely)
    cursor.executemany('''
        INSERT OR REPLACE INTO employees 
        (employee_id, username, password, name, skill_level, department, is_active, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    # Insert sample tools for testing
    tools_data = [
        ('TOOL001', '123456789', 'Hammer', 'Hand Tools', 'available', 'good', None, datetime.now().isoformat()),
        ('TOOL002', '987654321', 'Power Drill', 'Power Tools', 'available', 'good', None, datetime.now().isoformat()),
        ('TOOL003', '456789123', 'Screwdriver Set', 'Hand Tools', 'available', 'good', None, datetime.now().isoformat()),
        ('TOOL004', '789123456', 'Socket Wrench', 'Hand Tools', 'available', 'good', None, datetime.now().isoformat())
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO tools 
        (tool_id, barcode, tool_name, category, status, condition_status, checked_out_to, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', tools_data)
    
    # Save changes and close database
    conn.commit()  # Important: save the changes!
    conn.close()
    print("Database created and sample data inserted!")
    print("You can now run: python web_server.py")

# Run the setup when this file is executed
if __name__ == "__main__":
    create_database()