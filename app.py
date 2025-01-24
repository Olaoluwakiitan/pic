from datetime import datetime
from flask import Flask, request, json, redirect, jsonify, make_response
from models import db,CalendarModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pic_event.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

default_time_format = "%Y-%m-%dT%H:%M:%S"
default_start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
default_to_time = datetime.now()

@app.before_request
def create_table():
    db.create_all()


@app.route('/')
def run():
    event_ = CalendarModel.query.all()
    if event_ is None:
        return make_response(jsonify({"message": f" No calendar event not found"}), 200)
    if isinstance(event_, list):
        return jsonify([row.get_event() for row in event_])
    else:
        return jsonify(event_.get_event())

@app.route('/events', methods=['POST'])
def events():
    if request.method == 'POST':
        data = request.get_json()
        id_ = data['id']
        time_ = data['time']
        description_ = data['description']
        if id_ and time_ and description_:
            pic_event = CalendarModel(id_=id_, time_=time_, description=description_)
            db.session.add(pic_event)
            db.session.commit()
            return redirect('/')

        else:
            return make_response(jsonify({"message": "Invalid input"}), 404)

@app.route("/events/", methods=["GET"])
def retrieve_event():
    try:
        id_ =request.args.get("ID")
        result_format = request.args.get("datetime_format") if "datetime_format" in request.args else default_time_format
        event_ = CalendarModel.query.filter_by(event_id=id_).first()
        if event_ is None:
            return make_response(jsonify({"message": f" ID {id_} calendar event not found"}), 200)
        if isinstance(event_, list):
            return jsonify([row.get_event() for row in event_])
        else:
            return jsonify(event_.get_event())
    except:
        return make_response(jsonify({"message": "Invalid input"}), 404)

@app.route("/events", methods=["GET"])
def retrieve_events():
    try:
            result_format = request.args.get("datetime_format") if "datetime_format" in request.args else default_time_format
            from_time = request.args.get("from_time") if "from_time" in request.args else default_start_time
            to_time = request.args.get("to_time") if "to_time" in request.args  else default_to_time
            event_start_time = datetime.strptime(from_time, result_format)
            event_stop_time = datetime.strptime(to_time, result_format)
            events_ = CalendarModel.query.filter(CalendarModel.event_time.between(event_start_time, event_stop_time)).all()
            if events_ is None:
                return make_response(jsonify({"message": f" No calendar event not found"}), 200)
            if isinstance(events_, list):
                return jsonify([row.get_event() for row in events_])
            else:
                return jsonify(events_.get_events())
    except:
        return make_response(jsonify({"message": "Invalid Date input"}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
