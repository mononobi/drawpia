# -*- coding: utf-8 -*-

import random

from drawpia.extractor import Extractor, Entry


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

        if not restricted_level:
            return False

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

        if not optional_level:
            return False

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
        self._total_groups = None
        self._group_size = None

    def _validate(self, group_size):
        """
        validates the drawing parameters.

        :param str group_size: group size.
        """

        if not group_size or not group_size.isdigit():
            raise ValueError('Group size is invalid.')

        group_size = int(group_size)
        if group_size <= 0:
            raise ValueError('Group size must be a positive integer.')

        if self._extractor.count < group_size:
            raise ValueError(f'Group size can not be bigger than entries '
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

        self._group_size = group_size
        self._total_groups = total_groups

    def _confirm(self):
        """
        confirms the drawing.
        """

        group_size = input('Please enter the group size:\n')
        self._validate(group_size)

        print('*' * 200)
        print('Total Entry Count:')
        print(self._extractor.count)
        print('*' * 100)
        print('Group Size:')
        print(self._group_size)
        print('*' * 100)
        print('Number Of Groups:')
        print(self._total_groups)

    def _select(self, entries, group, picked,
                is_restricted=False, is_optional=False):
        """
        selects a random entry from the list of entries and returns it.

        it returns None if no entry can be selected and the entries list is exhausted.

        :param list[Entry] entries: list of entries to pick from.
        :param Group group: the corresponding group to pick an entry for it.
        :param list[Entry] picked: global list of already picked entries.

        :param bool is_restricted: specifies that the provided group should not have
                                   any other entry with the same restricted level as
                                   the selected entry.

        :param bool is_optional: specifies that the provided group should not have
                                 any other entry with the same optional level as
                                 the selected entry.

        :rtype: Entry
        """

        reduced_entries = list(entries)
        if not reduced_entries:
            return None

        selected = random.choice(reduced_entries)
        if (is_restricted and group.has_restricted(selected.restricted_level)) or \
                (is_optional and group.has_optional(selected.optional_level)):
            reduced_entries.remove(selected)
            return self._select(reduced_entries, group, picked,
                                is_restricted, is_optional)

        group.add(selected)
        picked.append(selected)
        return selected

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
                sources = list(set(items).difference(set(picked)))
                for group in groups:
                    if not sources:
                        break

                    if group.is_full or group.has_restricted(level):
                        continue

                    # we should prevent entries with the same optional
                    # level to be put in the same group.
                    selected = self._select(sources, group, picked,
                                            is_optional=True)
                    if not selected:
                        continue

                    sources.remove(selected)

        if self._extractor.has_optional:
            for level, items in self._extractor.optional_entries.items():
                sources = list(set(items).difference(set(picked)))
                for group in groups:
                    if not sources:
                        break

                    if group.is_full or group.has_optional(level):
                        continue

                    # we should prevent entries with the same restricted
                    # level to be put in the same group.
                    selected = self._select(sources, group, picked,
                                            is_restricted=True)
                    if not selected:
                        continue

                    sources.remove(selected)

        # we should first enforce that no entries with the same optional level put
        # in the same group. but if all groups have been processed 10 times and
        # there were still some groups without enough entries, we lift the optional
        # level enforcement to be able to fill all groups.
        tried_optional = 0
        sources = list(set(self._extractor.entries).difference(set(picked)))
        while len(picked) < self._extractor.count:
            for group in groups:
                if not sources:
                    break

                if group.is_full:
                    continue

                selected = self._select(sources, group, picked,
                                        is_restricted=True,
                                        is_optional=tried_optional < 10)
                if not selected:
                    continue

                sources.remove(selected)

            tried_optional += 1

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
        print('Draw Results:')
        for item in groups:
            print('*' * 100)
            print(str(item))
