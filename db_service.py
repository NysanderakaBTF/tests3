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