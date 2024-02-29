from flask_restful import Resource

from slagents import settings
from slagents.auth import RequiresServiceAccountAuth


class ZendeskSupportCloudTaskHandler(Resource):
    @RequiresServiceAccountAuth(
        service_accounts=settings.SERVICE_ACCOUNTS_FOR_CLOUD_TASK_HANDLER
    )
    def post(self, token=None):
       pass