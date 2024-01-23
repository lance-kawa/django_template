import traceback

timeout = 3

def worker_abort(worker):
    pid = worker.pid
    print("worker is being killed - {}".format(pid))
    traceback.print_stack()