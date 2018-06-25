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

