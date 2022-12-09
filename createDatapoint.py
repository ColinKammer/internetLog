import datetime
import time
import sys

# pip install mariadb
import mariadb as dbInterface
# pip install icmplib
import icmplib as icmp

server = sys.argv[1]
databaseName = sys.argv[2]
user = sys.argv[3]
passwd = sys.argv[4]

pingServers = [
    "192.168.1.1",
    "google.de",
    "reddit.com",
    "amazon.de",
    "youtube.com",
    "facebook.de",
    "1.1.1.1",
    "steampowered.de"]


def insertPing(cursor, creationTime, server,
               receivedPackets, avgLatency_ms):
    cursor.execute("""
        INSERT INTO InternetLog_Pings ( createdAt, server, receivedPackets, avgLatency_ms )
        VALUES (?, ?, ?, ?);
        """, (creationTime, server, receivedPackets, avgLatency_ms))


def asSqlTimestamp(time: float):
    return datetime.datetime.fromtimestamp(time).strftime('%Y.%m.%d %H:%M:%S')


def runPing(server: str):
    pingRes = icmp.ping(server, count=4, interval=0.2,
                        timeout=1.0, privileged=False)
    relativepackets = pingRes.packets_received / pingRes.packets_sent
    return [relativepackets, pingRes.avg_rtt]


if __name__ == '__main__':
    db = dbInterface.connect(
        host=server,
        user=user,
        password=passwd,
        database=databaseName)

    creationTime = asSqlTimestamp(time.time())

    for server in pingServers:
        receivedPackets, avgLatency_ms = runPing(server)
        insertPing(db.cursor(), creationTime, server,
                   receivedPackets, avgLatency_ms)
        print(f"Handled ping to {server}: avg_latency={avgLatency_ms}ms")
    db.commit()
    db.close()
