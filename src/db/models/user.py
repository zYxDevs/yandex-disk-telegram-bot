from enum import IntEnum, unique

from sqlalchemy.sql import func

from ..db import db
from ...localization import SupportedLanguages


@unique
class UserGroup(IntEnum):
    """
    User rights group.
    """
    USER = 1
    TESTER = 2
    ADMIN = 3


class User(db.Model):
    """
    Telegram user.
    """
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    create_date = db.Column(
        db.DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )
    last_update_date = db.Column(
        db.DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    telegram_id = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        comment="Unique ID to identificate user in Telegram"
    )
    is_bot = db.Column(
        db.Boolean,
        nullable=False,
        comment="User is bot in Telegram"
    )
    language = db.Column(
        db.Enum(SupportedLanguages),
        default=SupportedLanguages.EN,
        nullable=False,
        comment="Preferred language of user"
    )
    group = db.Column(
        db.Enum(UserGroup),
        default=UserGroup.USER,
        nullable=False,
        comment="User rights group"
    )

    def __repr__(self):
        return f"<User {self.id}>"
