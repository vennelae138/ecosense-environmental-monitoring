from flask import Flask, render_template, jsonify, request
import sqlite3, random, os
from datetime import datetime, timedelta

app = Flask(__name__)
DB_PATH = os.environ.get("ECOSENSE_DB", os.path.join(os.path.dirname(__file__), "ecosense.db"))
LOCATIONS = {
    "College Campus": {"temperature": 29.4, "humidity": 64, "aqi": 42},
    "City Centre": {"temperature": 32.1, "humidity": 51, "aqi": 78},
    "Green Park": {"temperature": 27.8, "humidity": 71, "aqi": 28},
    "Industrial Area": {"temperature": 34.2, "humidity": 46, "aqi": 126},
}

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, location TEXT NOT NULL,
            temperature REAL NOT NULL, humidity REAL NOT NULL, aqi INTEGER NOT NULL,
            created_at TEXT NOT NULL)""")
        if conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0] == 0:
            now = datetime.now()
            for loc, base in LOCATIONS.items():
                for i in range(24):
                    t = now - timedelta(hours=23-i)
                    conn.execute("INSERT INTO readings(location,temperature,humidity,aqi,created_at) VALUES(?,?,?,?,?)",
                        (loc, round(base["temperature"]+random.uniform(-2,2),1),
                         max(20,min(95,round(base["humidity"]+random.uniform(-8,8)))),
                         max(5,round(base["aqi"]+random.uniform(-12,12))),t.isoformat(timespec="seconds")))

def sample(location):
    b=LOCATIONS[location]
    return {"location":location,"temperature":round(b["temperature"]+random.uniform(-1.2,1.2),1),
            "humidity":max(15,min(95,round(b["humidity"]+random.uniform(-4,4)))),
            "aqi":max(5,round(b["aqi"]+random.uniform(-8,8))),
            "created_at":datetime.now().isoformat(timespec="seconds"),
            "source":"Simulated demo data"}

@app.route("/")
def home():
    return render_template("index.html", locations=list(LOCATIONS))

@app.get("/api/reading")
def reading():
    location=request.args.get("location","College Campus")
    if location not in LOCATIONS: return jsonify({"error":"Unknown location"}),400
    r=sample(location)
    with db() as conn:
        conn.execute("INSERT INTO readings(location,temperature,humidity,aqi,created_at) VALUES(?,?,?,?,?)",
                     (location,r["temperature"],r["humidity"],r["aqi"],r["created_at"]))
    return jsonify(r)

@app.get("/api/history")
def history():
    location=request.args.get("location","College Campus")
    if location not in LOCATIONS: return jsonify({"error":"Unknown location"}),400
    with db() as conn:
        rows=conn.execute("SELECT temperature,humidity,aqi,created_at FROM readings WHERE location=? ORDER BY id DESC LIMIT 24",(location,)).fetchall()
    return jsonify([dict(row) for row in rows][::-1])

@app.get("/health")
def health():
    return jsonify({"status":"ok","app":"EcoSense"})

init_db()
if __name__=="__main__":
    app.run(debug=True,host="127.0.0.1",port=int(os.environ.get("PORT",5000)))
