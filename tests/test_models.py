from unittest import TestCase
from models import MetricValues

class TestMetricValues(TestCase):
    def test_transform_from_raw_string_to_dict(self):
        test_data = "1649941817 Voltage 1.34"
        obj = {}
        try:
            obj = MetricValues.transform_from_raw_string_to_dict(test_data)
        except:
            self.fail()
        if "name" not in obj or obj["name"] != "Voltage":
            self.fail()

        test_data = "Voltage 1649941817 1.34"
        obj = {}
        try:
            obj = MetricValues.transform_from_raw_string_to_dict(test_data)
        except:
            pass
        if "name" in obj:
            self.fail()

        test_data = "1649941817 Voltage"
        obj = {}
        try:
            obj = MetricValues.transform_from_raw_string_to_dict(test_data)
        except:
            pass
        if "name" in obj:
            self.fail()
