# -*- coding: utf-8 -*-
import os
import sys
import time
import signal
import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, LoggingEventHandler


class NginxConfigReloadHandler(PatternMatchingEventHandler):
    patterns = ['*.conf']
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = False

    def on_any_event(self, event):
        # if self._confirm_correct_config():
        #    with open('/run/nginx.pid', mode='r') as f:
        #        pid = int(f.read())
        #        os.kill(pid, signal.SIGHUP)
        # super().on_any_event(event)
        print('ble')

    @staticmethod
    def _confirm_correct_config():
        return True


if __name__ == "__main__":
    path = os.path.abspath('.')  # sys.argv[1] if len(sys.argv) > 1 else '.'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
