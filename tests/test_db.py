import asyncio

import pytest

from db_service import DBService
from models.models import Question, init


@pytest.fixture(autouse=True, scope='function')
def execute_before_any_test():
    print("Executing before any test")
    asyncio.run(init())


@pytest.mark.asyncio
async def test_db_get_questions():
    get_all = await DBService.get_all_questions()
    print(get_all)


    assert isinstance(get_all, list)
    if (len(get_all) > 0):
        assert isinstance(get_all[0], Question)



