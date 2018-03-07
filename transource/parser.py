# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import codecs
import re

import six


class CodeBlock(object):
    def __init__(self, is_comment, is_multiline):
        self.is_multiline = is_multiline
        self.is_comment = is_comment
        self.__lines = []

    def update(self, lines):
        self.__lines = lines

    def append(self, line):
        self.__lines.append(line)

    def reset(self):
        self.__lines = []

    def __iter__(self):
        for line in self.__lines:
            yield line

    def __str__(self):
        return '\n'.join(self) + '\n'

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return bool(self.__lines)


class CommentParser(six.with_metaclass(abc.ABCMeta)):

    def __init__(self, src, encoding):
        self.src = src
        self.encoding = encoding

    def read_lines(self):
        with codecs.open(self.src, 'r', encoding=self.encoding, errors='replace') as fl:
            for line in fl.readlines():
                yield line

    @abc.abstractmethod
    def read_blocks(self):
        pass

    @abc.abstractmethod
    def add_comment(self, block):
        pass

    @classmethod
    def get(cls, src, *args, **kwargs):
        return HashCommentParser(src, *args, **kwargs)


class HashCommentParser(CommentParser):
    HASH_COMMENT = re.compile(r'(\s*)#(\s*.+)$', re.U & re.M)

    def read_blocks(self):
        is_comment_block = False
        current_block = CodeBlock(False, True)
        for line in self.read_lines():
            line = line.rstrip()
            if not line.strip():
                current_block.append(line)
                continue

            match = self.HASH_COMMENT.match(line)
            if match:
                if not is_comment_block:
                    yield current_block
                    is_comment_block = True
                    current_block = CodeBlock(True, False)

                current_block.append(''.join(match.groups()))
            else:
                if is_comment_block:
                    yield current_block
                    is_comment_block = False
                    current_block = CodeBlock(False, True)
                current_block.append(line)

        yield current_block

    def add_comment(self, block):
        block.update(['#{}'.format(b) if b.strip() else b for b in block])
