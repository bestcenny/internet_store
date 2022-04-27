import sqlalchemy
from sqlalchemy_serializer import SerializerMixin


from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cart'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
