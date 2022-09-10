from models import db, Metric, MetricValues
from datetime import datetime


def get_metric_values_by_date(date_from: datetime, date_to: datetime) -> [{}]:
    ret = []

    values = MetricValues.query.filter(MetricValues.timestamp >= date_from, MetricValues.timestamp <= date_to).all()

    for val in values:
        val_obj = val.as_dict()
        ret.append(val_obj)

    return ret


def bulk_save_metric_values(data: [{}]):
    for metric_val in data:
        timestamp = datetime.fromtimestamp(metric_val["timestamp"])
        name = metric_val["name"]
        value = metric_val["value"]

        metric = Metric.query.filter_by(name=name).first()

        m_val = MetricValues(timestamp=timestamp, metric=metric, value=value)

        db.session.add(m_val)


def create_metrics():
    m1 = Metric(name="Voltage")
    m2 = Metric(name="Current")

    db.session.add(m1)
    db.session.add(m2)

    db.session.commit()

