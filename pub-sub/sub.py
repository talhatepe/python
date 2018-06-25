import time

from google.cloud import pubsub_v1

project_name = 'my-project-py-207610'
topic_name = 'topics'
subscription_name = 'subs'

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_name, subscription_name)


def callback(message):
    print('Received message: {}, date: {}'.format(message, int(time.time())))
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)

print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)