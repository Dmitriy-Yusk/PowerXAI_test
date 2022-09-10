from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

FIELDS_IN_METRIC_RECORD: int = 3


class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True, nullable=False)
    values = db.relationship("MetricValues", backref="metric", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f'<Metric {self.name}>'


class MetricValues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    value = db.Column(db.Float)

    def __repr__(self):
        return f'<{self.timestamp} {self.metric} {self.value}>'

    def as_dict(self):
        obj = {
            "time": self.timestamp.isoformat(),
            "name": self.metric.name,
            "value": self.value
        }
        return obj

    @staticmethod
    def transform_from_raw_string_to_dict(raw_string: str) -> {}:
        values = raw_string.split(' ')

        # data is of the form:
        #  {timestamp} {name} {value}

        if len(values) != FIELDS_IN_METRIC_RECORD:
            raise ValueError(f'Not enough info about metric value: {raw_string}')

        field_val = values[0].strip()
        if field_val.isdigit() is not True:
            raise ValueError(f'First value must contain only digits: "{field_val}"')
        timestamp = int(field_val)

        field_val = values[1].strip()
        if field_val.isalnum() is not True:
            raise ValueError(f'Second value must be string or alphanumeric: "{field_val}"')
        name = field_val

        field_val = values[2].strip()
        value = 0
        res = True
        try:
            value = float(field_val)
        except:
            raise ValueError(f'Third value must be integer or float: "{field_val}"')

        val_rec = {
            'timestamp': timestamp,
            'name': name,
            'value': value
        }

        return val_rec


