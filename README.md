# Platform Component Tester

The purpose of the platform component tester is to be able to test individual platform components in isolation. The test suite is composed of a consumer and a producer. The producer sends a pre-crafted method to the component being tested and the consumer reads from the queue on the other side of the component. The tester requires a kafka instance as well as the component to be current running in the environment you are testing with. The test can be run locally or in Openshift.

## Details

The below sequence diagram shows the workflow of the test

![UML](http://www.plantuml.com/plantuml/png/RP31JlGm38JlVGhV_jE-m1vMA_rd48Wz8g4ecRH6RHpPRX5lZy9kLbHmS-jlnfavcmVrTPdfQGwUHHVwBqkLWk9qWJbqg46T8zTGdAfAMYDqG77sp_xzvb8vxaY3RXpHmIZ5rkKFi6zqwDw7qyxrI2yeYQmYSkP82yp227AXgzcZE4Xvd9maKtSvqcN27MQZG553TYHocDytxwjvywh1ZBOmSmhEKbwB2R4tOHRz29gG6kOJI7o2ad72i7lfuNGBVVnH8fSHvjQ4kyF3ZJsSUZKzxVK_6KgotsbtT1Utk7qYHGHl-3xPzTUIPkJMqGtj7Ts5R6tEFAwAH58eKEASeIt7mpEDAcljnII1bNzEia7dK4aHPd8DENCSpYXfNURX2m00 "Platform Component Tester")

## Running

The system expects kafka and the component to be up and running. You can do this by following the instructions in the repo for the component you are trying to test. Standing up each individual one might require different steps and that is out of scope for this readme.

Requires: 
Python >= 3.6 

The app can be run directly from within a virtual environment, or deployed as a container using docker, podman, or Openshift.

When the consumer pulls in the message it will read the `elapsed_time` key if it is available and print the time it spent in the component you are testing. This is an optional field and should be set within the app if at all possible. A secondary option is for the producer to tag the time, and the consumer to subtract that time when it receives the message. This incorporates kafka lag, so it may be that the times are longer than they should be.

### Consumer

Standing up the consumer should be done first as it will simply sit and wait for messages to show up on the corresponding topic. The app is set to consume by default, so you should only need to specify kafka and the component to test when launching.

     $> BOOTSTRAP_SERVERS=kafka:29092 COMPONENET=<service> python app.py
    
### Producer

The producer requires a bit more configuration. The producer needs a repository of archives to pull from in order to send them through the system. You can use Minio if testing locally and AWS creds if you are testing within one of our Openshift instance. If using Minio, the producer will need there to be archives currently in your minio instance and you may need to modify the bucket name if yours differ from the defaults.

    $> ROLE=produce COMPONENT=<service> BOOTSTRAP_SERVERS=kafka:2902 MINIO_ACCESS_KEY=<string> MINIO_SECRET_KEY=<string> python app.py

### Using containers

You can also build a container using source-to-image

    s2i build . centos/python-36-centos7 platform-component-tester:latest -e ENABLE_PIPENV=true

Then you can simply launch using docker or podman

    docker run -d platform-component-tester:latest
    OR
    podman run -d platform-component-tester:latest

## Contributing

If you have a new component to add to the framework, you will need to update the `maps.py` file with the mappings to provide the consume_topic, produce_topic, and message to send through the system.

     SERVICE = {"produce_topic": TOPIC,
                "consume_topic": ANOTHER_TOPIC,
                "msg": {MESSAGE JSON}
                }

## Authors

* Stephen Adams - Initial Work - [SteveHNH](https://www.github.com/SteveHNH)
