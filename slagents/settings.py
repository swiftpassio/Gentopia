import os


def get(name, default=None):
    """
    Get the value of a variable in the settings module scope.
    """
    return globals().get(name, default)


HOST_NAME = os.getenv("HOST_NAME", "https://swiftlane-dev.appspot.com")

SERVICE_ACCOUNTS_FOR_CLOUD_TASK_HANDLER = os.getenv(
    "SERVICE_ACCOUNTS_FOR_CLOUD_TASK_HANDLER",
    "swiftpass-demo@swiftpass.iam.gserviceaccount.com",
)
# firebase
INIT_FIREBASE = os.getenv("INIT_FIREBASE", True)
FIRESTORE_ENV = os.getenv("FIRESTORE_ENV", "dev")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "swiftlane-dev")
GOOGLE_PROJECT_LOCATION = os.getenv("GOOGLE_PROJECT_LOCATION", "us-east1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
ADMIN_REFRESH_TOKEN = os.getenv("ADMIN_REFRESH", "sk-dsd")
BASE_URL = os.getenv("BASE_URL", "https://api.openai.com")
ZENDESK_API_TOKEN = os.getenv("ZEDESK_API_TOKEN",
                              "")
API_TOKEN = os.getenv("API_TOKEN", "")
