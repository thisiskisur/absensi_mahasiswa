from app import create_app
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_server():
    try:
        app = create_app()
        print("🚀 Starting Flask server...")
        print("📍 Server will run on: http://127.0.0.1:8000")
        print("🔧 Debug mode: ON")
        print("📝 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app.run(
            host='127.0.0.1',  # Use localhost only
            port=3001,
            debug=True,
            use_reloader=False  # Disable reloader to avoid issues
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        logger.exception("Server startup failed")

if __name__ == '__main__':
    run_server()
