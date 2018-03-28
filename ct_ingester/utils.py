# -*- coding: utf-8 -*-

import enum


class EnumBase(enum.Enum):
    """Enumeration base-class."""

    @classmethod
    def get_member(
        cls,
        value: str,
    ):
        """Returns an enumeration member with a value matching `value`.

        Args:
            value (str): The value of the member to match.

        Returns:
            The matching member of `None` if `value` is undefined or no member
                was found.
        """
        if not value:
            return None

        members = [
            (member, member.value)
            for member in cls.__members__.values()
        ]
        for member, member_value in members:
            if member_value == value:
                return member

        return None
