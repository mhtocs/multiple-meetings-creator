from api.meetings.payload import Session
import json
import pytest


class TestPayloads:

    def test_empty_schema(self):
        with pytest.raises(KeyError):
            Session.from_json('{}')

    def test_schema_json(self):
        orig_sess = dict(topic="A new topic",
                         presenter="Arvind",
                         agenda="Test agenda",
                         participants=[],
                         start_time_in_sec=0,
                         duration="1234",
                         timezone="Asia")

        sess_js = Session.from_json(json.dumps(orig_sess))

        morped_sess = orig_sess.copy()
        del morped_sess['start_time_in_sec']
        morped_sess['startTime'] = 'Jan 01, 1970 05:30 AM'

        assert sess_js.to_dict() == morped_sess
