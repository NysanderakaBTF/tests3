import asyncio

import pytest

from db_service import DBService
from models.models import Question, init


@pytest.fixture(autouse=True, scope='session')
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


@pytest.mark.asyncio
async def test_db_create_question():
    question = await DBService.create_question(
        question="Alla?",
        answer="Who",
    )

    assert isinstance(question, Question)
    assert question.question == "Alla?"
    assert question.answer == "Who"
    assert question.id is not None


@pytest.mark.asyncio
async def test_db_update_question():
    question = await DBService.create_question(
        question="Alla?",
        answer="Who",
    )

    updated_question = await DBService.update_question(
        id=question.id,
        question="Alla?",
        answer="Alla!!",
    )

    assert isinstance(updated_question, Question)
    assert updated_question.question == "Alla?"
    assert updated_question.answer == "Alla!!"
    assert updated_question.id == question.id


@pytest.mark.asyncio
async def test_db_delete_question():
    question = await DBService.create_question(
        question="Alla?",
        answer="Who7",
    )

    deleted_question = await DBService.delete_question(id=question.id)

    assert deleted_question is None


@pytest.mark.asyncio
async def test_get_random_question():
    question = await DBService.get_random_question()

    assert isinstance(question, Question)
    assert question.question is not None
    assert question.answer is not None
    assert question.id is not None
