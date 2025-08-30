# Import Flask components we need for the web server
from flask import Flask, render_template, request, redirect, url_for
# Flask - main web framework for creating web applications
# render_template - for loading HTML files (not using this yet but might later)
# request - to get form data from POST requests (username, password, etc.)
# redirect - to send user to different pages after actions
# url_for - to generate URLs for our routes safely

# Import our custom classes that handle the business logic
from checkout_system import CheckoutSystem  # Main system that handles login, checkout, return
from report import Report                   # Handles generating different types of reports

# Create the Flask web application instance
app = Flask(__name__)  # This creates our web server

# Create system components that will stay alive while server runs
# These are like global objects that all pages can use
system = CheckoutSystem()  # Handles all the business logic - login, checkout, return
report = Report()          # Handles generating reports for management

# Home page - shows login form
@app.route('/')  # This means when someone goes to localhost:5000/ they get this page
def home():
    # Return HTML as a string - not the prettiest but it works for now
    # TODO: Maybe move to separate HTML files later if we have time
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

# Handle login form submission
@app.route('/login', methods=['POST'])  # Only accepts POST requests (form submissions)
def login():
    # Get username and password from the form that was submitted
    username = request.form['username']  # Extract username from form data
    password = request.form['password']  # Extract password from form data
    
    # Try to authenticate with our checkout system
    if system.authenticate_user(username, password):
        # Success! Redirect to main dashboard
        return redirect(url_for('dashboard'))  # url_for is safer than hardcoding "/dashboard"
    else:
        # Login failed - show error message and link back to login
        return '''
        <html>
        <body>
            <h2>Login Failed</h2>
            <p>Invalid username or password</p>
            <p><a href="/">Try Again</a></p>
        </body>
        </html>
        '''

# Main dashboard after successful login
@app.route('/dashboard')
def dashboard():
    # Security check - make sure user is actually logged in
    # Remember: always validate this on every protected page!
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))  # Send back to login if not authenticated
    
    # Show main menu with user's name - using f-string to insert variables
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

# Checkout page - show available tools in a dropdown
@app.route('/checkout')
def checkout():
    # Always check authentication first - this is important for security
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    # Get list of tools that are available for checkout
    # Using list comprehension to filter only available tools
    available_tools = [tool for tool in system.tools if tool.status == "available"]
    
    # Build HTML option tags for the dropdown - probably a better way to do this
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

# Process the actual checkout when form is submitted
@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    # Security check again - every protected route needs this
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    # Get the barcode from the form submission
    barcode = request.form['barcode']
    
    # Try to checkout the tool using our business logic
    if system.process_checkout(barcode):
        # Find the tool object (not really using this but might be useful later)
        tool = system.find_tool_by_barcode(barcode)

        # Success! Show confirmation message
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
        # Failed - tool might be unavailable or not found
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

# Return page - show tools that current user has checked out
@app.route('/return')
def return_tool():
    # Authentication check - getting tired of writing this but it's necessary
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    # Find tools that are checked out to the current user
    # Only show tools this employee actually has
    my_tools = [tool for tool in system.tools if tool.checked_out_to == system.current_user.employee_id]
    
    # If user has no tools checked out, show message
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
    
    # Build dropdown options for tools this user can return
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

# Process the actual return when form is submitted
@app.route('/process_return', methods=['POST'])
def process_return():
    # Yet another authentication check - maybe there's a better way to do this
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    # Get form data - barcode and condition
    barcode = request.form['barcode']
    condition = request.form['condition']
    
    # Try to process the return
    if system.process_return(barcode, condition):
        # Success message
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
        # Error - tool not found or not checked out to this user
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

# Reports menu page
@app.route('/reports')
def reports():
    # Authentication check (getting repetitive but necessary)
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    # Show available report types
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

# Generate specific reports based on type
@app.route('/generate_report/<report_type>')  # <report_type> is a variable from the URL
def generate_report(report_type):
    # Authentication check once more
    if not system.current_user or not system.current_user.is_logged_in:
        return redirect(url_for('home'))
    
    # Generate different reports based on what was requested
    if report_type == 'tools':
        # Tool status report - show all tools and their current status
        report_html = '''
        <html>
        <body>
            <h2>Tool Status Report</h2>
            <table border="1">
                <tr><th>Tool ID</th><th>Tool Name</th><th>Status</th><th>Condition</th></tr>
        '''
        # Loop through all tools and add table rows
        for tool in system.tools:
            report_html += f'<tr><td>{tool.tool_id}</td><td>{tool.tool_name}</td><td>{tool.status}</td><td>{tool.condition}</td></tr>'
        
        # Close the table and add navigation links
        report_html += '''
            </table>
            <p><a href="/reports">Generate Another Report</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
        return report_html
    
    elif report_type == 'checkout':
        # Checkout report - show all transactions
        report_html = '''
        <html>
        <body>
            <h2>Checkout Report</h2>
            <table border="1">
                <tr><th>Transaction ID</th><th>Employee</th><th>Tool</th><th>Date</th></tr>
        '''
        # Loop through all transactions and add table rows
        for transaction in system.transactions:
            report_html += f'<tr><td>{transaction.transaction_id}</td><td>{transaction.employee_id}</td><td>{transaction.tool_id}</td><td>{transaction.checkout_date}</td></tr>'
        
        # Close table and add navigation
        report_html += '''
            </table>
            <p><a href="/reports">Generate Another Report</a></p>
            <p><a href="/dashboard">Back to Dashboard</a></p>
        </body>
        </html>
        '''
        return report_html

# Logout functionality
@app.route('/logout')
def logout():
    # Clean up the current user session
    if system.current_user:
        system.current_user.logout()  # Call logout method on user
        system.current_user = None    # Clear the current user
    return redirect(url_for('home'))  # Send back to login page

# Start the web server when this file is run directly
if __name__ == '__main__':
    print("Starting Equipment Checkout System...")
    print("Open your browser to: http://localhost:5000")
    # debug=True means server restarts when we change code - helpful during development
    app.run(debug=True)