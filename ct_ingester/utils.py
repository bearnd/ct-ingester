# -*- coding: utf-8 -*-


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
