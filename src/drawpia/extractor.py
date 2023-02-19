# -*- coding: utf-8 -*-

import os

import drawpia

from drawpia.settings import SEP


class Entry:
    """
    entry class.

    it represents an entry participating in drawing.
    """

    def __init__(self, name, row, restricted_level=None, optional_level=None):
        """
        initializes an instance of Entry.

        :param str name: name of the entry.
        :param int row: the row number of this entry.

        :param str restricted_level: a value indicating the restricted level of this entry.
                                     entries which have the same restricted level, would
                                     not be put in the same group.

        :param str optional_level: a value indicating the optional level of this entry.
                                   entries which have the same optional level, would
                                   not be put in the same group unless it's not possible.
        """

        super().__init__()

        self._name = name
        self._row = row
        self._restricted_level = restricted_level
        self._optional_level = optional_level

    def __hash__(self):
        """
        gets the hash of this entry.

        :rtype: int
        """

        return hash((self._row, self._name, self._restricted_level, self._optional_level))

    def __eq__(self, other):
        """
        implements the equality operator.

        :param object other: the other object to check equality with.

        :rtype: bool
        """

        if not isinstance(other, Entry):
            return False

        return hash(other) == hash(self)

    def __ne__(self, other):
        """
        implements the not equality operator.

        :param object other: the other object to check not equality with.

        :rtype: bool
        """

        return not other == self

    @property
    def name(self):
        """
        gets the name of this entry.

        :rtype: str
        """

        return self._name

    @property
    def row(self):
        """
        gets the row number of this entry.

        :rtype: str
        """

        return self._row

    @property
    def restricted_level(self):
        """
        gets the restricted level of this entry.

        :rtype: str
        """

        return self._restricted_level

    @property
    def optional_level(self):
        """
        gets the optional level of this entry.

        :rtype: str
        """

        return self._optional_level

    def __str__(self):
        """
        gets the string representation of this entry.

        :rtype: str
        """

        if self._restricted_level and self._optional_level:
            return f'[{self._row}]-[{self._name}]-' \
                   f'[{self._restricted_level}]-[{self._optional_level}]'

        elif self._restricted_level:
            return f'[{self._row}]-[{self._name}]-[{self._restricted_level}]'

        elif self._optional_level:
            return f'[{self._row}]-[{self._name}]-[{self._optional_level}]'

        return f'[{self._row}]-[{self._name}]'

    def __repr__(self):
        """
        gets the string representation of this entry.

        :rtype: str
        """

        return str(self)


class Extractor:
    """
    extractor class.

    it reads the entries from `entries.txt` file and populates the available information.
    """

    def __init__(self):
        """
        initializes an instance of Extractor.
        """

        super().__init__()

        root = os.path.dirname(drawpia.__file__)
        file_path = os.path.join(root, 'files', 'entries.txt')
        self._entries, self._restricted_entries, self._optional_entries, \
            self._restricted_count, self._optional_count = self._extract_entries(file_path)

    def _extract_entries(self, file_path):
        """
        extracts entries from given file.

        :param str file_path: file path to extract entries from.

        :returns: a tuple containing a list of entries, a dict of restricted levels
                  and their related entries, a dict of optional levels and their
                  related entries, a dict of restricted levels and their entry count
                  and a dict of optional levels and their entry count

        :rtype: tuple[list[Entry], dict, dict, dict, dict]
        """

        if not os.path.isfile(file_path):
            raise ValueError(f'The required file [{file_path}] does not exist.')

        # keeps a list of all entries.
        entries = []
        # keeps a dict of different entries based on their restricted levels.
        restricted_entries = {}
        # keeps a dict of different entries based on their optional levels.
        optional_entries = {}
        # keeps a dict of different restricted levels and their entry count.
        restricted_count = {}
        # keeps a dict of different optional levels and their entry count.
        optional_count = {}

        with open(file_path) as file:
            lines = file.readlines()
            for index, item in enumerate(lines):
                if not item or not item.strip() or item.strip().isspace():
                    continue

                parts = item.split(SEP)
                name = None
                restricted_level = None
                optional_level = None
                if len(parts) == 3:
                    name = parts[0].strip()
                    restricted_level = parts[1].strip()
                    optional_level = parts[2].strip()

                elif len(parts) == 2:
                    name = parts[0].strip()
                    restricted_level = parts[1].strip()

                elif len(parts) == 1:
                    name = parts[0].strip()

                else:
                    ValueError(f'Invalid entry found: [{item.rstrip()}]')

                if not name or name.isspace():
                    raise ValueError(f'Invalid name found for entry: '
                                     f'[{index + 1}-{item.rstrip()}]')

                if restricted_level and not restricted_level.isspace():
                    restricted_level = restricted_level.strip()
                else:
                    restricted_level = None

                if optional_level and not optional_level.isspace():
                    optional_level = optional_level.strip()
                else:
                    optional_level = None

                entry = Entry(name, index + 1,
                              restricted_level=restricted_level,
                              optional_level=optional_level)

                entries.append(entry)

                if restricted_level:
                    restricted_items = restricted_entries.setdefault(restricted_level, [])
                    restricted_items.append(entry)

                if optional_level:
                    optional_items = optional_entries.setdefault(optional_level, [])
                    optional_items.append(entry)

        if not entries:
            raise ValueError('No valid entries found.')

        if restricted_entries:
            for level_name, items in restricted_entries.items():
                restricted_count[level_name] = len(items)

        if optional_entries:
            for level_name, items in optional_entries.items():
                optional_count[level_name] = len(items)

        return entries, restricted_entries, optional_entries, restricted_count, optional_count

    @property
    def entries(self):
        """
        gets the entries.

        :rtype: list[Entry]
        """

        return self._entries

    @property
    def restricted_entries(self):
        """
        gets the restricted levels and their entries.

        :rtype: dict
        """

        return self._restricted_entries

    @property
    def optional_entries(self):
        """
        gets the optional levels and their entries.

        :rtype: dict
        """

        return self._optional_entries

    @property
    def restricted_count(self):
        """
        gets the restricted levels and the count of their entries.

        :rtype: dict
        """

        return self._restricted_count

    @property
    def optional_count(self):
        """
        gets the optional levels and the count of their entries.

        :rtype: dict
        """

        return self._optional_count

    @property
    def count(self):
        """
        gets the entries count.

        :rtype: int
        """

        return len(self._entries)

    @property
    def has_restricted(self):
        """
        gets a value indicating that restricted level is in place.

        :rtype: bool
        """

        return len(self._restricted_count) > 0

    @property
    def has_optional(self):
        """
        gets a value indicating that optional level is in place.

        :rtype: bool
        """

        return len(self._optional_count) > 0
