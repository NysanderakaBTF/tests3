import pytest

from db_service import DBService
from models import Question

def test_db_get_questions():
    get_all = DBService.get_all_questions()

    assert isinstance(get_all, list)
    if (len(get_all) > 0):
        assert isinstance(get_all[0], Question)



