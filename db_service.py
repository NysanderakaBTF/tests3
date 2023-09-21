import random

from models.models import Question


class DBService:
    def __init__(self):
        ...

    @classmethod
    async def get_all_questions(cls):
        return await Question.filter().all()

    @classmethod
    async def create_question(cls, question, answer):
        q = Question(question=question, answer=answer)
        await q.save()
        return q

    @classmethod
    async def update_question(cls, id, question, answer):
        q = await Question.get(id=id)
        q.question = question
        q.answer = answer
        await q.save()
        return q

    @classmethod
    async def delete_question(cls, id):
        await Question.filter(id=id).delete()
        return None

    @classmethod
    async def get_random_question(cls):
        q = await Question.filter().all()
        return q[random.randint(0, len(q))]

