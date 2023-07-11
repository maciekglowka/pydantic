from collections import deque
from typing import Deque

from pydantic import VERSION
from pydantic.v1 import VERSION as V1_VERSION
from pydantic.v1 import BaseModel as V1BaseModel
from pydantic.v1 import root_validator as v1_root_validator


def test_version():
    assert V1_VERSION.startswith('1.')
    assert V1_VERSION != VERSION


def test_root_validator():
    class Model(V1BaseModel):
        v: str

        @v1_root_validator(pre=True)
        @classmethod
        def root_validator(cls, values):
            values['v'] += '-v1'
            return values

    model = Model(v='value')
    assert model.v == 'value-v1'


def test_deque_maxlen():
    class DequeTypedModel(V1BaseModel):
        field: Deque[int] = deque(maxlen=10)

    assert DequeTypedModel(field=deque(maxlen=25)).field.maxlen == 25
    assert DequeTypedModel().field.maxlen == 10

    class DequeUnTypedModel(V1BaseModel):
        field: deque = deque(maxlen=10)

    assert DequeUnTypedModel(field=deque(maxlen=25)).field.maxlen == 25
    assert DequeTypedModel().field.maxlen == 10

    class DeuqueNoDefaultModel(V1BaseModel):
        field: deque

    assert DeuqueNoDefaultModel(field=deque(maxlen=25)).field.maxlen == 25
