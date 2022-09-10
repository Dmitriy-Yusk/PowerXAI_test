from main import app, init_app
from models import db
from flask import json

app.config.update(SERVER_NAME="127.0.0.1:5000", DEBUG=True)

init_app(app, db)


def test_post_data(data, status_code):
    with app.test_client() as c:
        # data = '1649941817 Voltage 1.34'
        print('Run test:\npost /data with = {}'.format(data))

        rv = c.post(
            '/data',
            data=data,
            content_type='text/plain'
        )

        json_data = rv.get_json()

        print('post /data status code = {}'.format(rv.status_code))
        print('----------------------------------------------------')
        assert rv.status_code == status_code


def test_get_data(data, status_code):
    with app.test_client() as c:
        print('Run test:\nget /data with = {}'.format(data))
        rv = c.get(
            '/data?' + data
        )

        json_data = rv.get_json()

        print('get /data status code = {}'.format(rv.status_code))
        print(json_data)
        print('----------------------------------------------------')
        assert rv.status_code == status_code


if __name__ == "__main__":
    test_post_data('1649941817 Voltage 1.34', 200)
    test_post_data('Voltage 1649941817 1.34', 400)
    test_post_data('1649941817 Voltage 1.34\r\n1649941818 Voltage 1.35\r\n1649941817 Current 12.0\r\n1649941818 Current 14.0', 200)

    test_get_data('from=2022-01-01&to=2022-04-15', 200)


