import requests

while True:
    str = str(input("Mesaj: "))
    str = bytes(str, 'UTF-8')
    r = requests.post("http://127.0.0.1:6666/pubsub/topics?data={0}".format(str))
    print(r.status_code, r.reason)