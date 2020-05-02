import contextlib

import aionursery

@contextlib.asynccontextmanager
async def create_handy_nursery() -> aionursery.Nursery:
    try:
        async with aionursery.Nursery() as nursery:
            yield nursery
    except aionursery.MultiError as e:
        if len(e.exceptions) == 1:
            # suppress exception chaining
            # https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement
            raise e.exceptions[0] from None
        raise
