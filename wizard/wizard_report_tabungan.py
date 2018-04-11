from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime

class wizard_report_tabungan(models.TransientModel):
    _name = 'siswa_tab_ocb11.wizard_report_tabungan'

    name = fields.Char('Name', default='Report Tabungan')
    awal = fields.Date('Periode Awal', default=datetime.today(), required=True)
    akhir = fields.Date('Periode Akhir', default=datetime.today(), required=True)
    siswa_id = fields.Many2one('res.partner', string='Siswa', required=True)
    tabungan_ids = fields.Many2many('siswa_tab_ocb11.tabungan', relation='siswa_tab_ocb11_wizard_report_report_tabungan_rel', column1='report_id',column2='tabungan_id', string="Data Tabungan")
    saldo_begining = fields.Float('Saldo Begining', default=0)
    saldo_ending = fields.Float('Saldo Ending', default=0)
    saldo_current = fields.Float('Saldo Current', default=0)



    def action_save(self):
        self.ensure_one()
        # set kas_ids
        tabs = self.env['siswa_tab_ocb11.tabungan'].search([('tanggal','>=',self.awal),('tanggal','<=',self.akhir), ('siswa_id','=',self.siswa_id.id)])
        reg_tab = []
        for tab in tabs:
            self.write({
                'tabungan_ids' : [(4,tab.id)]
            })
        saldo_before = self.env['siswa_tab_ocb11.tabungan'].search([('tanggal','<',self.awal), ('siswa_id','=',self.siswa_id.id)])
        saldo_begining = sum(x.jumlah for x in saldo_before)
        
        saldo_after = self.env['siswa_tab_ocb11.tabungan'].search([('tanggal','>',self.akhir), ('siswa_id','=',self.siswa_id.id)])
        saldo_ending = sum(x.jumlah for x in saldo_after)
        
        saldo_current = sum(x.jumlah for x in tabs)
        
        self.write({
                'saldo_begining' : saldo_begining,
                'saldo_ending' : saldo_ending,
                'saldo_current' : saldo_current,
            })

        return self.env.ref('siswa_tab_ocb11.report_tabungan_action').report_action(self)

