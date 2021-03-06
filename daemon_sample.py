#!/opt/python3/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import psutil
import signal
import logging


class Daemon(object):
    """
    Usage: - create your own a subclass Daemon class and override the run() method. Run() will be periodically the calling inside the infinite run loop
           - you can receive reload signal from self.isReloadSignal and then you have to set back self.isReloadSignal = False
    """

    def __init__(self, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.ver = 0.1  # version
        # 0 means none pause between the calling of run() method.
        self.pauseRunLoop = 0
        # 0 means without a pause between stop and start during the restart of the daemon
        self.restartPause = 1
        # when terminate a process, wait until kill the process with SIGTERM signal
        self.waitToHardKill = 3

        self.isReloadSignal = False
        self._canDaemonRun = True
        self.processName = os.path.basename(sys.argv[0])
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def _sigterm_handler(self, signum, frame):
        self._canDaemonRun = False

    def _reload_handler(self, signum, frame):
        self.isReloadSignal = True

    def _makeDaemon(self):
        """
        Make a daemon, do double-fork magic.
        """

        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent.
                sys.exit(0)
        except OSError as e:
            m = "Fork #1 failed: {}".format(e)
            print(m)
            sys.exit(1)

        # Decouple from the parent environment.
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Do second fork.
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent.
                sys.exit(0)
        except OSError as e:
            m = "Fork #2 failed: {}".format(e)
            print(m)
            sys.exit(1)

        m = "The daemon process is going to background."
        print(m)

        # Redirect standard file descriptors.
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    def _getProces(self):
        procs = []

        for p in psutil.process_iter():
            if self.processName in [part.split('/')[-1] for part in p.cmdline()]:
                # Skip  the current process
                if p.pid != os.getpid():
                    procs.append(p)

        return procs

    def start(self):
        """
        Start daemon.
        """

        # Handle signals
        signal.signal(signal.SIGINT, self._sigterm_handler)
        # go to null -> si = open(os.devnull, 'r')
        signal.signal(signal.SIGTERM, self._sigterm_handler)
        signal.signal(signal.SIGHUP, self._reload_handler)

        # Check if the daemon is already running.
        procs = self._getProces()

        if procs:
            m = "Find a previous daemon processes with PIDs {}. Is not already the daemon running?".format(
                ",".join([str(p.pid) for p in procs]))
            print(m)
            sys.exit(1)
        else:
            m = "Start the daemon version {}".format(self.ver)
            print(m)

        # Daemonize the main process
        self._makeDaemon()
        # Start a infinitive loop that periodically runs run() method
        self._infiniteLoop()

    def version(self):
        print("The daemon version {}".format(self.ver))

    def status(self):
        """
        Get status of the daemon.
        """

        procs = self._getProces()

        if procs:
            m = "The daemon is running with PID {}.".format(
                ",".join([str(p.pid) for p in procs]))
            print(m)
        else:
            m = "The daemon is not running!"
            print(m)

    def reload(self):
        """
        Reload the daemon.
        """

        procs = self._getProces()

        if procs:
            for p in procs:
                os.kill(p.pid, signal.SIGHUP)
                m = "Send SIGHUP signal into the daemon process with PID {}.".format(
                    p.pid)
                print(m)
        else:
            m = "The daemon is not running!"
            print(m)

    def stop(self):
        """
        Stop the daemon.
        """

        procs = self._getProces()

        def on_terminate(process):
            m = "The daemon process with PID {} has ended correctly.".format(
                process.pid)
            print(m)

        if procs:
            for p in procs:
                p.terminate()

            gone, alive = psutil.wait_procs(
                procs, timeout=self.waitToHardKill, callback=on_terminate)

            for p in alive:
                m = "The daemon process with PID {} was killed with SIGTERM!".format(
                    p.pid)
                print(m)
                p.kill()
        else:
            m = "Cannot find some daemon process, I will do nothing."
            print(m)

    def restart(self):
        """
        Restart the daemon.
        """
        self.stop()

        if self.restartPause:
            time.sleep(self.restartPause)

        self.start()

    def _infiniteLoop(self):
        try:
            if self.pauseRunLoop:
                time.sleep(self.pauseRunLoop)

                while self._canDaemonRun:
                    self.run()
                    time.sleep(self.pauseRunLoop)
            else:
                while self._canDaemonRun:
                    self.run()

        except Exception as e:
            m = "Run method failed: {}".format(e)
            sys.stderr.write(m)
            sys.exit(1)

    # this method you have to override
    def run(self):
        pass


########################################################################################################################

# example of a custom run method
class MyDaemon(Daemon):
    def run(self):
        x = 10
        y = x ** 10
        return y

    def main(self):
        a = run.y()
        print(a)


########################################################################################################################


if __name__ == "__main__":
    daemon = MyDaemon()
    daemon.main()

    usageMessage = "Usage: {} (start|stop|restart|status|reload|version)".format(
        sys.argv[0])

    if len(sys.argv) == 2:
        choice = sys.argv[1]
        if choice == "start":
            daemon.start()
        elif choice == "stop":
            daemon.stop()
        elif choice == "restart":
            daemon.restart()
        elif choice == "status":
            daemon.status()
        elif choice == "reload":
            daemon.reload()
        elif choice == "version":
            daemon.version()
        else:
            print("Unknown command.")
            print(usageMessage)
            sys.exit(1)
        sys.exit(0)
    else:
        print(usageMessage)
        sys.exit(1)
