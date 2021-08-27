"""
this only exists because https://github.com/tortoise/tortoise-orm/issues/527 is
not yet resolved much of this code is copied from tortoise source and adapted
to ease changes to native when they exist
"""

from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Type,
)

from tortoise.models import Model, MODEL
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.backends.base.executor import BaseExecutor, EXECUTOR_CACHE


class BulkCreate(Model):
    @classmethod
    async def bulk_create(
        cls: Type[MODEL],
        objects: Iterable[MODEL],
        batch_size: Optional[int] = None,
        using_db: Optional[BaseDBAsyncClient] = None,
    ) -> None:
        db = using_db or cls._choose_db(True)
        executor = db.executor_class(model=cls, db=db)

        for instance_chunk in executor._chunk(objects, batch_size):
            values_lists_all = []
            values_lists = []
            for instance in instance_chunk:
                if instance._custom_generated_pk:
                    values_lists_all.append(
                        [
                            executor.column_map[field_name](
                                getattr(instance, field_name), instance
                            )
                            for field_name in executor.regular_columns_all
                        ]
                    )
                else:
                    values_lists.append(
                        [
                            executor.column_map[field_name](
                                getattr(instance, field_name), instance
                            )
                            for field_name in executor.regular_columns
                        ]
                    )
            if values_lists_all:
                _, insert_query_all = _insert_query(executor)
                await executor.db.execute_many(insert_query_all, values_lists_all)
            if values_lists:
                insert_query, _ = _insert_query(executor)
                await executor.db.execute_many(insert_query, values_lists)

    class Meta:
        abstract = True


def _prepare_insert_statement(
    self: BaseExecutor, columns: Sequence[str], has_generated: bool = True
) -> str:
    return str(
        self.db.query_class.into(self.model._meta.basetable)
        .columns(*columns)
        .insert(*[self.parameter(i) for i in range(len(columns))])
        .ignore()
    )


def _insert_query(self: BaseExecutor) -> (str, str):
    self.regular_columns, columns = self._prepare_insert_columns()
    self.insert_query = _prepare_insert_statement(self, columns)
    self.regular_columns_all = self.regular_columns
    self.insert_query_all = self.insert_query
    if self.model._meta.generated_db_fields:
        self.regular_columns_all, columns_all = self._prepare_insert_columns(
            include_generated=True
        )
        self.insert_query_all = _prepare_insert_statement(self, columns_all, has_generated=False)

    self.column_map: Dict[str, Callable[[Any, Any], Any]] = {}
    for column in self.regular_columns_all:
        field_object = self.model._meta.fields_map[column]
        if field_object.__class__ in self.TO_DB_OVERRIDE:
            self.column_map[column] = partial(
                self.TO_DB_OVERRIDE[field_object.__class__], field_object
            )
        else:
            self.column_map[column] = field_object.to_db_value

    table = self.model._meta.basetable
    self.delete_query = str(
        self.model._meta.basequery.where(
            table[self.model._meta.db_pk_column] == self.parameter(0)
        ).delete()
    )
    self.update_cache: Dict[str, str] = {}
    return self.insert_query, self.insert_query_all
