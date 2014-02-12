from os.path import abspath, join, dirname
from relatorio import Report

# test data
from common import inv

#PDF
if __name__ == '__main__':
    print "generating output_basic.pdf... ",
    report = Report(abspath(join(dirname(__file__), 'basic.tex')),
        'application/pdf')
    content = report(o=inv).render().getvalue()
    open(join(dirname(__file__), 'output_basic.pdf'), 'wb').write(content)
    print "done"

