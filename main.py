import cherrypy
import threading
import subprocess
import config as c


def do_every(interval, worker_func, iterations=0):
    if iterations != 1:
        threading.Timer(
            interval,
            do_every, [interval, worker_func,
                       0 if iterations == 0 else iterations - 1]
        ).start()
    worker_func()


def exe(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return output


class GetServerStatus(object):
    def __init__(self):
        do_every(0.5, self.every_1s)
        do_every(1, self.every_5s)

    status = {'uptime': 0, 'temp': 0, 'cpu': 0}

    def every_1s(self):
        self.status['uptime'] = int(float(str(exe(c.uptime)).split()[0][2:]))
        self.status['temp'] = int(str(exe(c.temp_a))[2:4])
        self.status['cpu'] = int(c.cpu_usage())

    def every_5s(self):
        pass

    def every_30s(self):
        pass

    def every_1m(self):
        pass

    def every_5m(self):
        pass

    def every_30m(self):
        pass

    def every_1h(self):
        pass

    @cherrypy.expose
    def cpu(self):
        return str(self.status['cpu'])

    @cherrypy.expose
    def temp(self):
        return str(self.status['temp'])

    @cherrypy.expose
    def uptime(self):
        return str(self.status['uptime'])

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return self.status

cherrypy.quickstart(GetServerStatus())
