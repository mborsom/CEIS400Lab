import sqlite3
from datetime import datetime

def create_database():
    # Create/connect to SQLite database
    conn = sqlite3.connect('equipment_checkout.db')
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            skill_level TEXT,
            department TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_date TEXT
        )
    ''')
    
    # Create tools table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tools (
            tool_id TEXT PRIMARY KEY,
            barcode TEXT UNIQUE NOT NULL,
            tool_name TEXT NOT NULL,
            category TEXT,
            status TEXT DEFAULT 'available',
            condition_status TEXT DEFAULT 'good',
            checked_out_to TEXT,
            created_date TEXT
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            employee_id TEXT NOT NULL,
            tool_id TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            checkout_date TEXT,
            return_date TEXT,
            condition_on_return TEXT,
            notes TEXT
        )
    ''')
    
    # Insert sample employees (for login testing)
    employees_data = [
        ('EMP001', 'employee1', 'password123', 'John Smith', 'Level 2', 'Maintenance', 1, datetime.now().isoformat()),
        ('EMP002', 'employee2', 'password456', 'Jane Doe', 'Level 3', 'Maintenance', 1, datetime.now().isoformat()),
        ('MGR001', 'manager1', 'manager123', 'Bob Johnson', 'Manager', 'Management', 1, datetime.now().isoformat())
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO employees 
        (employee_id, username, password, name, skill_level, department, is_active, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)
    
    # Insert sample tools
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
    
    conn.commit()
    conn.close()
    print("Database created and sample data inserted!")

if __name__ == "__main__":
    create_database()