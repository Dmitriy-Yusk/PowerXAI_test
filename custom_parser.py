from marshmallow import Schema, fields
from webargs.flaskparser import FlaskParser
from models import MetricValues


def _metric_values_to_json(metrics_data: str):
    records = metrics_data.splitlines()
    if len(records) < 1:
        raise ValueError(f'No data provided: {metrics_data}')

    transformed_data = []
    for rec in records:
        if rec.strip() == '':
            continue

        transformed_obj = MetricValues.transform_from_raw_string_to_dict(rec)
        transformed_data.append(transformed_obj)

    return transformed_data


class CustomFlaskParser(FlaskParser):
    def pre_load(self, location_data, *, schema, req, location):
        if location in ("data"):
            return _metric_values_to_json(location_data.decode('utf-8'))
        return location_data


parser = CustomFlaskParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs


@parser.location_loader("data")
def load_data(request, schema):
    return request.data


class MetricValueSchema(Schema):
    timestamp = fields.Int()
    name = fields.Str()
    value = fields.Float()


get_data_args = {
    "from": fields.Str(required=True),
    "to": fields.Str(required=True)
}
