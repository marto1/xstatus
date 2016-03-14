from twisted.internet import reactor, defer
from txdbus import error, client

@defer.inlineCallbacks
def call_method(
    bus,
    iface,
    path,
    method,
    cb,
    *args):
    try:
        cli   = yield client.connect(reactor, bus)
        robj  = yield cli.getRemoteObject(
            iface.name,
            path,
            iface)
        r = yield robj.callRemote(method, *args)
        cb(r)

    except error.DBusException, e:
        print 'DBus Error:', e


@defer.inlineCallbacks
def activate_notification(
    bus,
    iface,
    path,
    signal,
    cb):
    try:
        cli   = yield client.connect(reactor, bus)
        robj  = yield cli.getRemoteObject(
            iface.name,
            path,
            iface)
        robj.notifyOnSignal(signal, cb)

    except error.DBusException, e:
        print 'DBus Error:', e

@defer.inlineCallbacks
def update_state(
    bus,
    iface,
    path,
    property,
    cb):
    try:
        cli   = yield client.connect(reactor, bus)
        robj  = yield cli.getRemoteObject(
            iface,
            path)

        r = yield robj.callRemote('Get', '', property)
        cb(r)

    except error.DBusException, e:
        print 'DBus Error:', e
