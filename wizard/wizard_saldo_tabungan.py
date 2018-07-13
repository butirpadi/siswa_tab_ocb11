from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime

class wizard_saldo_tabungan(models.TransientModel):
    _name = 'siswa_tab_ocb11.wizard_saldo_tabungan'

    name = fields.Char('Name', default='Report Saldo Tabungan')
    awal = fields.Date('Periode Awal', default=datetime.today(), required=True)
    akhir = fields.Date('Periode Akhir', default=datetime.today(), required=True)
    rombel_id = fields.Many2one('siswa_ocb11.rombel_id')
    siswa_id = fields.Many2one('res.partner', string='Siswa')
    tabungan_ids = fields.Many2many('siswa_tab_ocb11.tabungan', relation='siswa_tab_ocb11_wizard_report_report_tabungan_rel', column1='report_id',column2='tabungan_id', string="Data Tabungan")
    saldo_begining = fields.Float('Saldo Begining', default=0)
    saldo_ending = fields.Float('Saldo Ending', default=0)

    # def action_save(self):
    #     self.ensure_one()

    #     if self.tipe == 'det' :
    #         if self.siswa_id:
    #             siswa = 'siswa_id = ' + str(self.siswa_id.id)
    #         else:
    #             siswa = 'True'

    #         print('get data tabungan')
    #         self.env.cr.execute("select * from siswa_tab_ocb11_tabungan where state = 'post' and tanggal >= '%s' and tanggal <= '%s' and %s" % (self.awal, self.akhir, siswa) )
    #         tabs = self.env.cr.dictfetchall()

    #         # # tabs = self.env['siswa_tab_ocb11.tabungan'].search([('tanggal','>=',self.awal),('tanggal','<=',self.akhir), siswa])

    #         reg_tab = []
    #         for tab in tabs:
    #             self.write({
    #                 'tabungan_ids' : [(4,tab['id'])]
    #             })

    #         # saldo_before = self.env['siswa_tab_ocb11.tabungan'].search([('tanggal','<',self.awal), ('siswa_id','=',self.siswa_id.id)])
    #         # saldo_begining = sum(x.jumlah for x in saldo_before)

    #         self.env.cr.execute("select sum(jumlah) from siswa_tab_ocb11_tabungan where tanggal < '%s' and %s" % (self.awal, siswa) )
    #         saldo_begining = self.env.cr.fetchone()[0]
            
    #         # saldo_after = self.env['siswa_tab_ocb11.tabungan'].search([('tanggal','>',self.akhir), ('siswa_id','=',self.siswa_id.id)])
    #         # saldo_ending = sum(x.jumlah for x in saldo_after)

    #         self.env.cr.execute("select sum(jumlah) from siswa_tab_ocb11_tabungan where tanggal > '%s' and %s" % (self.akhir, siswa) )
    #         saldo_ending = self.env.cr.fetchone()[0]

    #         saldo_current = sum(x['jumlah'] for x in tabs)
            
    #         self.write({
    #                 'saldo_begining' : saldo_begining,
    #                 'saldo_ending' : saldo_ending,
    #                 'saldo_current' : saldo_current,
    #             })

    #         return self.env.ref('siswa_tab_ocb11.report_tabungan_action').report_action(self)

    #     else:
    #         print('show summary data')

