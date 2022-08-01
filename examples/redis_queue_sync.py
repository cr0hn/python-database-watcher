from databases_watcher import connect_database

def main():
    redis_watch = connect_database("redis://localhost:6501/?db=0&queue=default")

    redis_watch.send_message("hello!")
    redis_watch.send_json_message({"message": "hello!"})

    print(next(redis_watch.read_messages()))
    print(next(redis_watch.read_json_messages()))


if __name__ == '__main__':
    main()
