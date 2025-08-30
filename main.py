# Import our main system class
from checkout_system import CheckoutSystem

def main():
    # Simple info display when someone runs this file directly
    # This isn't the web interface - just shows how to use it
    print("=== Equipment Checkout System ===")
    print("Backend classes loaded successfully")
    print()
    print("To use the web interface:")
    print("1. Run: python web_server.py")      # This starts the web server
    print("2. Open browser to: http://localhost:5000")  # This is where to go
    print()
    print("Test login credentials:")
    # Show the test accounts from our database
    print("- employee1 / password123")
    print("- employee2 / password456")
    print("- manager1 / manager123")

# Only run main() if this file is run directly (not imported)
if __name__ == "__main__":
    main()