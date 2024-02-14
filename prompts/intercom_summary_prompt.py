from gentopia import PromptTemplate

PromptOfIntercomSummary = PromptTemplate(
    input_variables=[],
    template=
    """Given the JSON data provided, extract and summarize the intercom-related information in a structured YAML format suitable for further processing by another model. Focus on the following key aspects, not provide data if no input is available:
    Intercom directory creation status (is_intercom_directory_created).
    User's role at the front desk (is_user_front_desk).
    Intercom settings, including:
    App usage (use_app) if true user uses video calling, if false user uses regular phone,
    Phone usage (use_phone).
    Details of all intercom tokens, including:
    Device type,
    Last updated time,
    Token type
    
    Intercom history, including:
    No of missed calls,
    If any call picked by another user and number of times it happened.
    
    read debugging logs of missed calls:
    any notification was not sent due to error .
    time difference between room created and start call notification sent.
    check if call was terminated(ap_call_terminted) before sending sent call notification based on timestamp difference.
      """
)