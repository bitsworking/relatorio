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

__metaclass__ = type

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import yaml
import genshi
import genshi.output
from genshi.template import NewTextTemplate

from relatorio.templates.base import RelatorioStream
from relatorio.reporting import MIMETemplateLoader

import cairo
import pycha
import pycha.pie
import pycha.line
import pycha.bar

PYCHA_TYPE = {'pie': pycha.pie.PieChart,
              'vbar': pycha.bar.VerticalBarChart,
              'hbar': pycha.bar.HorizontalBarChart,
              'line': pycha.line.LineChart,
             }
_encode = genshi.output.encode


class Template(NewTextTemplate):
    "A chart templating object"

    def generate(self, *args, **kwargs):
        generated = super(Template, self).generate(*args, **kwargs)
        return RelatorioStream(generated, CairoSerializer())

    @staticmethod
    def id_function(mimetype):
        "The function used to return the codename."
        if mimetype in ('image/png', 'image/svg'):
            return 'chart'


class CairoSerializer:

    def __init__(self):
        self.text_serializer = genshi.output.TextSerializer()

    def __call__(self, stream):
        result = StringIO()
        yml = StringIO(_encode(self.text_serializer(stream)))
        chart_yaml = yaml.load(yml.read())
        chart_info = chart_yaml['chart']
        chart_type = chart_info['output_type']
        if chart_type == 'png':
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                         chart_yaml['options']['width'],
                                         chart_yaml['options']['height'])
        elif chart_type == 'svg':
            surface = cairo.SVGSurface(result, chart_yaml['options']['width'],
                                       chart_yaml['options']['height'])
        else:
            raise NotImplementedError

        chart = PYCHA_TYPE[chart_info['type']](surface, chart_yaml['options'])
        chart.addDataset(chart_info['dataset'])
        chart.render()

        if chart_type == 'png':
            surface.write_to_png(result)
        elif chart_type == 'svg':
            surface.finish()

        return result

MIMETemplateLoader.add_factory('chart', Template, Template.id_function)
