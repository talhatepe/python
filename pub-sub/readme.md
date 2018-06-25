#Pub/Sub

### •Publisher (pub.py):

```python
from flask import Flask, request, jsonify, abort
from google.cloud import pubsub

app = Flask(__name__)

project_name = 'my-project-py-207610'
topic_name = 'topics'
subscription_name = 'subs'

batch_settings = pubsub.types.BatchSettings(
    max_bytes=1024,  # One kilobyte
    max_latency=1,  # One second
)

publisher = pubsub.PublisherClient(batch_settings)
topic_path = publisher.topic_path(project_name, topic_name)


@app.route('/pubsub/topics', methods=['POST'])
def pushtotopic():
    if not "data" in request.args:
        abort(400)

    data = request.args['data']
    data = bytes(data, 'UTF-8')
    publisher.publish(topic_path, data=data)
    print("{0}".format(data))
    return jsonify({'result': 'OK'}), 200


if __name__ == '__main__':
    app.run(port='6666', threaded=True,debug=True)


```


### •Subscriber (sub.py):

```python
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
```


### •Message pusher to publisher (push.py):

```python
import requests

while True:
    str = str(input("Mesaj: "))
    str = bytes(str, 'UTF-8')
    r = requests.post("http://127.0.0.1:6666/pubsub/topics?data={0}".format(str))
    print(r.status_code, r.reason)
```