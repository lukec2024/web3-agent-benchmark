import multiprocessing

bind = "0.0.0.0:7007"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"  # Or "gevent"(Install gevent first)
timeout = 600
accesslog = "log/access.log"
errorlog = "log/error.log"
loglevel = "info"