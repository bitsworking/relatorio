import relatorio
from common import Invoice, inv
from os.path import join, dirname

ODT_MIME = 'application/vnd.oasis.opendocument.text'
ODS_MIME = 'application/vnd.oasis.opendocument.spreadsheet'
ODP_MIME = 'application/vnd.oasis.opendocument.presentation'

repository = relatorio.ReportRepository()
repository.add_report(Invoice, ODT_MIME, 'basic.odt', report_name='basic')
repository.add_report(Invoice, ODT_MIME,
                      'complicated.odt', report_name='complicated')
repository.add_report(Invoice, ODS_MIME, 'pivot.ods', report_name='pivot')
repository.add_report(Invoice, ODP_MIME,
                      'presentation.odp', report_name='presentation')
repository.add_report(Invoice, 'image/png', 'pie_chart', report_name='pie')

if __name__ == '__main__':
    # Add a chart to the invoice
    inv['chart'] = repository.by_id(Invoice, 'pie')[:2]

    # Generate all reports on the invoice class
    for report_name, ext in (('basic', '.odt'),
                             ('complicated', '.odt'),
                             ('pivot', '.ods'),
                             ('presentation', '.odp')):
        filename = 'output_%s%s' % (report_name, ext)
        print "generating '%s'..." % filename,
        report, mimetype, desc = repository.by_id(Invoice, report_name)
        data = report(o=inv).render().getvalue()
        open(join(dirname(__file__), filename), 'wb').write(data)
        print "done"
