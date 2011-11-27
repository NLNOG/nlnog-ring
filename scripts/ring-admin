#!/usr/bin/env python
import sqlite3, sys, inspect

DB='./ring.sqlite'

class commands(object):
    def __init__(self):
        super(commands, self).__init__()

    def run(self, argv):
        func = None
        for i in reversed(range(len(argv))):
            try:
                func = getattr(self, 'cmd_'+'_'.join(argv[0:i+1]))

                args, kwargs = self.splitargv(argv[i+1:])
                break
            except AttributeError:
                pass

        if not func:
            return self.usage()
        func(*args, **kwargs)
    
    def splitargv(self, argv):
        args = list()
        kwargs = dict()
        for arg in argv:
            if '=' in arg:
                k,v = arg.split('=',1)
                kwargs[k]=v
            else:
                if kwargs:
                    raise SyntaxError
                args.append(arg)
        
        return args, kwargs

    def usage(self):
        cmds = []
        for k, v in sorted(inspect.getmembers(self)):
            if k.startswith('cmd_'):
                cmd = k[4:].replace('_',' ')
                argspec = inspect.getargspec(v)
                args = []
                if argspec.defaults:
                    defcount = len(argspec.defaults)
                    print 'defcount %r argsub %r' % (defcount, argspec.args[0:-defcount])
                    for arg in argspec.args[1:-defcount]:
                        args.append('<%s>' % arg)
                    for arg in argspec.args[-defcount:]:
                        args.append('[%s]' % arg)
                else:
                    for arg in argspec.args[1:]:
                        args.append('<%s>' % arg)
                doc=v.__doc__
                if not doc:
                    doc=''
                cmds.append(('%s %s' % (cmd, ' '.join(args)), doc))

        maxcmdlen = max(len(cmd[0]) for cmd in cmds)
        for cmd, doc in cmds:
            print '%-*s %s' % (maxcmdlen+2, cmd, doc)
        return 1
    
    def dbdo(self, q, v):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(q, v)
        conn.commit()
        return cur.rowcount, cur.lastrowid
    
    def dbquery(self, q, v=None):
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if v:
            cur.execute(q, v)
        else:
            cur.execute(q)
        for row in cur:
            yield row

    def dbselect(self, table, **kwargs):
        cols, vals = zip(*kwargs.items())
        query = 'SELECT * FROM %s WHERE %s' % (table, ' '.join('%s=?' % col for col in cols))
        return self.dbquery(query, vals)

    def dbselectone(self, table, **kwargs):
        res = list(self.dbselect(table, **kwargs))
        if len(res)>1:
            raise KeyError
        elif res:
            return res[0]
        else:
            return None
        
    def dbinsert(self, table, **kwargs):
        cols, vals = zip(*kwargs.items())
        query = 'INSERT INTO %s (%s) VALUES(%s)' % (table, ','.join(cols), ','.join(['?']*len(vals)))
        _, rowid = self.dbdo(query, vals)
        return rowid

    def dblist(self, table):
        query = 'SELECT * FROM %s' % table
        result = self.dbquery(query)
        for row in result:
            print row

    def cmd_add_participant(self, company, url, autnum, noc_email):
        """add a participant"""
        self.dbinsert('participants', company=company, autnum=autnum, url=url) # noc_email!

    #[20:09] <job> ring-admin add machine $name $participant $location 
    def cmd_add_machine(self, participant, name, country):
        res = self.dbselectone('participants', id=participant)
        machineid = self.dbinsert('machines', participant=participant, name=name, country=country)
        print "Added machine %s ('%s' at '%s') for participant '%s'" % (machineid, name, country, res['company'])

    def cmd_list_participants(self, pid=None):
        if pid:
            print self.dbselectone('participants', id=pid)
        else:
            self.dblist('participants')

    def cmd_list_machines(self):
        self.dblist('machines')

def run(args):
    c = commands()
    c.run(args)

if __name__ == "__main__":
    c = commands()
    sys.exit(c.run(sys.argv[1:]))