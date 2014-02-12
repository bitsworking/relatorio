from os.path import join, dirname

class Invoice(dict):

    @property
    def total(self):
        return sum(l['amount'] for l in self['lines'])

    @property
    def vat(self):
        return self.total * 0.21


inv = Invoice(customer={'name': 'John Bonham',
                        'address': {'street': 'Smirnov street',
                                    'zip': 1000,
                                    'city': 'Montreux'}},
              lines=[{'item': {'name': 'Vodka 70cl',
                               'reference': 'VDKA-001',
                               'price': 10.34},
                      'quantity': 7,
                      'amount': 7*10.34},
                     {'item': {'name': 'Cognac 70cl',
                               'reference': 'CGNC-067',
                               'price': 13.46},
                      'quantity': 12,
                      'amount': 12*13.46},
                     {'item': {'name': 'Sparkling water 25cl',
                               'reference': 'WATR-007',
                               'price': 4},
                      'quantity': 1,
                      'amount': 4},
                     {'item': {'name': 'Good customer',
                               'reference': 'BONM-001',
                               'price': -20},
                      'quantity': 1,
                      'amount': -20},
                    ],
              id='MZY-20080703',
              status='late',
              bottle=(open(join(dirname(__file__), 'bouteille.png'), 'rb'),
                  'image/png'))

