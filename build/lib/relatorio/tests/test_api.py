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
from nose.tools import *

from relatorio.reporting import (ReportRepository, Report, MIMETemplateLoader,
                                 DefaultFactory, _absolute, _guess_type)


class StubObject(object):

    def __init__(self, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)


class TestRepository(object):

    def test_register(self):
        "Testing the registration"
        reporting = ReportRepository()
        reporting.add_report(StubObject, 'text/plain',
                             os.path.join('templates', 'test.tmpl'),
                             description='Test report')

        assert_true(StubObject in reporting.classes)
        assert_true('default' in reporting.classes[StubObject].ids)
        assert_true('text/plain' in reporting.classes[StubObject].mimetypes)

        report, mime, desc = reporting.classes[StubObject].ids['default']
        eq_(mime, 'text/plain')
        eq_(desc, 'Test report')
        eq_(report.mimetype, 'text/plain')
        assert_true(report.fpath.endswith(os.path.join('templates',
                                                       'test.tmpl')))

        report2, name = (reporting.classes[StubObject]
                         .mimetypes['text/plain'][0])
        eq_(name, 'default')
        eq_(report, report2)

    def test_mimeguesser(self):
        eq_(_guess_type('application/pdf'), 'pdf')
        eq_(_guess_type('text/plain'), 'text')
        eq_(_guess_type('text/xhtml'), 'markup')
        eq_(_guess_type('application/vnd.oasis.opendocument.text'), 'oo.org')

    def abspath_helper(self, path):
        return _absolute(path)

    def test_absolute(self):
        "Test the absolute path calculation"
        eq_("/home/nicoe/python/mock.py",
            _absolute("/home/nicoe/python/mock.py"))

        our_dir, _ = os.path.split(__file__)
        # We use this because me go up by two frames
        new_path = self.abspath_helper(os.path.join('brol', 'toto'))
        eq_(os.path.join(our_dir, 'brol', 'toto'), new_path)


class TestReport(object):

    def setup(self):
        self.loader = MIMETemplateLoader()
        our_dir, _ = os.path.split(__file__)
        self.report = Report(os.path.join(our_dir, 'templates', 'test.tmpl'),
                             'text/plain', DefaultFactory(), self.loader)

    def test_report(self):
        "Testing the report generation"
        a = StubObject(name='OpenHex')
        eq_(self.report(o=a).render(), 'Hello OpenHex.\n')

    def test_factory(self):
        "Testing the data factory"
        class MyFactory:
            def __call__(self, o, time, y=1):
                d = dict()
                d['o'] = o
                d['y'] = y
                d['time'] = time
                d['func'] = lambda x: x + 1
                return d

        our_dir, _ = os.path.split(__file__)
        report = Report(os.path.join(our_dir, 'templates', 'time.tmpl'),
                        'text/plain', MyFactory(), self.loader)

        a = StubObject(name='Foo')
        eq_(report(o=a, time="One o'clock").render(),
            "Hi Foo,\nIt's One o'clock to 2 !\n")
        eq_(report(o=a, time="One o'clock", y=4).render(),
            "Hi Foo,\nIt's One o'clock to 5 !\n")
        assert_raises(TypeError, report, a)


class TestReportInclude(object):

    def test_include(self):
        our_dir = os.path.dirname(__file__)
        template_path = os.path.join(our_dir, 'templates')
        relative_report = Report(os.path.join(template_path, 'include.tmpl'),
                                 'text/plain')
        eq_(relative_report().render(), 'Another Hello.\n\n')
