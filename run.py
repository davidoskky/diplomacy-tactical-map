#!/usr/bin/env python
# EXAMPLE CODE BELOW

from map import *
from tactic import *

context(ENGLAND)
set('nor')
fleet_hold('nor')
fleet_hold('lon')
army_hold('yor')

context(ITALY)
set('tun')
set('gas')
set('mar')
set('spa')
army_move('gas', 'spa')
fleet_support_move('lyo', 'gas', 'spa')
fleet_move_failed('ion', 'tun')
army_support_move('mar', 'gas', 'spa')

context(FRANCE)
army_hold('par')
fleet_hold('nth')
dislodge('spa')
fleet_move_failed('wes', 'tun')
set('naf')
set('por')

context(GERMANY)
fleet_move('den', 'bal')
army_move('trl', 'ven')
army_hold('ber')
set('hol')
set('den')
set('swe')
set('ven')

context(RUSSIA)
set('boh')
set('sil')
set('gal')
set('pru')
set('bud')
set('rum')

context(AUSTRIA)
set('alb')
set('vie')

context(TURKEY)
army_hold('con')
fleet_move_failed('eas', 'ion')
set('bul')
set('ser')
set('smy')

tactical_map()
done()
