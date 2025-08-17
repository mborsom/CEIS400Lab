from flask import Flask, render_template, request, redirect, url_for
from checkout_system import CheckoutSystem
from report import Report

app = Flask(__name__)

# Create system components
system = CheckoutSystem()
report = Report()

# Home page - shows login
@app.route('/')
def home():
    return '''
    <html>
    <head><title>Equipment Checkout System</title></head>
    <body>
        <h2>Equipment Checkout System</h2>
        <h3>Employee Login</h3>
        <form method="POST" action="/login">
            <p>Username: <input type="text" name="username" required></p>
            <p>Password: <input type="password" name="password" required></p>
            <p><input type="submit" value="Login"></p>
        </form>
        <h4>Test Accounts:</h4>
        <p><strong>employee1</strong> / password123 (John Smith - Level 2)</p>
        <p><strong>employee2</strong> / password456 (Jane Doe - Level 3)</p>
        <p><strong>manager1</strong> / manager123 (Bob Johnson - Manager)</p>
    </body>
    </html>
    '''

# Handle login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if system.authenticate_user(username, password):
        return redirect(url_for('dashboard'))
    else:
        return '''
        <html>
        <body>
            <h2>Login Failed</h2>
            <p>Invalid username or password</p>
            <p><a href="/">Try Again</a></p>
        </body>
        </html>
        '''

# Dashboard - main menu
@app.route('/dashboard')
def dashboard():
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    return f'''
    <html>
    <head><title>Dashboard</title></head>
    <body>
        <h2>Equipment Checkout System</h2>
        <p>Welcome, {system.current_user.name} ({system.current_user.employee_id})</p>
        
        <h3>Actions:</h3>
        <p><a href="/checkout">Checkout Tool</a></p>
        <p><a href="/return">Return Tool</a></p>
        <p><a href="/reports">Generate Reports</a></p>
        <p><a href="/logout">Logout</a></p>
    </body>
    </html>
    '''
# Checkout page - show available tools
@app.route('/checkout')
def checkout():
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    # Get available tools
    available_tools = [tool for tool in system.tools if tool.status == "available"]
    
    tool_options = ""
    for tool in available_tools:
        tool_options += f'<option value="{tool.barcode}">{tool.tool_name} (ID: {tool.tool_id})</option>'
    
    return f'''
    <html>
    <head><title>Checkout Tool</title></head>
    <body>
        <h2>Checkout Tool</h2>
        <p>Employee: {system.current_user.name}</p>
        
        <form method="POST" action="/process_checkout">
            <p>Select Tool to Checkout:</p>
            <select name="barcode" required>
                <option value="">-- Choose a Tool --</option>
                {tool_options}
            </select>
            <p><input type="submit" value="Checkout Tool"></p>
        </form>
        
        <p><a href="/dashboard">Back to Dashboard</a></p>
    </body>
    </html>
    '''

# Process the checkout
@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    barcode = request.form['barcode']
    
    if system.process_checkout(barcode):
        tool = system.find_tool_by_barcode(barcode)

        return f'''
        <html>
        <body>
            <h2>Checkout Successful!</h2>
            <p>Tool {barcode} has been checked out to {system.current_user.name}</p>
            <p><a href="/checkout">Checkout Another Tool</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
    else:
        return '''
        <html>
        <body>
            <h2>Checkout Failed</h2>
            <p>Tool not available or not found</p>
            <p><a href="/checkout">Try Again</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''

# Return page
@app.route('/return')
def return_tool():
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    my_tools = [tool for tool in system.tools if tool.checked_out_to == system.current_user.employee_id]
    
    if not my_tools:
        return f'''
        <html>
        <body>
            <h2>Return Tool</h2>
            <p>Employee: {system.current_user.name}</p>
            <p><strong>You have no tools checked out.</strong></p>
            <p><a href="/checkout">Checkout a Tool</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
    
    tool_options = ""
    for tool in my_tools:
        tool_options += f'<option value="{tool.barcode}">{tool.tool_name} (ID: {tool.tool_id})</option>'
    
    return f'''
    <html>
    <body>
        <h2>Return Tool</h2>
        <p>Employee: {system.current_user.name}</p>
        
        <form method="POST" action="/process_return">
            <p>Select Tool to Return:</p>
            <select name="barcode" required>
                <option value="">-- Choose a Tool --</option>
                {tool_options}
            </select>
            
            <p>Tool Condition:</p>
            <select name="condition" required>
                <option value="good">Good</option>
                <option value="damaged">Damaged</option>
                <option value="broken">Broken</option>
            </select>
            
            <p><input type="submit" value="Return Tool"></p>
        </form>
        
        <p><a href="/dashboard">Back to Dashboard</a></p>
    </body>
    </html>
    '''

# Process return
@app.route('/process_return', methods=['POST'])
def process_return():
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    barcode = request.form['barcode']
    condition = request.form['condition']
    
    if system.process_return(barcode, condition):
        return f'''
        <html>
        <body>
            <h2>Return Successful!</h2>
            <p>Tool {barcode} has been returned in {condition} condition</p>
            <p><a href="/return">Return Another Tool</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
    else:
        return '''
        <html>
        <body>
            <h2>Return Failed</h2>
            <p>Tool not found or not checked out to you</p>
            <p><a href="/return">Try Again</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''

# Reports page
@app.route('/reports')
def reports():
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    return f'''
    <html>
    <body>
        <h2>Generate Reports</h2>
        <p>Employee: {system.current_user.name}</p>
        
        <h3>Available Reports:</h3>
        <p><a href="/generate_report/tools">Tool Status Report</a></p>
        <p><a href="/generate_report/checkout">Checkout Report</a></p>
        
        <p><a href="/dashboard">Back to Dashboard</a></p>
    </body>
    </html>
    '''

# Generate reports
@app.route('/generate_report/<report_type>')
def generate_report(report_type):
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    if report_type == 'tools':
        report_html = '''
        <html>
        <body>
            <h2>Tool Status Report</h2>
            <table border="1">
                <tr><th>Tool ID</th><th>Tool Name</th><th>Status</th><th>Condition</th></tr>
        '''
        for tool in system.tools:
            report_html += f'<tr><td>{tool.tool_id}</td><td>{tool.tool_name}</td><td>{tool.status}</td><td>{tool.condition}</td></tr>'
        
        report_html += '''
            </table>
            <p><a href="/reports">Generate Another Report</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
        return report_html
    
    elif report_type == 'checkout':
        report_html = '''
        <html>
        <body>
            <h2>Checkout Report</h2>
            <table border="1">
                <tr><th>Transaction ID</th><th>Employee</th><th>Tool</th><th>Date</th></tr>
        '''
        for transaction in system.transactions:
            report_html += f'<tr><td>{transaction.transaction_id}</td><td>{transaction.employee_id}</td><td>{transaction.tool_id}</td><td>{transaction.checkout_date}</td></tr>'
        
        report_html += '''
            </table>
            <p><a href="/reports">Generate Another Report</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
        return report_html

# Logout
@app.route('/logout')
def logout():
    if system.current_user:
        system.current_user.logout()
        system.current_user = None
    return redirect(url_for('home'))


# Run the server
if __name__ == '__main__':
    print("Starting Equipment Checkout System...")
    print("Open your browser to: http://localhost:5000")
    app.run(debug=True)