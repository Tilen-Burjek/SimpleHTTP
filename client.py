#!/usr/bin/python

import asyncio, sys, random, time, requests, threading

keep_running = True


async def process(id):
    """
    Outputs the threads userId and waits a random time between 0 and 1
    :param id: user id
    :return: None
    """
    r = requests.get(f"http://127.0.0.1:5000/?clientId={id}")
    time.sleep(random.random())


def get_input():
    """
    Keystroke enter stops running logic
    :return:
    """
    global keep_running
    input("Press enter to stop \n")
    keep_running = False


async def main():
    """
    Contains logic for populating and running tasks
    :return:
    """
    global number_of_clients, keep_running
    while keep_running:
        tasks = []
        for i in range(int(number_of_clients)):
            tasks.append(asyncio.ensure_future(process(i)))
        await asyncio.gather(*tasks)
        if not keep_running:
            print("Stopping clients")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        number_of_clients = sys.argv[1]
    else:
        number_of_clients = 1

    threading.Thread(target=get_input).start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()