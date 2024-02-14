from gentopia.tools import *


class GetUserData(BaseTool):
    name = "get_user_data"
    description = "A tool to get user data"

    def _run(self, user_id: str) -> Any:
        return {
            "data": {
                "activation_date": "2024-01-16T05:05:21.242683",
                "can_edit": True,
                "created_at": "2020-10-28 11:22:23.114301",
                "deactivation_date": None,
                "email": "nagesh@swiftlane.com",
                "enable_custom_pin": True,
                "first_name": "Nagesh",
                "id": 236154022679109146,
                "id_str": "236154022679109146",
                "intercom_settings": {
                    "enable_dnd": False,
                    "use_app": True,
                    "use_phone": False
                },
                "intercom_tokens": [
                    {
                        "device_type": "web",
                        "last_updated": "Wed, 14 Feb 2024 09:44:17 GMT",
                        "token_type": "background"
                    },
                    {
                        "device_type": "android",
                        "last_updated": "Wed, 14 Feb 2024 05:51:47 GMT",
                        "token_type": "background"
                    },
                    {
                        "device_type": "ios",
                        "last_updated": "Wed, 14 Feb 2024 01:59:11 GMT",
                        "token_type": "background"
                    },
                    {
                        "device_type": "ios",
                        "last_updated": "Wed, 14 Feb 2024 01:59:10 GMT",
                        "token_type": "voip"
                    }
                ],
                "is_face_scanned": True,
                "is_intercom_directory_created": True,
                "is_mobile_credentials_assigned": True,
                "is_pin_assigned": True,
                "is_user_front_desk": True,
                "last_name": "Bhad",
                "max_digits_in_custom_pin": 6,
                "min_digits_in_custom_pin": 4,
                "phone_number": {
                    "country_code": "91",
                    "phone_number": "5132123132"
                },
                "pin": 2232,
                "role": "admin",
                "source": "BRIVO",
                "status": "active",
                "updated_at": "2024-01-16 05:05:21.252610",
                "user_photo_path": None,
                "workspace_display_name": "Swiftlane Inc",
                "workspace_id_str": "82488426438216692",
                "workspace_name": "swiftlane"
            },
            "metadata": {
                "status_code": 200
            }
        }

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class GetIntercomHistoryForUser(BaseTool):
    name = "get_intercom_history_for_user"
    description = "A tool to get intercom history for user"

    def _run(self, user_id: str) -> Any:
        return {
    "data": {
        "call_history": [
            {
                "access_point_id": 404704787626995836,
                "access_point_id_str": "404704787626995836",
                "access_point_name": "Entry Door - Swiftreader",
                "call_answered_by": "Nagesh Bhad",
                "call_direction": "Incoming",
                "call_url": "https://video.twilio.com/v1/Rooms/RM5acc1b8334a8ee112530a5679b2eed26",
                "company_id": 82488426438216692,
                "company_id_str": "82488426438216692",
                "created_at": "Sat, 27 Jan 2024 09:38:16 GMT",
                "description": "Intercom call for tenant:Nagesh Bhad requesting access. Recipients:Nagesh Bhad",
                "duration": 32,
                "id": 676234212097855288,
                "id_str": "676234212097855288",
                "recipients": [
                    [
                        236154022679109146
                    ]
                ],
                "room_id": "RM5acc1b8334a8ee112530a5679b2eed26",
                "room_name": "prod-82488426438216692-404704787626995836-41H2JD",
                "site_name": "Intercom Demo Site",
                "status": "completed",
                "target_user_id": 236154022679109146,
                "target_user_id_str": "236154022679109146",
                "updated_at": "Sat, 27 Jan 2024 09:39:01 GMT",
                "visitor_photo_path": "https://prod-sp-workspaces.s3.amazonaws.com/82488426438216692/visitors/404704787626995836/20240127/C1F47063-5DE0-4121-B53A-563310F93B15.jpg?AWSAccessKeyId=AKIAUOM3BAVU44FMLKH7&Signature=vJ808ulbkfQGLB5hfvjWgdDBuOI%3D&Expires=1708520299"
            },
            {
                "access_point_id": 404704787626995836,
                "access_point_id_str": "404704787626995836",
                "access_point_name": "Entry Door - Swiftreader",
                "call_direction": "Incoming",
                "call_url": "https://video.twilio.com/v1/Rooms/RM81404648ce34c8f0ac79c11e563bc30f",
                "company_id": 82488426438216692,
                "company_id_str": "82488426438216692",
                "created_at": "Sat, 27 Jan 2024 09:36:55 GMT",
                "description": "Intercom call for tenant:Nagesh Bhad requesting access. Recipients:Nagesh Bhad",
                "duration": 12,
                "id": 676233864529062658,
                "id_str": "676233864529062658",
                "recipients": [
                    [
                        236154022679109146
                    ]
                ],
                "room_id": "RM81404648ce34c8f0ac79c11e563bc30f",
                "room_name": "prod-82488426438216692-404704787626995836-NFCNDZ",
                "site_name": "Intercom Demo Site",
                "status": "missed",
                "target_user_id": None,
                "target_user_id_str": "None",
                "updated_at": "Sat, 27 Jan 2024 09:37:06 GMT",
                "visitor_photo_path": "https://prod-sp-workspaces.s3.amazonaws.com/82488426438216692/visitors/404704787626995836/20240127/1BD8922E-879D-4E09-A42F-F272E96FAA36.jpg?AWSAccessKeyId=AKIAUOM3BAVU44FMLKH7&Signature=qp%2Ftp2HLhz732JtnwPT5BK3%2Fock%3D&Expires=1708520299"
            },
            {
                "access_point_id": 186535597032570580,
                "access_point_id_str": "186535597032570580",
                "access_point_name": "Intercom Front Door",
                "call_answered_by": "Nagesh Bhad",
                "call_direction": "Incoming",
                "call_url": "https://video.twilio.com/v1/Rooms/RMcf829a123433aba311477f0278f5a6a8",
                "company_id": 82488426438216692,
                "company_id_str": "82488426438216692",
                "created_at": "Thu, 04 Jan 2024 13:16:39 GMT",
                "description": "Intercom call for tenant:Nagesh Bhad requesting access. Recipients:Nagesh Bhad",
                "duration": 19,
                "id": 667755526627098100,
                "id_str": "667755526627098100",
                "recipients": [
                    [
                        236154022679109146
                    ]
                ],
                "room_id": "RMcf829a123433aba311477f0278f5a6a8",
                "room_name": "prod-82488426438216692-186535597032570580-VPS72Y",
                "site_name": "Intercom Demo Site",
                "status": "completed",
                "target_user_id": 236154022679109146,
                "target_user_id_str": "236154022679109146",
                "updated_at": "Thu, 04 Jan 2024 13:16:57 GMT",
                "visitor_photo_path": "https://prod-sp-workspaces.s3.amazonaws.com/82488426438216692/visitors/186535597032570580/20240104/F91D2367-9028-4B52-8A2A-9BECA14D403A.jpg?AWSAccessKeyId=AKIAUOM3BAVU44FMLKH7&Signature=g%2BwszWBqnVJ%2BPB4j%2FMTU08qZl%2BE%3D&Expires=1708520299"
            },
            {
                "access_point_id": 186535597032570580,
                "access_point_id_str": "186535597032570580",
                "access_point_name": "Intercom Front Door",
                "call_direction": "Incoming",
                "call_url": "https://video.twilio.com/v1/Rooms/RM007b835932f3f98331dddfe127b8212e",
                "company_id": 82488426438216692,
                "company_id_str": "82488426438216692",
                "created_at": "Thu, 04 Jan 2024 13:16:11 GMT",
                "description": "Intercom call for tenant:Nagesh Bhad requesting access. Recipients:Nagesh Bhad",
                "duration": 10,
                "id": 667755407749735382,
                "id_str": "667755407749735382",
                "recipients": [
                    [
                        236154022679109146
                    ]
                ],
                "room_id": "RM007b835932f3f98331dddfe127b8212e",
                "room_name": "prod-82488426438216692-186535597032570580-8M0WVQ",
                "site_name": "Intercom Demo Site",
                "status": "missed",
                "target_user_id": None,
                "target_user_id_str": "None",
                "updated_at": "Thu, 04 Jan 2024 13:16:22 GMT",
                "visitor_photo_path": "https://prod-sp-workspaces.s3.amazonaws.com/82488426438216692/visitors/186535597032570580/20240104/DA9A185A-0105-4333-9C0F-EA67A42AB69B.jpg?AWSAccessKeyId=AKIAUOM3BAVU44FMLKH7&Signature=6%2FJxf68nZ8UPtqZWouDjhTIXAqQ%3D&Expires=1708520299"
            },
            {
                "access_point_id": 399084821026109328,
                "access_point_id_str": "399084821026109328",
                "access_point_name": "Entry Door - Swiftreader X",
                "call_answered_by": "Nagesh Bhad",
                "call_direction": "Incoming",
                "call_url": "https://video.twilio.com/v1/Rooms/RMb804d4e170f029e449a9ef02bbe73b89",
                "company_id": 82488426438216692,
                "company_id_str": "82488426438216692",
                "created_at": "Thu, 04 Jan 2024 11:10:35 GMT",
                "description": "Intercom call for tenant:Nagesh Bhad requesting access. Recipients:Nagesh Bhad,Atul Test",
                "duration": 19,
                "id": 667723043058810264,
                "id_str": "667723043058810264",
                "recipients": [
                    [
                        236154022679109146
                    ],
                    [
                        371989804513109314
                    ]
                ],
                "room_id": "RMb804d4e170f029e449a9ef02bbe73b89",
                "room_name": "prod-82488426438216692-399084821026109328-KE866N",
                "site_name": "Intercom Demo Site",
                "status": "completed",
                "target_user_id": 236154022679109146,
                "target_user_id_str": "236154022679109146",
                "updated_at": "Thu, 04 Jan 2024 11:10:54 GMT",
                "visitor_photo_path": "https://prod-sp-workspaces.s3.amazonaws.com/82488426438216692/visitors/399084821026109328/20240104/2024-01-04-16-40-33-675.jpg?AWSAccessKeyId=AKIAUOM3BAVU44FMLKH7&Signature=iTBdP%2FtMtV%2Fsc38bmsczd3JYvpQ%3D&Expires=1708520299"
            }
        ]
    },

}

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class ZendeskSearchArticle(BaseTool):
    name = "zendesk_search_article"
    description = "A tool to search knowledge base articles in Zendesk using the API"

    def _run(self, user_id: str) -> Any:
        return {
        }

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
