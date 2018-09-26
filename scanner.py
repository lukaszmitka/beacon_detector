from bluepy.btle import Scanner, DefaultDelegate
import sqlite3

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

def create_table(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS beacons (id INTEGER PRIMARY KEY AUTOINCREMENT, address STRING, rssi REAL, UNIQUE(address));")
    db_conn.commit() 

def update_device_status(db_conn, device_adress, rssi):
    cursor = db_conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO beacons (rssi, address) VALUES('" + str(rssi) + "', '" + device_adress + "');")
    cursor.execute("UPDATE beacons SET rssi = '" + str(rssi) + "' WHERE address= '" + device_adress + "';")        
    db_conn.commit()

scanner = Scanner().withDelegate(ScanDelegate())

conn = sqlite3.connect('beacon_detected.sqlite')
create_table(conn)

while 1:
    print "While loop"
    devices = scanner.scan(1.0)
    print "Detected devices %d" % (len(devices))
    print "%s" % (devices)

    for dev in devices:
        print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
        update_device_status(conn, dev.addr, dev.rssi)
    #     for (adtype, desc, value) in dev.getScanData():
    #         # print "  %s = %s" % (desc, value)
    #         a = desc
