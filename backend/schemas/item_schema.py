from apiflask import Schema
from apiflask.fields import Integer, String, List, Nested


class ItemSchema(Schema):
    id = Integer()
    name = String()
    image = String()


class ItemOutSchema(Schema):
        items = List(Nested(ItemSchema))