import psycopg2 as pg;
import json;

class PostgreConn:
    # Init Connection
    def __init__(self, User, Password, Host, Port, DB):
        self.User = User;
        self.Password = Password;
        self.Host = Host;
        self.Port = Port;
        self.DB = DB;
        try:
            self.conn = pg.connect(user=User, password=Password, host=Host, port=Port, database=DB);
            self.cursor = self.conn.cursor();
        except (Exception, pg.Error) as error:
            print("Error while connecting to PostgreSQL Server\n", error);
    # connection test
    def test(self):
        print(self.conn.get_dsn_parameters(), "\n");
        self.cursor.execute("SELECT version();");
        print(f"You are Successfully connected to {self.cursor.fetchone()}\n");
    # SELECT with sql
    def select(self, sql):
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        self.cursor.close();
        return results;
    # INSERT with sql
    # If you want to insert only one record into table, simply write sql about that.

    # ----------------- In Bulk INSERT Case --------------------
    # If bulkInsert, bulk=True & records should have tuples in list format.
    # And in bulkInsert, sql's values() should have %s.

    # For example,  bulk = True
    #               sql = "INSERT INTO tbl1(attr1, attr2, attr3) values(%s, %s, %s)"
    #               records = [(attr1_val1, attr2_val1, attr3_val1), (attr1_val2, attr2_val2, attr3_val2), (attr1_val3, attr2_val3, attr3_val3)]
    # => Total 3 records are inserted into tbl1
    def insert(self, sql, bulk=False, records=[]):
        if bulk:
            self.cursor.executemany(sql, records);
            self.conn.commit();
            print(f"{self.cursor.rowcount} records inserted successfully into Table");
        else:
            self.cursor.execute(sql);
            self.conn.commit();
            print(f"{self.cursor.rowcount} record inserted successfully into Table");
    # UPDATE with sql
    # So many parts are similar to INSERT function

    # ---------------- In Bulk UPDATE Case ----------------------
    # Example
    # bulk = True
    # sql = "UPDATE tbl1 SET %s WHERE %s"
    # params = [('attr1=val1', 'attr3="updateAttr1"'), ('attr1=val1, attr2=val2', 'attr3="updateAttr1and2"')]
    # => This is just example, %s is universal
    def update(self, sql, bulk=False, params=[]):
        if bulk:
            self.cursor.executemany(sql, params);
            self.conn.commit();
            print(f"{self.cursor.rowcount} records Updated");
        else:
            self.cursor.execute(sql);
            self.conn.commit();
            print(f"{self.cursor.rowcount} record Updated");
    # If you want DELETE records, Just use insert() or update() in non-bulk option.
    # Example
    # a.insert("DELETE FROM tbl1 WHERE attr3='DELETE'")
    # Maybe you will see "X record inserted suc...", Ignore the console output.
    # ---------------- Connection -------------------
    # connection release
    def close(self):
        if(self.conn):
            self.cursor.close();
            self.conn.close();
            print("PostgreSQL Connection is Closed");
    # Re-connection
    # Reconnect database with initial Information
    def reconnect(self):
        try:
            self.conn = pg.connect(user=self.User, password=self.Password, host=self.Host, port=self.Port, database=self.DB);
            self.cursor = self.conn.cursor();
        except (Exception, pg.Error) as error:
            print("Error while connecting to PostgreSQL Server\n", error);
    # SAVE Data to JSON FILE
    # If you want to save one table's information to JSON file, use that.
    # Example
    # a.saveJSON("tblName", "JSONFileName");
    def saveJSON(self, tbl, jsonFile):
        self.cursor = self.conn.cursor();
        self.cursor.execute(f"select * from {tbl}");
        r = [dict((self.cursor.description[i][0], value)
                  for i, value in enumerate(row)) for row in self.cursor.fetchall()];
        with open(jsonFile, "w") as J:
            json.dump(r, J, indent=4, sort_keys=True, default=str);
            print(f"{tbl}'s Data successfully written in {jsonFile}");