from os.path import abspath, join, dirname
from relatorio import Report

# test data
from common import inv

if __name__ == '__main__':
    pie_report = Report(abspath(join(dirname(__file__), 'pie_chart')),
            'image/png')
    open(join(dirname(__file__), 'pie.png'), 'wb').write(
            pie_report(o=inv).render().getvalue())
    hbar_report = Report(abspath(join(dirname(__file__), 'hbar_chart')),
            'image/svg')
    open(join(dirname(__file__), 'hbar.svg'), 'wb').write(
            hbar_report(o=inv).render().getvalue())
    vbar_report = Report(abspath(join(dirname(__file__), 'vbar_chart')),
            'image/svg')
    open(join(dirname(__file__), 'vbar.svg'), 'wb').write(
            vbar_report(o=inv).render().getvalue())
    line_report = Report(abspath(join(dirname(__file__), 'line_chart')),
            'image/png')
    open(join(dirname(__file__), 'line.png'), 'wb').write(
            line_report(o=inv).render().getvalue())
