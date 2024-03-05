from gentopia import PromptTemplate

PromptOfIntercomLogsAnalyzer = PromptTemplate(
    input_variables=["instruction"],
    template=
    """
    Json data: {instruction}
    Given the data provided, extract and analyze the intercom-related information in a structured YAML format suitable for further processing by another model. Focus on the following key aspects, not provide data if no input is available:
    The data contains logs from server side sending notification and from mobile side receiving notification for intercom calls. 
    Server Logs: The logs contain information about the notification sent to the mobile app. Each notification has a timestamp and a status (sent or error).
    each call has a list of events. Each event has a timestamp and a type.
    based on message,event_type and timestamp analyze the logs and provide the following information:
    any notification was not sent due to error with the error message and timestamp , specify error in output.
    time difference between room created and start call notification sent with room_id and timestamp.
    
    Mobile Logs: The logs contain information about the notification received by the mobile app. Each notification has a timestamp and a status (received or error).
    if no mobile logs are available, then provide the output as "No mobile logs available".
    check if notification was received by app
    check if there is delay in receiving notification
    check if there is any error state and output the error message and timestamp.
    """
)