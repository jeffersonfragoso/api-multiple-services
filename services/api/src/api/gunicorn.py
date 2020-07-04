"""
This module has the configuration of gunicorn

"""

# pylint: skip-file

import json
import multiprocessing
from logging import StreamHandler
from api.settings import LOGGING_CONFIG

# ===============================================
#           Server Socket
# ===============================================

# bind - The server socket to bind
bind = '0.0.0.0:8000'

# ===============================================
#           Worker Processes
# ===============================================

# workers - The number of worker processes for handling requests.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
workers = 1

# threads - The number of worker threads for handling requests. This will
# run each worker with the specified number of threads.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
threads = 0

# timeout - Workers silent for more than this many seconds are killed
# and restarted
timeout = 30

# keep_alive - The number of seconds to wait for requests on a
# Keep-Alive connection
# Generally set in the 1-5 seconds range.
keep_alive = 2

# max_requests - The maximum number of requests a worker will process before restarting.
# Any value greater than zero will limit the number of requests a work will process
# before automatically restarting. This is a simple method to help limit the damage of memory leaks.
max_requests = 100

# max_requests_jitter - The maximum jitter to add to the max_requests setting.
# The jitter causes the restart per worker to be randomized by randint(0, max_requests_jitter).
# This is intended to stagger worker restarts to avoid all workers restarting at the same time.
max_requests_jitter = 30

# ===============================================
#           Debugging
# ===============================================

# reload - Restart workers when code changes
reload = True

# ===============================================
#           Server Mechanics
# ===============================================

# daemon - Daemonize the Gunicorn process.
# Detaches the server from the controlling terminal and enters the background.
daemon = False

# preload_app - Load application code before the worker processes are forked.
# By preloading an application you can save some RAM resources as well as speed up server boot times.
preload_app = True

# ===============================================
#           Logging
# ===============================================

logconfig_dict = LOGGING_CONFIG
