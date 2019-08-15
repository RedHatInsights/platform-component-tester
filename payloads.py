import uuid
import json

system_profile = {"number_of_cpus": 1,
                  "number_of_sockets": 2}

payloads = {
    "pup": {
        "account": "000001",
        "principal": "123456",
    },
    "hbi": {
        "operation": "add_host",
        "data": {
            "account": "000001",
            "insights_id": str(uuid.uuid4()),
            "bios_uuid": str(uuid.uuid4()),
            "fqdn": "fred.flinstone.com",
            "display_name": "fred.flinstone.com",
            "subscription_manager_id": str(uuid.uuid4()),
            "system_profile": system_profile,
        }
    },
}

def build_payload(payload_type):
    return payloads[payload_type]

