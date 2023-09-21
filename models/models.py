import asyncio

from tortoise import Model, fields, Tortoise


class Question(Model):
    id = fields.IntField(pk=True)
    question = fields.TextField()
    answer = fields.TextField()

    def __str__(self):
        return self.question


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models.models']}
    )
    await Tortoise.generate_schemas()
