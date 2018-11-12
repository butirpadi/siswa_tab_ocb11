from flectra import models, fields, api, _
from pprint import pprint
from datetime import datetime

class saldo_tabungan_per_siswa_rel(models.TransientModel):
    _name = 'siswa_tab_ocb11.saldo_tabungan_per_siswa_rel'

    wizard_id = fields.Many2one('siswa_tab_ocb11.wizard_saldo_tabungan', ondelete="cascade")
    rombel_id = fields.Many2one('siswa_ocb11.rombel', ondelete="cascade")
    siswa_id = fields.Many2one('res.partner', ondelete="cascade")
    saldo = fields.Float('Saldo', default=0.0) 