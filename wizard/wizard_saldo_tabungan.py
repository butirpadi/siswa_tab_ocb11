from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime

class wizard_saldo_tabungan(models.TransientModel):
    _name = 'siswa_tab_ocb11.wizard_saldo_tabungan'

    name = fields.Char('Name', default='Report Saldo Tabungan')
    tanggal = fields.Date('Tanggal', default=datetime.today(), required=True)
    saldo_rombel_ids = fields.One2many('siswa_tab_ocb11.wizard_report_tabungan_rombel_rel', inverse_name="wizard_id", string="Rombongan Belajar")
    saldo_per_siswa_ids = fields.One2many('siswa_tab_ocb11.saldo_tabungan_per_siswa_rel', inverse_name="wizard_id", string="Saldo Detail")
    rombel_ids = fields.Many2many('siswa_ocb11.rombel', relation='siswa_tab_ocb11_wizard_saldo_tabungan_rombel_rel', column1='wizard_id',column2='rombel_id', string="Rombongan Belajar")
    report_type = fields.Selection([('sum', 'Summary'), ('det', 'Detail')], string='Tipe', required=True, default='sum')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran')
    # akhir = fields.Date('Periode Akhir', default=datetime.today(), required=True)
    # tabungan_ids = fields.Many2many('siswa_tab_ocb11.tabungan', relation='siswa_tab_ocb11_wizard_report_report_tabungan_rel', column1='report_id',column2='tabungan_id', string="Data Tabungan")
    # siswa_id = fields.Many2one('res.partner', string='Siswa')
    tabungan_ids = fields.Many2many('siswa_tab_ocb11.tabungan', relation='siswa_tab_ocb11_wizard_report_report_tabungan_rel', column1='wizard_id',column2='tabungan_id', string="Data Tabungan")
    # saldo_begining = fields.Float('Saldo Begining', default=0)
    # saldo_ending = fields.Float('Saldo Ending', default=0)
    

    def action_save(self):
        self.tahunajaran_id = self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]).id
        tahunajaran_id = self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)])            
        my_rombel_ids = self.env['siswa_ocb11.rombel'].search([])

        # jika rombel di pilih dalam selection
        if self.rombel_ids:
            my_rombel_ids = self.rombel_ids

        for rb in my_rombel_ids:
            rombel_siswa_ids = self.env['siswa_ocb11.rombel_siswa'].search([
                ('rombel_id','=',rb.id),
                ('tahunajaran_id','=',self.tahunajaran_id.id),
            ])

            # get data saldo tabungan based on report_type
            if self.report_type == 'sum':
                # report summary
                siswa_ids = []
                for rbs in rombel_siswa_ids:
                    siswa_ids.append(rbs.siswa_id.id)
                print('siswa_ids : ')
                pprint(siswa_ids)
                tabungan_list = self.env['siswa_tab_ocb11.tabungan'].search([
                    ('siswa_id','in',siswa_ids),
                    ('state','=','post')
                ])
        
                saldo = sum(tabungan_list.mapped('jumlah'))

                self.saldo_rombel_ids = [(0,0,{
                    'rombel_id' : rb.id,
                    'saldo' : saldo
                })]
            
            else:
                # report detail
                for rbs in rombel_siswa_ids:
                    tabungan_list = self.env['siswa_tab_ocb11.tabungan'].search([
                        ('siswa_id','=',rbs.siswa_id.id),
                        ('state','=','post')
                    ])

                    saldo = sum(tabungan_list.mapped('jumlah'))

                    self.saldo_per_siswa_ids = [(0,0,{
                        'rombel_id' : rbs.rombel_id.id,
                        'siswa_id' : rbs.siswa_id.id,
                        'saldo' : saldo 
                    })]
                
        # return qweb report based on report_type
        if self.report_type == 'sum':
            # return qweb report
            return self.env.ref('siswa_tab_ocb11.report_saldo_tabungan_action').report_action(self)
        else:
            return self.env.ref('siswa_tab_ocb11.report_saldo_tabungan_detail_action').report_action(self)
                    


            # # show wizard form view
            # return {
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'res_model': 'siswa_tab_ocb11.wizard_saldo_tabungan',
            #     'target': 'current',
            #     'res_id': self.id,
            #     'type': 'ir.actions.act_window'
            # }

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

