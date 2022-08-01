import time
import threading

from databases_watcher import connect_database

CONNECTION_STRING = "redis+pubsub://localhost:6501/?db=0&channel=default"

def background_read_pubsub():
    redis_watch = connect_database(CONNECTION_STRING)

    print(next(redis_watch.read_messages()))
    print(next(redis_watch.read_json_messages()))


def main():
    redis_watch = connect_database(CONNECTION_STRING)

    t = threading.Thread(target=background_read_pubsub)
    t.start()

    time.sleep(2)

    redis_watch.send_message("hello!")
    redis_watch.send_json_message({"message": "hello!"})

    t.join()

if __name__ == '__main__':
    main()
