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
        self.cursor = self.conn.cursor();
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
            #print("PostgreSQL Connection is Closed");
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

    def loadData(self):
        self.cursor = self.conn.cursor();
        self.cursor.execute("select * from thrmresult;");
        results = self.cursor.fetchall();
        self.cursor.close();
        return results;

    def dataOut(self, blurVal, outputs):
        r = self.loadData(); # r[i][12] is id
        self.cursor = self.conn.cursor();
        a = self.select("select * from thrmresultaoi;"); # a[i][19] is id
        rids = [item[12] for item in r];
        aids = [item[19] for item in a];
        exceptid = [];
        for i in range(len(rids)):
            if rids[i] in aids:
                exceptid.append(rids[i]);
        a = tuple(exceptid) if len(exceptid) > 0 else '(-1)';
        if len(a)==1:
            a = str(a)[:-2]+")";
        self.cursor = self.conn.cursor();
        r = self.select(f"select dbindex, equipmentkey, mptkey, dcsid, eventid, id from thrmresult where id not in {a}");
        self.cursor = self.conn.cursor();
        for i in range(len(r)):
            if outputs[i][20] < blurVal:
                outputs[i] = ['NULL' for j in range(len(outputs[i]))];
                self.update(f"update thrmresult set falsemeasure=True where id={r[i][5]}");
            self.insert(f"""insert into thrmresultaoi(dbindex, equipmentkey, mptkey, dcsid, eventid, aoiid, limittemp, maxtemp, mintemp, avgtemp, deltatemp, confidencefactor, tempalarm, deltaalarm, diagnosiscode, diagnosisresult, failuretype, hp, rp, id, createdate, updatedate, boxpoint, pointtemp, deltamax, deltamin, bluralarm, recommendaction, measuredevice, imagesize, imagetype)
                    values('{r[i][0]}', '{r[i][1]}', '{r[i][2]}', '{r[i][3]}', '{r[i][4]}', {outputs[i][0]}, {outputs[i][1]}, {outputs[i][2]},
                    {outputs[i][3]}, {outputs[i][4]}, {outputs[i][5]}, {outputs[i][6]}, '{outputs[i][7]}', '{outputs[i][8]}', '{outputs[i][9]}',
                    '{outputs[i][10]}', '{outputs[i][11]}','{outputs[i][12]}','{outputs[i][13]}','{r[i][5]}',{outputs[i][14]},{outputs[i][15]},'{outputs[i][16]}',
                    {outputs[i][17]},{outputs[i][18]},{outputs[i][19]},{outputs[i][20]},'{outputs[i][21]}','{outputs[i][22]}','{outputs[i][23]}',
                    '{outputs[i][24]}')""");
        self.cursor.close();
