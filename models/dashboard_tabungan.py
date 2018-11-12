# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions, _
from flectra.addons import decimal_precision as dp
from datetime import datetime
from pprint import pprint

class dashboard_tabungan(models.Model):
    _name = 'siswa_tab_ocb11.dashboard_tabungan'

    color = fields.Integer(string='Color Index') 
    name = fields.Char('Name')
    subtitle = fields.Char('Subtitle')
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string='Rombongan Belajar', ondelete="cascade")
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', ondelete="cascade")
    saldo = fields.Float('Saldo', default=0.00)
    active = fields.Boolean(default=False)

    def compute_saldo_tabungan(self):
        if self.rombel_id and self.tahunajaran_id:
            print('Compute saldo tabungan per rombel')
            # get siswa
            rombel_siswa_ids = self.env['siswa_ocb11.rombel_siswa'].search([
                ('rombel_id','=',self.rombel_id.id),
                ('tahunajaran_id','=',self.tahunajaran_id.id),
            ])
            siswa_ids = []
            for rbs in rombel_siswa_ids:
                siswa_ids.append(rbs.siswa_id.id)
                
            # # get saldo per rombel
            # setoran_list = self.env['siswa_tab_ocb11.tabungan'].search([
            #     ('siswa_id','in',siswa_ids),
            #     ('state','=','post'),
            #     ('jenis','=','setor'),
            # ])
            # setoran = sum(setoran_list.mapped('jumlah'))

            # tarik_list = self.env['siswa_tab_ocb11.tabungan'].search([
            #     ('siswa_id','in',siswa_ids),
            #     ('state','=','post'),
            #     ('jenis','=','tarik'),
            # ])
            # tarikan = sum(tarik_list.mapped('jumlah'))
            # saldo = setoran - tarikan

            tabungan_list = self.env['siswa_tab_ocb11.tabungan'].search([
                ('siswa_id','in',siswa_ids),
                ('state','=','post')
            ])
            saldo = sum(tabungan_list.mapped('jumlah'))
        else:
            print('Compute Saldo Tabungan')
            self.env.cr.execute("select coalesce(sum(coalesce(jumlah,0)),0) from siswa_tab_ocb11_tabungan where state = 'post' ")
            saldo = self.env.cr.fetchone()[0]        

        self.saldo = saldo 