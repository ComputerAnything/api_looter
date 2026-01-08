import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Development mode: hot reload enabled
    # Use debug=True for auto-reload on file changes
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
