def get_model_config_from_provider_model(provider_model):
    from config import API_SETTINGS
    if not isinstance(provider_model, str) or '/' not in provider_model:
        raise ValueError('模型名称格式错误，应为 provider/model，例如 gpt/gpt-4o-mini')

    provider, model = provider_model.split('/', 1)
    if not provider or not model:
        raise ValueError('模型名称格式错误，应为 provider/model，例如 gpt/gpt-4o-mini')
    if provider not in API_SETTINGS:
        raise ValueError(f'未知模型供应商: {provider}')

    provider_config = API_SETTINGS[provider]
    available_models = provider_config.get('available_models', [])
    if available_models and model not in available_models:
        raise ValueError(f'{provider} 未配置可用模型: {model}')
    
    if provider == 'doubao':
        # Get the index of the model in available_models to find corresponding endpoint_id
        model_index = provider_config['available_models'].index(model)
        endpoint_id = provider_config['endpoint_ids'][model_index] if model_index < len(provider_config['endpoint_ids']) else ''
        model_config = {**provider_config, 'model': model, 'endpoint_id': endpoint_id}
    else:
        model_config = {**provider_config, 'model': model}
    
    # Remove lists from config before creating ModelConfig
    if 'available_models' in model_config:
        del model_config['available_models']
    if 'endpoint_ids' in model_config:
        del model_config['endpoint_ids']

    from llm_api import ModelConfig
    return ModelConfig(**model_config)
