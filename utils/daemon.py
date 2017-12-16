#-*- coding: utf-8 -*-


import os
import sys
import time
import atexit 
import string
import signal
from signal import SIGTERM, SIGKILL

#description: 一个守护进程包装类, 具备常用的start|stop|restart|status功能, 使用方便  
#需要改造为守护进程的程序只需要重写基类的run函数就可以了

class CDaemonWrap(object):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', *args, **kwargs):
        #需要获取调试信息，改为stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr'，以root身份运行。
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        super(CDaemonWrap, self).__init__(*args, **kwargs)

    def _daemonize(self):
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0) 
        except OSError, e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)
            
        basedir = os.path.expanduser(r'~')
        os.chdir(basedir)
        os.setsid() 
        os.umask(0) 
  
        #创建子进程
        try: 
            pid = os.fork() 
            if pid > 0:
                sys.exit(0)
        except OSError, e: 
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1) 
  
        #重定向文件描述符
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
  
        #创建processid文件
        pid = str(os.getpid())
        file(self.pidfile,'w+').write('%s\n' % pid)

        #signal.signal(SIGKILL, sig_handler)    
        #signal.signal(SIGTERM, sig_handler)
        #注册进程退出时的回调
        atexit.register(self.del_pid)

    # def sig_handler(signum, frame):
    #     self.del_pid()

    def get_pid(self):
        #从pid文件中获取pid
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        return pid

    def del_pid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def start(self, *args, **kwargs):
        #检查pid文件是否存在以探测是否存在进程
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
  
        if pid:
            sys.stderr.write('pidfile %s already exist. Daemon already running?\n' % self.pidfile)
            sys.exit(1)
    
        #start the daemon  
        self._daemonize()
        self._run(*args, **kwargs)

    def stop(self):
        pid = self.get_pid()
        if not pid:
            message = 'pid file %s does not exist. Process not running\n' %self.pidfile
            sys.stderr.write(message % self.pidfile)
            return

        #try to kill the daemon process  
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find('No such process') > 0:
                self.del_pid()
            else:
                sys.stdout.write('Daemon starting...') 
                sys.stdout.write('%s' %err) 
                sys.exit(1)

    def restart(self, *args, **kwargs):
        self.stop()
        self.start(*args, **kwargs)

    def _run(self, *args, **kwargs):
        pass