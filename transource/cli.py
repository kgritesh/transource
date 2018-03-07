#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import click
import logging

from transource.translator import SourceTranslator


def get_version():
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')) as version_file:
        return version_file.read().strip()


@click.command()
@click.argument('src')
@click.argument('dest')
@click.option('--src-lang', default='auto', help='Source language for comments')
@click.option('--dest-lang', default='en', help='Dest language for comments')
@click.option('-e', '--encoding', default='utf-8', help='Source code encoding')
@click.option('-a', '--auto-detect',is_flag=True, default=True, help='Auto Detect File Encoding')
@click.option('-t', '--threshold', type=click.FLOAT, help='Condifence threshold while auto detecting encoding')
@click.version_option(version=get_version(), prog_name="transource")
def cli(src, dest, src_lang=None, dest_lang=None, encoding=None, auto_detect=None, threshold=None):
    """
    A cli tool to translate comments in source code from one language to another
    """
    logging.basicConfig(level=logging.INFO)
    if os.path.isfile(src):
        translator = SourceTranslator(src, dest, src_lang, dest_lang, encoding, auto_detect, threshold)
        translator.run()


if __name__ == '__main__':
    cli()
