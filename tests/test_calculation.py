from datetime import datetime
from decimal import Decimal

import pytest

import config
from src.core.calculation import Engine


@pytest.fixture(scope='function')
def engine() -> Engine:
    e = Engine()
    return e


@pytest.fixture(scope='function')
def engine_with_full_recent(engine) -> Engine:
    name = 'instrument4'
    for i in range(1, 11):
        date = datetime(year=2015, month=1, day=i)
        engine.add(name, date, Decimal(str(i)))
    return engine


@pytest.mark.parametrize(
    'name,date,value,expected',
    [
        (config.INSTRUMENT1, datetime(year=2014, month=2, day=1), Decimal('3'), Decimal('3')),
        (config.INSTRUMENT1, datetime(year=2014, month=1, day=5), Decimal('1.4'), Decimal('1.4')),
        (config.INSTRUMENT1, datetime(year=2012, month=5, day=29), Decimal('5.8'), Decimal('5.8')),
        (config.INSTRUMENT1, datetime(year=2013, month=1, day=11), Decimal('0'), Decimal('0')),
        (config.INSTRUMENT1, datetime(year=2015, month=11, day=15), Decimal('7'), Decimal('7')),
    ],
)
def test_add_instrument1_to_empty_engine(engine, name: str, date: datetime, value: Decimal, expected: Decimal):
    engine.add(name, date, value)
    assert engine.get_mean(name) == expected


@pytest.mark.parametrize(
    'name,date,value,expected',
    [
        (config.INSTRUMENT1, datetime(year=2014, month=2, day=1), Decimal('3'), Decimal('2')),
        (config.INSTRUMENT1, datetime(year=2014, month=1, day=5), Decimal('1'), Decimal('1')),
        (config.INSTRUMENT1, datetime(year=2015, month=11, day=15), Decimal('7'), Decimal('4')),
    ],
)
def test_add_instrument1_to_non_empty_engine(engine, name: str, date: datetime, value: Decimal, expected: Decimal):
    engine.add(name, date, Decimal(1))

    engine.add(name, date, value)
    assert engine.get_mean(name) == expected


@pytest.mark.parametrize(
    'name,date,value,expected',
    [
        (config.INSTRUMENT2, datetime(year=2014, month=11, day=1), Decimal('3'), Decimal('2')),
        (config.INSTRUMENT2, datetime(year=2014, month=1, day=5), Decimal('1'), Decimal('0')),
        (config.INSTRUMENT2, datetime(year=2015, month=11, day=15), Decimal('7'), Decimal('0')),
    ],
)
def test_add_instrument2_to_non_empty_engine(engine, name: str, date: datetime, value: Decimal, expected: Decimal):
    engine.add(name, date, Decimal(1))

    engine.add(name, date, value)
    assert engine.get_mean(name) == expected


@pytest.mark.parametrize(
    'name,date,value,expected',
    [
        (config.INSTRUMENT3, datetime(year=2014, month=11, day=1), Decimal('3'), Decimal('10')),
        (config.INSTRUMENT3, datetime(year=2014, month=1, day=5), Decimal('11'), Decimal('11')),
        (config.INSTRUMENT3, datetime(year=2015, month=11, day=15), Decimal('0'), Decimal('10')),
    ],
)
def test_add_instrument3_to_non_empty_engine(engine, name: str, date: datetime, value: Decimal, expected: Decimal):
    engine.add(name, date, Decimal(10))

    engine.add(name, date, value)
    assert engine.get_mean(name) == expected


@pytest.mark.parametrize(
    'name,date,value,expected',
    [
        ('instrument4', datetime(year=2015, month=11, day=30), Decimal('3'), Decimal('5.7')),
        ('instrument4', datetime(year=2014, month=1, day=5), Decimal('11'), Decimal('5.5')),
    ],
)
def test_add_other_instrument_to_engine_with_full_recent(
    engine_with_full_recent, name: str, date: datetime, value: Decimal, expected: Decimal
):
    engine_with_full_recent.add(name, date, value)
    assert engine_with_full_recent.get_mean_from_recent(name) == expected
