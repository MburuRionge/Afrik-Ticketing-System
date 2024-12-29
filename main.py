# Import the create_app function from the website module
from app import create_app


# Call the create_app function to get the Flask application instance
# This function typically sets up the app with necessary configurations,
# registers blueprints, and initializes extensions like databases
app = create_app()

# The following block of code ensures that the Flask application runs only if
# this script is executed directly, and not when it is imported as a module
if __name__ == '__main__':
    # Start the Flask development server
    # Setting debug=True enables the debugger, allows for automatic reloading
    # of the server upon code changes, and provides detailed error messages
    app.run(debug=True)