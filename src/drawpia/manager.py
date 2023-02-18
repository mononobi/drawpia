# -*- coding: utf-8 -*-

import random

from drawpia.extractor import Extractor, Entry
from drawpia.settings import GROUP_SIZE


class Group:
    """
    group class.
    """

    def __init__(self,  name , size):
        """
        initializes an instance of Group.

        :param str name: group name.
        :param int size: group size.
        """

        super().__init__()

        self._name = name
        self._size = size
        self._entries = []

    def __str__(self):
        """
        gets the string representation of this group.

        :rtype: str
        """

        name = f'[{self._name}]:\n\n'
        entries = '\n'.join(str(item) for item in self._entries)
        return f'{name}{entries}'

    def add(self, entry):
        """
        adds the entry into the group.

        :param Entry entry: entry to be added to the group.
        """

        if self.is_full:
            raise ValueError(f'Group [{self._name}] is full with [{self._size}] entries.')

        if entry in self._entries:
            raise ValueError(f'Entry {entry} is already added to group [{self._name}]')

        self._entries.append(entry)

    def has_restricted(self, restricted_level):
        """
        gets a value indicating that an entry with the given restricted level exists in group.

        :param str restricted_level: restricted level to check for existence.

        :rtype: bool
        """

        for item in self._entries:
            if item.restricted_level == restricted_level:
                return True

        return False

    def has_optional(self, optional_level):
        """
        gets a value indicating that an entry with the given optional level exists in group.

        :param str optional_level: optional level to check for existence.

        :rtype: bool
        """

        for item in self._entries:
            if item.optional_level == optional_level:
                return True

        return False

    @property
    def entries(self):
        """
        gets the entries of this group.

        :rtype: list[Entry]
        """

        return list(self._entries)

    @property
    def count(self):
        """
        gets the entry count of this group.

        :rtype: int
        """

        return len(self._entries)

    @property
    def size(self):
        """
        gets the size this group.

        :rtype: int
        """

        return self._size

    @property
    def name(self):
        """
        gets the name this group.

        :rtype: str
        """

        return self._name

    @property
    def is_full(self):
        """
        gets a value indicating that this group is full.

        :rtype: bool
        """

        return len(self._entries) >= self._size


class Manager:
    """
    manager class.

    it performs the whole drawing process.
    """

    def __init__(self):
        """
        initializes an instance of Manager.
        """

        super().__init__()

        self._extractor = Extractor()
        self._total_groups, self._group_size = self._validate()

    def _validate(self):
        """
        validates the drawing parameters and returns the validated total groups and group size.

        :returns: int total_groups, int group_size
        :rtype: int, int
        """

        group_size = int(GROUP_SIZE)
        if group_size != GROUP_SIZE:
            raise ValueError('"GROUP_SIZE" must be an integer.')

        if group_size <= 0:
            raise ValueError('"GROUP_SIZE" must be a positive number.')

        if self._extractor.count < group_size:
            raise ValueError(f'"GROUP_SIZE" can not be bigger than entries '
                             f'count which is [{self._extractor.count}]')

        if self._extractor.count % group_size != 0:
            raise ValueError(f'Entries count is [{self._extractor.count}] which is not '
                             f'dividable by group size [{group_size}].')

        total_groups = int(self._extractor.count / group_size)
        if self._extractor.has_restricted:
            for level, count in self._extractor.restricted_count.items():
                if count > total_groups:
                    raise ValueError(f'There are [{count}] entries with restricted '
                                     f'level [{level}], but there would be only '
                                     f'[{total_groups}] groups in total. entries with '
                                     f'the same restricted level can not be put in '
                                     f'the same group.')

        return total_groups, group_size

    def _confirm(self):
        """
        confirms the drawing.
        """

        print('*' * 200)
        print('Total Entry Count:')
        print(self._extractor.count)
        print('*' * 100)
        print('Group Size:')
        print(self._group_size)
        print('*' * 100)
        print('Number Of Groups:')
        print(self._total_groups)

    def _draw(self):
        """
        performs a draw and gets the groups list.

        :rtype: list[Group]
        """

        picked = []
        groups = []
        for i in range(self._total_groups):
            new_group = Group(f'Group {i + 1}', self._group_size)
            groups.append(new_group)

        if self._extractor.has_restricted:
            for level, items in self._extractor.restricted_entries.items():
                sources = list(items)
                for group in groups:
                    if len(sources) <= 0:
                        break

                    if group.is_full or group.has_restricted(level):
                        continue

                    selected = random.choice(sources)
                    group.add(selected)
                    picked.append(selected)
                    sources.remove(selected)

        if self._extractor.has_optional:
            for level, items in self._extractor.optional_entries.items():
                sources = list(items)
                for group in groups:
                    if len(sources) <= 0:
                        break

                    if group.is_full or group.has_optional(level):
                        continue

                    selected = random.choice(sources)
                    group.add(selected)
                    picked.append(selected)
                    sources.remove(selected)

        sources = list(self._extractor.entries)
        while len(picked) < self._extractor.count:
            for group in groups:
                if len(sources) <= 0:
                    break

                if group.is_full:
                    continue

                selected = random.choice(sources)
                group.add(selected)
                picked.append(selected)
                sources.remove(selected)

        return groups

    def perform(self):
        """
        performs a draw.
        """

        self._confirm()
        groups = self._draw()
        print('*' * 200)
        print('Performing The Draw...')
        print('*' * 200)
        print('Drawing Results:')
        for item in groups:
            print('*' * 100)
            print(str(item))
