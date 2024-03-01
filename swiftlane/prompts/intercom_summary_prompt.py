from gentopia import PromptTemplate

PromptOfIntercomSummary = PromptTemplate(
    input_variables=["instruction"],
    template=
    """
    JSON data: {instruction}
    Given the JSON data provided, extract and summarize the intercom-related information in a structured YAML format suitable for further processing by another model. Focus on the following key aspects, not provide data if no input is available:
    Intercom directory creation status (is_intercom_directory_created).
    User's role at the front desk (is_user_front_desk).
    ##Intercom settings##, including:
    App usage (use_app) if true user uses video calling, if false user uses regular phone,
    Phone usage (use_phone).
    
    ##Details of all intercom tokens##, including:
    Device type,
    Last updated time,
    Token type
    
    ##User's phone settings##, including:
    is_dnd_enabled
    is_battery_optimization_ignored
    is_silent_mode_enabled
    is_notification_enabled
    read_phone_state_permission_granted
    idle_mode_enabled
    power_save_mode_enabled
    context_device_model
    context_app_version
    network_reachable
    
    ##Intercom history##, including:
    No of missed calls,
    If any call picked by another user and number of times it happened.
      """
)