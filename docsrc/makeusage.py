#!/usr/bin/env python2
from lxml import etree, html
import codecs
import sys
import re
from cStringIO import StringIO
import time
import os
import textwrap


class TextBlock(object):

    def __init__(self, indent, content, break_after=0):
        self.indent = indent
        self.content = content
        self.break_after = break_after

    def __str__(self):
        content = re.sub(' +', ' ', self.content.replace('\n', ' ')).strip()
        block = ('\t'*self.indent + '') + ('\n'+'\t'*self.indent + '').join(textwrap.wrap(content, replace_whitespace=False))
        return block + '\n' * self.break_after


def html_to_text(html):
    indent_tags = 'DD',
    block_tags = 'P', 'H1', 'H2', 'DT'

    def massage(text):
        return text.encode('utf-8')

    def parse_element(e, blocklist):
        last_indent = blocklist[-1].indent
        inner =  massage(e.text) if e.text else ''
        tail = massage(e.tail) if e.tail and e.tail.strip() else ''
        if e.tag.upper() in block_tags or e.get('class') == 'block':
            blocklist.append(TextBlock(last_indent, ''))
        elif e.tag.upper() in indent_tags:
            blocklist.append(TextBlock(last_indent+1, '', 1))
        blocklist[-1].content += inner
        for c in e.iterchildren(tag=etree.Element):
            parse_element(c, blocklist)
        if (e.tag.upper() in indent_tags + block_tags or blocklist[-1].indent != last_indent):
            break_after = blocklist[-1].break_after
            blocklist.append(TextBlock(last_indent, tail, break_after))
        else:
            blocklist[-1].content += tail

    parser = etree.HTMLParser(encoding='utf-8')
    doc = etree.parse(StringIO(html), parser)
    docroot = doc.getroot()
    blocklist = [TextBlock(0, '')]
    parse_element(docroot, blocklist)
    return '\n'.join(str(block) for block in blocklist[1:] if block.content)

usage_html = open('options.html', mode='r').read()

# output usage
with open('usage.txt', 'w') as textfile:
    textfile.write(html_to_text(usage_html))
