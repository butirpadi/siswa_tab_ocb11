from flectra import models, fields, api, _
from pprint import pprint
from datetime import datetime

class wizard_report_tabungan_rombel_rel(models.TransientModel):
    _name = 'siswa_tab_ocb11.wizard_report_tabungan_rombel_rel'

    wizard_id = fields.Many2one('siswa_tab_ocb11.wizard_saldo_tabungan', ondelete="cascade")
    rombel_id = fields.Many2one('siswa_ocb11.rombel', ondelete="cascade")
    saldo = fields.Float('Saldo', default=0.0) 