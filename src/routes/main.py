from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    """
    Serve the main application page
    
    Returns:
        Rendered HTML template
    """
    return render_template('index.html')


@main_bp.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    
    Returns:
        JSON response with service status
    """
    return {
        'status': 'healthy',
        'service': 'voice-assistant'
    }, 200
