from datetime import datetime
from decimal import Decimal
from collections import defaultdict


import config


class Engine:
    def __init__(self) -> None:
        self._mean = defaultdict(Decimal)
        self._count = defaultdict(Decimal)
        self._recent_values = defaultdict(lambda: defaultdict(Decimal))
        self._recent_limit = 10

    def get_mean(self, name: str) -> Decimal:
        """
        Gets mean value for given instrument name
        :param name: instrument name
        :return: Mean value for instrument
        """
        return self._mean[name]

    def show_mean_for_all(self) -> None:
        """Shows current state for all instruments"""
        for name, mean in self._mean.items():
            if name == config.INSTRUMENT3:
                print(f'Max for {name}: {mean}')
            else:
                print(f'Mean for {name}: {mean} counted: {self._count[name]}')

        for name, latest in self._recent_values.items():
            count = len(latest.values())
            mean = sum(latest.values()) / count
            print(f'Mean for {name} from last {count} records: {mean}')

    def add(self, name: str, date: datetime, value: Decimal):
        """
        Adds record to engine register
        :param name: insrument name
        :param date: date of the record
        :param value: Decimal value of the record
        """
        self._dispatch(name, date, value)

    def _dispatch(self, name: str, date: datetime, value: Decimal):
        """
        Dispatch to proper method based on the instrument name
        :param name: insrument name
        :param date: date of the record
        :param value: Decimal value of the record
        """
        match name:
            case config.INSTRUMENT1:
                self._calculate_mean(name, value)
            case config.INSTRUMENT2:
                self._add_instrument2(name, date, value)
            case config.INSTRUMENT3:
                self._add_instrument3(name, value)
            case _:
                self._add_to_recent(name, date, value)

    def _add_instrument2(self, name: str, date: datetime, value: Decimal):
        """
        Adds to mean for instrument2
        :param name: insrument name
        :param date: date of the record
        :param value: Decimal value of the record
        """
        if date.year == config.INSTRUMENT2_YEAR and date.month == config.INSTRUMENT2_MONTH:
            self._calculate_mean(name, value)

    def _add_instrument3(self, name: str, value: Decimal):
        """
        Sets max value from comparison of registered one and new value
        :param name: insrument name
        :param value: Decimal value of the record
        """
        self._mean[name] = max(value, self._mean[name])

    def _add_to_recent(self, name: str, date: datetime, value: Decimal):
        """
        Adds to recent values when the timestamp is higher or values count limit was not exceeded
        :param name: insrument name
        :param date: date of the record
        :param value: Decimal value of the record
        """
        lowest = sorted(self._recent_values[name].keys())[0] if self._recent_values[name] else 0
        if (timestamp := date.timestamp()) > lowest:
            self._recent_values[name][timestamp] = value
            if len(self._recent_values[name]) > self._recent_limit:
                self._recent_values[name].pop(lowest)

    def _calculate_mean(self, name: str, value: Decimal):
        """
        Calculates mean based on previous value and count
        :param name: insrument name
        :param value: Decimal value of the record
        """
        self._count[name] += 1
        self._mean[name] = self._mean[name] + (value - self._mean[name]) / self._count[name]
