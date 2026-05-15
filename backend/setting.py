from flask import Blueprint, jsonify, request

setting_bp = Blueprint('setting', __name__)

@setting_bp.route('/setting', methods=['GET'])
def get_settings():
    """Get current settings and models"""
    from config import API_SETTINGS, DEFAULT_MAIN_MODEL, DEFAULT_SUB_MODEL, MAX_THREAD_NUM, MAX_NOVEL_SUMMARY_LENGTH
    
    # Get models grouped by provider
    models = {provider: config['available_models'] for provider, config in API_SETTINGS.items() if 'available_models' in config}
    
    # Combine all settings
    settings = {
        'models': models,
        'MAIN_MODEL': DEFAULT_MAIN_MODEL,
        'SUB_MODEL': DEFAULT_SUB_MODEL,
        'MAX_THREAD_NUM': MAX_THREAD_NUM,
        'MAX_NOVEL_SUMMARY_LENGTH': MAX_NOVEL_SUMMARY_LENGTH,
    }
    return jsonify(settings)

@setting_bp.route('/test_model', methods=['POST'])
def test_model():
    """Test if a model configuration works"""
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({
                'success': False,
                'error': '请求体必须是 JSON 对象'
            }), 400

        provider_model = data.get('provider_model')
        
        try:
            from backend_utils import get_model_config_from_provider_model
        except ImportError:
            from backend.backend_utils import get_model_config_from_provider_model
        model_config = get_model_config_from_provider_model(provider_model)
        
        from llm_api import test_stream_chat
        response = None
        for msg in test_stream_chat(model_config):
            response = msg
            
        return jsonify({
            'success': True,
            'response': response
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
