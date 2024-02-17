from gentopia import PromptTemplate

PromptOfIntercomLogsAnalyzer = PromptTemplate(
    input_variables=["instruction"],
    template=
    """
    Json data: {instruction}
    Given the data provided, extract and analyze the intercom-related information in a structured YAML format suitable for further processing by another model. Focus on the following key aspects, not provide data if no input is available:
    The data contains logs of intercom calls. each call has a list of events. Each event has a timestamp and a type.
    based on message,event_type and timestamp analyze the logs and provide the following information:
    any notification was not sent due to error with the error message and timestamp.
    time difference between room created and start call notification sent with room_id and timestamp.
    """
)