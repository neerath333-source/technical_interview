from app import create_app
import os

# Check if we should run in testing mode
is_testing = os.environ.get('FLASK_TESTING') == 'True'
app = create_app(testing=is_testing)

if __name__ == '__main__':
    # Print current DB for verification
    db_uri = app.config.get('MONGO_URI')
    db_name = db_uri.split('/')[-1] if db_uri else 'Unknown'
    print(f"\n[STARTUP] Using Database: {db_name}")
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run server
    app.run(host='0.0.0.0', port=port, debug=True)
