import payloads
import config

PUP = {"produce_topic": "platform.upload.advisor",
       "consume_topic": "platform.inventory.host-ingress",
       "msg": payloads.build_payload("pup")
       }

HBI = {"produce_topic": "platform.inventory.host-ingress",
       "consume_topic": "platform.inventory.host-egress",
       "msg": payloads.build_payload("hbi")
       }
