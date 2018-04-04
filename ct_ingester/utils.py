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
            The matching member or `None` if `value` is undefined or no member
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


def log_ingestion_of_document(
    document_name: str
):

    # Define the actual decorator. This three-tier decorator functions are
    # necessary when defining decorator functions with arguments.
    def log_ingestion_of_document_decorator(func):
        # Define the wrapper function.
        def wrapper(self, *args, **kwargs):

            msg = "Ingesting '{}' document"
            msg_fmt = msg.format(document_name)
            self.logger.debug(msg_fmt)

            # Simply execute the decorated method with the provided arguments
            # and return the result.
            return func(self, *args, **kwargs)

        return wrapper

    return log_ingestion_of_document_decorator
