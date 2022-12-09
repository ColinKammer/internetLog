import sys

# pip install mariadb
import mariadb as dbInterface

server = sys.argv[1]
databaseName = sys.argv[2]
user = sys.argv[3]
passwd = input(f"DB: Enter password for priviledged user {user}@{server}: ")

insertOnlyUser = "InternetLogInsertOnly"
insertOnlyUserPassWd = "passWdForInternetLog"

if __name__ == "__main__":
    db = dbInterface.connect(
        host=server,
        user=user,
        password=passwd,
        database=databaseName)
    print(db)

    print("Creating Tables")
    db.cursor().execute("""
            CREATE TABLE IF NOT EXISTS InternetLog_Pings(
                createdAt DATETIME,
                server VARCHAR(20),
                receivedPackets FLOAT,
                avgLatency_ms FLOAT,
                PRIMARY KEY( createdAt, server )
            );
        """)

    print("Creating User")
    db.cursor().execute(
        f"GRANT INSERT ON {databaseName}.InternetLog_Pings " +
        f"TO '{insertOnlyUser}' IDENTIFIED BY '{insertOnlyUserPassWd}';")

    db.commit()

    db.close()
