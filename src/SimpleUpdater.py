import requests

try:
    from config import config
except ImportError:
    print('import error')
    from src.config import config

import time

current_ip = ''
running = True


def update_no_ip():
    global current_ip
    try:
        new_ip = requests.get('http://api.ipify.org').text
        if new_ip != current_ip:
            current_ip = new_ip
            update = requests.get(
                config['update_url'].format(config['username'], config['password'], config['hostname'], current_ip))
            print(update.status_code)
        else:
            print('IP didnt change, no update necessary')
    except Exception as e:
        print('Could not update IP, error --> ', e)
        return


def get_timestamp_in_milli():
    return int(round(time.time() * 1000))


while running:
    # take timestamp
    before_task_milli_time = get_timestamp_in_milli()
    # execute task
    update_no_ip()
    # take second timestamp
    after_task_milli_time = get_timestamp_in_milli()
    # substract timestamps
    milli_diff = after_task_milli_time - before_task_milli_time
    # subtract passed time from waittime
    time_to_wait_in_seconds = config['update_interval_in_seconds'] - milli_diff / 1000
    if time_to_wait_in_seconds < 0:
        print('Updating took longer than your configured interval, waiting for normal interval instead:  ',
              str(config['update_interval_in_seconds']), 'seconds.')
        time_to_wait_in_seconds = config['update_interval_in_seconds']
    else:
        print('Updating took ', str(milli_diff), 'ms, waiting for ', str(time_to_wait_in_seconds), 'seconds.')
    # wait
    time.sleep(time_to_wait_in_seconds)
