# -*- coding: utf-8 -*-

from typing import Iterable

import itertools


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


def chunk_generator(
    generator: Iterable,
    chunk_size: int
):
    """Chunks a generator into small equally sized chunks generated lazily.

    Args:
        generator (Iterable): The generator to chunk.
        chunk_size (int): The maximum size of each chunk.

    Yields:
        itertools.chain: The generator chunks.
    """

    for first in generator:
        yield itertools.chain(
            [first],
            itertools.islice(generator, chunk_size - 1),
        )
