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

import genshi.core
from genshi.template import NewTextTemplate, MarkupTemplate

from relatorio.reporting import MIMETemplateLoader


class RelatorioStream(genshi.core.Stream):
    "Base class for the relatorio streams."

    def render(self, method=None, encoding='utf-8', out=None, **kwargs):
        "calls the serializer to render the template"
        return self.serializer(self.events)

    def serialize(self, method='xml', **kwargs):
        "generates the bitstream corresponding to the template"
        return self.render(method, **kwargs)

    def __or__(self, function):
        "Support for the bitwise operator"
        return RelatorioStream(self.events | function, self.serializer)

MIMETemplateLoader.add_factory('text', NewTextTemplate)
MIMETemplateLoader.add_factory('xml', MarkupTemplate)
