# -*- coding: utf-8 -*-

import enum


class EnumBase(enum.Enum):
    """Enumeration base-class."""

    @staticmethod
    def get_enum(value):
        if not value:
            return None

        members = [
            (member, member.value) for member in ArticlePubModel
        ]
        for member, member_value in members:
            if member_value.lower() == value.lower():
                return member
