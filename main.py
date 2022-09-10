from flask import Flask
from flask import jsonify
from dateutil import parser as dt_parser

from custom_parser import parser, use_args, MetricValueSchema, get_data_args
from models import db
from db_layer import create_metrics, bulk_save_metric_values, get_metric_values_by_date


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.post("/data")
# @use_args(MetricValueSchema(many=True), location='data', error_status_code=400)
def post_data():
    false_reponse = {"success": False}

    try:
        data = parser.parse(MetricValueSchema(many=True), location='data')
    except:
        return jsonify(false_reponse), 400

    try:
        with db.session.begin():
            bulk_save_metric_values(data)
    except:
        return jsonify(false_reponse), 500

    return jsonify({"success": True}), 200


@app.get("/data")
# @use_args(get_data_args, location='query', error_status_code=400)
def get_data():
    false_reponse = {"success": False}

    try:
        args = parser.parse(get_data_args, location='query')
    except:
        return jsonify(false_reponse), 400

    try:
        from_dt = dt_parser.isoparse(args["from"])
        to_dt = dt_parser.isoparse(args["to"])

        ret = get_metric_values_by_date(from_dt, to_dt)
    except:
        return jsonify(false_reponse), 500

    return jsonify(ret), 200


def init_app(app, db):
    app.app_context().push()
    db.init_app(app)

    db.create_all()

    create_metrics()


if __name__ == "__main__":
    init_app(app, db)

    app.run()
