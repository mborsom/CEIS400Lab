Equipment Checkout System - Week 6
==================================

SETUP INSTRUCTIONS:
1. Make sure Python is installed
2. Install Flask: pip install flask
3. Run: python database_setup.py
4. Run: python web_server.py  
5. Open browser to: http://localhost:5000

TEST LOGIN CREDENTIALS:
- employee1 / password123 (John Smith - Level 2)
- employee2 / password456 (Jane Doe - Level 3)
- manager1 / manager123 (Bob Johnson - Manager)

FEATURES:
- Employee login with database authentication
- Tool checkout and return with condition tracking
- Report generation (tool status, checkout history)
- 3-tier architecture (Web frontend, Python backend, SQLite database)

FILES INCLUDED:
- web_server.py - Flask web server (main application)
- checkout_system.py - Main business logic
- employee.py - Employee class
- tool.py - Tool class
- transaction.py - Transaction tracking
- inventory.py - Inventory management (legacy)
- report.py - Report generation
- main.py - Backend testing
- database_setup.py - Creates SQLite database
- equipment_checkout.db - SQLite database file

SYSTEM ARCHITECTURE:
Tier 1: HTML web pages (frontend)
Tier 2: Python Flask server (backend/business logic)  
Tier 3: SQLite database (data storage)