from flask import Flask, render_template, jsonify, request
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler


BeaconLocations = {
"DE69F34B12FB": "Lvl 1 Fire Fighting Lobby",
"D7EBDC5A92B9": "Lvl 1 Fire Fighting Lobby",
"C43298D4E8B2": "Lvl 1 Fire Fighting Lobby",
"F3B1B290486D": "Student Club",
"D975F28047B3": "Foyer",
"DB45ECD1DF33": "Foyer",
"ECAC7EDCDF93": "LT2A Lobby",
"D7BFA52AA899": "LT2A Lobby",
"D249FA5CECA0": "LT2B Lobby"
}

StaffId = {
"001": "DE69F34B12FB",
"002": "D7EBDC5A92B9",
"003": "C43298D4E8B2",
"004": "F3B1B290486D",
"005": "D975F28047B3",
"006": "DB45ECD1DF33",
"007": "ECAC7EDCDF93",
"008": "D7BFA52AA899",
"009": "D249FA5CECA0"
}



app = Flask(__name__)

# insert your IP here
ip_address = "localhost"

@app.route('/')
def index():
	return ('hello world')

@app.route('/asd',methods=["POST"])
def baaa():
	reply = request.form["hello"]
	return (reply)

#HACS Server
@app.route('/extractbeacon')
def baaaa():
	staff_id = request.args.get("staff_id", None)
	if staff_id in StaffId:
		return (BeaconLocations[StaffId[staff_id]]+","+request.args.get("start_time", None)+","+request.args.get("end_time", None))


@app.route('/test/1')
def ping_server_0():
	end_timestamp = int(time.time())
	start_timestamp = end_timestamp - 10

	temp_string = "http://"+ip_address+"5000/extractbeacon?staff_id=001&start_time="+str(start_timestamp)+"&end_time="+str(end_timestamp)
	r0 = requests.get(temp_string)
	print(r0.text)
	return (r0.text)

def ping_server_2():
	end_timestamp = int(time.time())
	start_timestamp = end_timestamp - 10

	temp_string = "http://"+ip_address+":5000/extractbeacon?staff_id=009&start_time="+str(start_timestamp)+"&end_time="+str(end_timestamp)
	r2 = requests.get(temp_string)
	print(r2.text)
	return (r2.text)


# sched_0 = BackgroundScheduler(daemon=True)
# sched_0.add_job(ping_server_0,'interval',seconds=10)
# sched_0.start()

# sched_2 = BackgroundScheduler(daemon=True)
# sched_2.add_job(ping_server_2,'interval',seconds=10)
# sched_2.start()

app.run(debug=True, host='0.0.0.0')