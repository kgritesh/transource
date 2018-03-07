# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import codecs

import chardet
import logging

import sys
from googletrans import Translator

from transource.parser import CommentParser


def guess_encoding(src, threshold):
    with open(src, 'rb') as src_file:
        guess = chardet.detect(src_file.read())

    confidence = float(guess['confidence'])
    if confidence < threshold:
        return None, confidence

    else:
        return guess['encoding'], confidence


class SourceTranslator(object):
    DEFAULT_ENCODING = 'utf-8'

    DEFAULT_THRESHOLD = 0.8

    def __init__(self, src, dest, src_lang='auto', dest_lang='en', encoding=None, autodetect=False, threshold=None):
        self.translator = Translator()
        self.logger = logging.getLogger(__name__)
        self.src = src
        self.dest = dest
        self.set_encoding(encoding, autodetect, threshold)
        self.src_lang = src_lang
        self.dest_lang = dest_lang
        self.comment_parser = CommentParser.get(self.src, encoding=self.encoding)
        self.logger.info('Translating from {} to {}'.format(src_lang, dest_lang))

    def set_encoding(self, encoding=None, autodetect=False, threshold=None):
        if autodetect:
            encoding, confidence = guess_encoding(self.src, threshold or self.DEFAULT_THRESHOLD)
            if not encoding:
                msg = 'Unable to detect encoding for the provided source file: {}. Confidence is too low: {}'.format(
                    self.src, confidence
                )                                 
                self.logger.error(msg)
                raise Exception(msg)

            self.logger.debug('Detected encoding for the provided source file: {} to {}'.format(
                self.src, encoding
            ))
        else:
            encoding = encoding or self.DEFAULT_ENCODING

        self.encoding = encoding

    def translate_block(self, block):
        block_lines = []
        prefix = []
        for line in block:
            stripped_line = line.strip()
            block_lines.append(stripped_line)
            prefix.append(len(line) - len(stripped_line))

        translations = self.translator.translate(block_lines, dest=self.dest_lang, src=self.src_lang)
        block.update(['{}{}'.format(' ' * prefix[i], t.text.strip()) for i, t in enumerate(translations)])
        self.comment_parser.add_comment(block)
        return block

    def run(self):
        with codecs.open(self.dest, 'w', encoding=self.encoding, errors='replace') as output:
            for block in self.comment_parser.read_blocks():
                if not block:
                    continue
                if block.is_comment:
                    block = self.translate_block(block)

                output.write(str(block))
