from bluepy.btle import Scanner, DefaultDelegate
import sqlite3
import datetime

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
    cursor.execute("CREATE TABLE IF NOT EXISTS `Beacons` (id INTEGER PRIMARY KEY AUTOINCREMENT, address STRING NOT NULL, rssi REAL NOT NULL, `createdAt` DATETIME NOT NULL, `updatedAt` DATETIME NOT NULL, UNIQUE(address));")
    db_conn.commit() 

def update_device_status(db_conn, device_adress, rssi):
    cursor = db_conn.cursor()
    time_now = datetime.datetime.now()
    cursor.execute("INSERT OR IGNORE INTO `Beacons` (rssi, address, createdAt, updatedAt) VALUES('" + str(rssi) + "', '" + device_adress + "', '" + str(time_now) + "', '" + str(time_now) + "');")
    cursor.execute("UPDATE `Beacons` SET rssi = '" + str(rssi) + "', updatedAt = '" + str(time_now) + "' WHERE address= '" + device_adress + "';")        
    db_conn.commit()

def delete_old_devices(db_conn, address_list):
    cursor = db_conn.cursor()
    time_now = datetime.datetime.now()
    command = ""
    if len(address_list)>0:
        command = "DELETE FROM `Beacons` WHERE"
        first_element = True
        for address in address_list:
            if first_element:
                first_element = False
            else:
                command += " AND "
            command += " address != '"
            command += address
            command += "' "
        command +=";"
    else:
        command = "DELETE FROM `Beacons`;"
    print command
    cursor.execute(command)
    db_conn.commit()

scanner = Scanner().withDelegate(ScanDelegate())

conn = sqlite3.connect('beacon_detected.sqlite')
create_table(conn)

while 1:
    print "While loop"
    devices = scanner.scan(1.0)
    print "Detected devices %d" % (len(devices))
    print "%s" % (devices)

    addresses = list()
    for dev in devices:
        print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
        update_device_status(conn, dev.addr, dev.rssi)
        addresses.append(dev.addr)
    delete_old_devices(conn, addresses)
    #     for (adtype, desc, value) in dev.getScanData():
    #         # print "  %s = %s" % (desc, value)
    #         a = desc
