# -*- encoding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2007, 2008 OpenHex SPRL. (http://openhex.com) All Rights
# Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


import os
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import lxml.etree
from nose.tools import *
from genshi.filters import Translator
from genshi.core import PI
from genshi.template.eval import UndefinedError

from relatorio.templates.opendocument import Template, GENSHI_EXPR,\
    GENSHI_URI, RELATORIO_URI

OO_TABLE_NS = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"


def pseudo_gettext(string):
    catalog = {'Mes collègues sont:': 'My colleagues are:',
               'Bonjour,': 'Hello,',
               'Je suis un test de templating en odt.':
                'I am an odt templating test',
               'Felix da housecat': u'Félix le chat de la maison',
               'We sell stuff': u'On vend des choses',
              }
    return catalog.get(string, string)

def stream_to_string(stream):
    # In Python 3, stream will be bytes
    if not isinstance(stream, str):
        return str(stream, 'utf-8')
    return stream


class TestOOTemplating(object):

    def setup(self):
        thisdir = os.path.dirname(__file__)
        filepath = os.path.join(thisdir, 'test.odt')
        self.oot = Template(open(filepath, mode='rb'))
        self.data = {'first_name': u'Trente',
                     'last_name': u'Møller',
                     'ville': u'Liège',
                     'friends': [{'first_name': u'Camille',
                                  'last_name': u'Salauhpe'},
                                 {'first_name': u'Mathias',
                                  'last_name': u'Lechat'}],
                     'hobbies': [u'Music', u'Dancing', u'DJing'],
                     'animals': [u'Felix da housecat', u'Dog eat Dog'],
                     'images': [(open(os.path.join(thisdir, 'one.jpg'), 'rb'),
                                 'image/jpeg'),
                                (open(os.path.join(thisdir, 'two.png'), 'rb'),
                                 'image/png')],
                     'oeuf': open(os.path.join(thisdir, 'egg.jpg'), 'rb'),
                     'footer': u'We sell stuff'}

    def test_init(self):
        "Testing the correct handling of the styles.xml and content.xml files"
        ok_(isinstance(self.oot.stream, list))
        eq_(self.oot.stream[0], (PI, ('relatorio', 'content.xml'), None))
        ok_((PI, ('relatorio', 'content.xml'), None) in self.oot.stream)

    def test_directives(self):
        "Testing the directives interpolation"
        xml = b'''<xml xmlns:text="urn:text" xmlns:xlink="urn:xlink">
                    <text:a xlink:href="relatorio://foo">foo</text:a>
                 </xml>'''
        interpolated = self.oot.insert_directives(xml)
        root_interpolated = lxml.etree.parse(interpolated).getroot()
        child = root_interpolated[0]
        eq_(child.get('{http://genshi.edgewall.org/}replace'), 'foo')

    def test_column_looping(self):
        xml = b'''
<table:table
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    table:name="Tableau1"
    table:style-name="Tableau1">
    <table:table-column table:style-name="Tableau1.A"
                        table:number-columns-repeated="2"/>
    <table:table-column table:style-name="Tableau1.C"/>
    <table:table-column table:style-name="Tableau1.A"/>
    <table:table-column table:style-name="Tableau1.E"/>
    <table:table-header-rows>
        <table:table-row table:style-name="Tableau1.1">
            <table:table-cell table:style-name="Tableau1.A1"
                              office:value-type="string">
                <text:p text:style-name="Table_20_Heading">Brol</text:p>
            </table:table-cell>
            <table:table-cell table:style-name="Tableau1.A1"
                              office:value-type="string">
                <text:p text:style-name="Table_20_Heading">
                    <text:a xlink:type="simple"
                            xlink:href="relatorio://for each=&quot;title in titles&quot;">for each=&quot;title in titles&quot;</text:a>
                </text:p>
            </table:table-cell>
            <table:table-cell table:style-name="Tableau1.A1"
                              office:value-type="string">
                <text:p text:style-name="Table_20_Heading">${title}</text:p>
                <text:p text:style-name="Table_20_Heading"/>
            </table:table-cell>
            <table:table-cell table:style-name="Tableau1.A1"
                              office:value-type="string">
                <text:p text:style-name="Table_20_Heading">
                    <text:a xlink:type="simple"
                            xlink:href="relatorio:///for">/for</text:a>
                </text:p>
            </table:table-cell>
            <table:table-cell table:style-name="Tableau1.E1"
                              office:value-type="string">
                <text:p text:style-name="Table_20_Heading">Truc</text:p>
            </table:table-cell>
        </table:table-row>
    </table:table-header-rows>
    <table:table-row>
        <table:table-cell table:style-name="Tableau1.A2"
                          table:number-columns-spanned="5"
                          office:value-type="string">
            <text:p text:style-name="Table_20_Contents">
                <text:a xlink:type="simple"
                        xlink:href="relatorio://for%20each=%22items%20in%20lst%22">for each=&quot;items in lst&quot;</text:a>
            </text:p>
        </table:table-cell>
        <table:covered-table-cell/>
        <table:covered-table-cell/>
        <table:covered-table-cell/>
        <table:covered-table-cell/>
    </table:table-row>
    <table:table-row>
        <table:table-cell table:style-name="Tableau1.A3"
                          office:value-type="string">
            <text:p text:style-name="Table_20_Contents">Brol</text:p>
        </table:table-cell>
        <table:table-cell table:style-name="Tableau1.A3"
                          office:value-type="string">
            <text:p text:style-name="Table_20_Contents">
                <text:a xlink:type="simple"
                        xlink:href="relatorio://for%20each=%22item%20in%20items%22">for each=&quot;item in items&quot;</text:a>
            </text:p>
        </table:table-cell>
        <table:table-cell table:style-name="Tableau1.A3"
                          office:value-type="string">
            <text:p text:style-name="Table_20_Contents">${item}</text:p>
            <text:p text:style-name="Table_20_Contents"/>
        </table:table-cell>
        <table:table-cell table:style-name="Tableau1.A3"
                          office:value-type="string">
            <text:p text:style-name="Table_20_Contents">
                <text:a xlink:type="simple"
                        xlink:href="relatorio:///for">/for</text:a>
            </text:p>
        </table:table-cell>
        <table:table-cell table:style-name="Tableau1.A2"
                          office:value-type="string">
            <text:p text:style-name="Table_20_Contents">Truc</text:p>
        </table:table-cell>
    </table:table-row>
    <table:table-row>
        <table:table-cell table:style-name="Tableau1.A2"
                          table:number-columns-spanned="5"
                          office:value-type="string">
            <text:p text:style-name="Table_20_Contents">
                <text:a xlink:type="simple"
                        xlink:href="relatorio:///for">/for</text:a>
            </text:p>
        </table:table-cell>
        <table:covered-table-cell/>
        <table:covered-table-cell/>
        <table:covered-table-cell/>
        <table:covered-table-cell/>
    </table:table-row>
</table:table>'''
        interpolated = self.oot.insert_directives(xml)
        root = lxml.etree.parse(interpolated).getroot()
        child2 = root[1]
        eq_(child2.tag, "{%s}repeat" % RELATORIO_URI)
        eq_(child2.get("closing"), "3")
        eq_(child2.get("opening"), "1")
        eq_(len(child2), 1)
        child4 = root[3]
        eq_(child4.tag, "{%s}table-header-rows" % OO_TABLE_NS)
        row1 = child4[0]
        ok_(row1.get("{%s}attrs" % GENSHI_URI)
                .startswith('__relatorio_reset_col_count'))
        eq_(len(row1), 4)
        loop = row1[1]
        eq_(loop.tag, "{%s}for" % GENSHI_URI)
        cell = loop[0]
        ok_(cell.get("{%s}attrs" % GENSHI_URI)
                .startswith('__relatorio_inc_col_count'))
        last_row_node = row1[3]
        eq_(last_row_node.tag, "{%s}replace" % GENSHI_URI)
        ok_(last_row_node.get("value")
                         .startswith('__relatorio_store_col_count'))

    def test_text_outside_p(self):
        "Testing that the tail text of a directive node is handled properly"
        xml = b'''<xml xmlns:text="urn:text" xmlns:xlink="urn:xlink">
                    <text:a xlink:href="relatorio://if%20test=%22True%22">if test=&quot;True&quot;</text:a>
                    xxx
                    <text:p text:style-name="other">yyy</text:p>
                    zzz
                    <text:a xlink:href="relatorio:///if">/if</text:a>
                    aaa
                 </xml>'''
        interpolated = self.oot.insert_directives(xml)
        root_interpolated = lxml.etree.parse(interpolated).getroot()
        child = root_interpolated[0]
        eq_(child.tag, '{http://genshi.edgewall.org/}if')
        eq_(child.text.strip(), 'xxx')
        eq_(child.tail.strip(), 'aaa')

    def test_styles(self):
        "Testing that styles get rendered"
        stream = self.oot.generate(**self.data)
        rendered = stream_to_string(stream.events.render(encoding='utf-8'))
        ok_('We sell stuff' in rendered)

        dico = self.data.copy()
        del dico['footer']
        stream = self.oot.generate(**dico)
        assert_raises(UndefinedError,
            lambda: stream.events.render(encoding='utf-8'))

    def test_generate(self):
        "Testing that content get rendered"
        stream = self.oot.generate(**self.data)
        rendered = stream_to_string(stream.events.render(encoding='utf-8'))
        ok_('Bonjour,' in rendered)
        ok_('Trente' in rendered)
        ok_('Møller' in rendered)
        ok_('Dog eat Dog' in rendered)
        ok_('Felix da housecat' in rendered)

    def test_filters(self):
        "Testing the filters with the Translator filter"
        stream = self.oot.generate(**self.data)
        translated = stream.filter(Translator(pseudo_gettext))
        translated_xml = stream_to_string(
            translated.events.render(encoding='utf-8'))
        ok_("Hello," in translated_xml)
        ok_("I am an odt templating test" in translated_xml)
        ok_('Felix da housecat' not in translated_xml)
        ok_('Félix le chat de la maison' in translated_xml)
        ok_('We sell stuff' not in translated_xml)
        ok_('On vend des choses' in translated_xml)

    def test_images(self):
        "Testing the image replacement directive"
        stream = self.oot.generate(**self.data)
        rendered = stream_to_string(stream.events.render(encoding='utf-8'))
        styles_idx = rendered.find('<?relatorio styles.xml?>')
        tree = lxml.etree.parse(StringIO(rendered[25:styles_idx]))
        root = tree.getroot()
        images = root.xpath('//draw:frame', namespaces=self.oot.namespaces)
        eq_(len(images), 3)
        eq_(images[0].get('{%s}name' % self.oot.namespaces['draw']), "")
        eq_(images[1].get('{%s}name' % self.oot.namespaces['draw']), '')
        eq_(images[1].get('{%s}width' % self.oot.namespaces['svg']),
            '1.732cm')
        eq_(images[1].get('{%s}height' % self.oot.namespaces['svg']),
            '1.513cm')
        eq_(images[2].get('{%s}width' % self.oot.namespaces['svg']),
            '1.732cm')
        eq_(images[2].get('{%s}height' % self.oot.namespaces['svg']),
            '1.513cm')

    def test_regexp(self):
        "Testing the regexp used to find relatorio tags"
        # a valid expression
        group = GENSHI_EXPR.match('for each="foo in bar"').groups()
        eq_(group, (None, 'for', 'each', 'foo in bar'))

        # invalid expr
        group = GENSHI_EXPR.match('foreach="foo in bar"').groups()
        eq_(group, (None, None, None, None))

        # valid closing tags
        group = GENSHI_EXPR.match('/for').groups()
        eq_(group, ('/', 'for', None, None))
        group = GENSHI_EXPR.match('/for ').groups()
        eq_(group, ('/', 'for', None, None))

        # another non matching expr
        group = GENSHI_EXPR.match('formatLang("en")').groups()
        eq_(group, (None, None, None, None))
