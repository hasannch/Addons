# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID, _


def pre_init_hook(env):
    try:
        sql = "UPDATE ir_module_module SET website = '%s' WHERE license like '%s' and website <> ''" % ('https://pandorarevolution.com', 'OEEL%')
        env.cr.execute(sql)
        env.cr.commit()
    except Exception as e:
        pass

def post_init_hook(env):
    # a = check_module_installed(cr, ['app_web_superbar','aaaaa'])
    pass
    # cr.execute("")

def uninstall_hook(env):
    """
    数据初始化，卸载时执行
    """
    pass

def check_module_installed(env, modules):
    installed = False
    m = env['ir.module.module'].sudo().search([('name', 'in', modules), ('state', 'in', ['installed', 'to install', 'to upgrade'])])
    if len(m) == len(modules):
        installed = True
    return installed

