# -*- coding: utf-8 -*-
import os
import time
import signal
import logging
import argparse
import subprocess

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


parser = argparse.ArgumentParser()
parser.add_argument(
    '--config',
    type=str,
    required=True,
    help='Nginx config directory to watch for changes.'
)
parser.add_argument(
    '--pidfile',
    type=str,
    required=True,
    help='Nginx file containing PID of the master process.'
)
parser.add_argument(
    '--log',
    type=str,
    help='Optional log file destination for easy debugging.'
)

args = parser.parse_args()

LOG_DESTINATION = args.log
CONFIG_DIRECTORY = args.config
PID_FILE = args.pidfile

logger = logging.getLogger('nginx-reloader')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(console_formatter)
logger.addHandler(console)

if args.log:
    # create file handler which logs even debug messages
    file = logging.FileHandler(LOG_DESTINATION)
    file.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # tell the handler to use this format
    file.setFormatter(file_formatter)
    logger.addHandler(file)


class NginxConfigReloadHandler(PatternMatchingEventHandler):
    patterns = ['*.conf']
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = False

    def on_any_event(self, event):
        if self._confirm_correct_config():
           with open(PID_FILE, mode='r') as f:
               pid = int(f.read())
               print('Reloading nginx master proces with PID: {}'.format(pid))
               os.kill(pid, signal.SIGHUP)
               print('HUP signal sent!')

    @staticmethod
    def _confirm_correct_config():
        proc = subprocess.run('nginx -t', stdout=subprocess.PIPE, shell=True)
        if proc.returncode != 0:
            print('Aborting reload!')
            return False
        else:
            print('Configuration correct.')
            return True


def main():
    path = os.path.abspath(CONFIG_DIRECTORY)
    event_handler = NginxConfigReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
