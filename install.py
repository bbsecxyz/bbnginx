#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-04 23:48
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : https://github.com/alexazhou/VeryNginx
# @Disc    : install VeryNginx
# @Disc    : support python 2.x and 3.x

import os
import sys
import getopt
import filecmp


openresty_pkg = 'openresty-1.13.6.2.tar.gz'

work_path = os.getcwd()

def install_openresty( ):
    #check if the old version of VeryNginx installed( use upcase directory )
    if os.path.exists('/opt/VeryNginx/VeryNginx') == True:
        print("Seems that a old version of VeryNginx was installed in /opt/verynginx/...\nBefore install, please delete it and backup the configs if you need.")
        sys.exit(1)
    
    #makesure the dir is clean
    print('### makesure the work directory is clean')
    exec_sys_cmd('rm -rf ' + openresty_pkg.replace('.tar.gz','_build'))


    #configure && compile && install openresty
    print('### configure openresty ...')
    exec_sys_cmd('chmod -R 7777 ./*')

    exec_sys_cmd('cp -r ' + openresty_pkg.replace('.tar.gz','') + '  ' + openresty_pkg.replace('.tar.gz','_build') )

    os.chdir( openresty_pkg.replace('.tar.gz','_build') + '/bundle/nginx-1.14.2' )
    exec_sys_cmd('wget https://raw.githubusercontent.com/kn007/patch/45f1417c450fc82cd470cb73a32e23085c4ba3d5/nginx.patch')
    exec_sys_cmd('wget https://raw.githubusercontent.com/kn007/patch/c59592bc1269ba666b3bb471243c5212b50fd608/nginx_auto_using_PRIORITIZE_CHACHA.patch')
    exec_sys_cmd('patch -p1 < nginx.patch')
    exec_sys_cmd('patch -p1 < nginx_auto_using_PRIORITIZE_CHACHA.patch')


    os.chdir('../../'+ '/openssl-1.1.1a')
    exec_sys_cmd('pwd')
    exec_sys_cmd('wget https://raw.githubusercontent.com/hakasenyang/openssl-patch/master/openssl-equal-1.1.1a.patch')
    exec_sys_cmd('patch -p1 < openssl-equal-1.1.1a.patch')


    os.chdir('../')
    exec_sys_cmd('pwd')
    exec_sys_cmd('git clone https://github.com/eustas/ngx_brotli.git')
    os.chdir('../ngx_brotli')
    exec_sys_cmd('git submodule update --init')

    os.chdir('../')
    exec_sys_cmd('pwd')
    exec_sys_cmd( './configure --add-module=\'ngx_brotli\' --prefix=/opt/verynginx/openresty --user=nginx --group=nginx --with-http_v2_module --with-http_sub_module --with-http_stub_status_module --with-luajit ' +
                  '--with-openssl=openssl-1.1.1a --with-openssl-opt=\'enable-tls1_3\' --with-http_v2_hpack_enc' )
    exec_sys_cmd('sudo rm -rf ngx_brotli ')
    print('### compile openresty ...')
    exec_sys_cmd( 'make' )
    
    print('### install openresty ...')
    exec_sys_cmd( 'make install' )

def install_verynginx():
    
    #install VeryNginx file
    print('### copy VeryNginx files ...')
    os.chdir( work_path )
    if os.path.exists('/opt/verynginx/') == False:
        exec_sys_cmd( 'mkdir -p /opt/verynginx' )
    
    exec_sys_cmd( 'cp -r -f ./verynginx /opt/verynginx' )

    #copy nginx config file to openresty
    if os.path.exists('/opt/verynginx/openresty') == True:
        if filecmp.cmp( '/opt/verynginx/openresty/nginx/conf/nginx.conf', '/opt/verynginx/openresty/nginx/conf/nginx.conf.default', False ) == True:
            print('cp nginx config file to openresty')
            exec_sys_cmd( 'cp -f ./nginx.conf  /opt/verynginx/openresty/nginx/conf/' )
    else:
        print( 'openresty not fount, so not copy nginx.conf' )

    #set mask for the path which used for save configs
    exec_sys_cmd( 'chmod -R 777 /opt/verynginx/verynginx/configs' )


def update_verynginx():
    install_verynginx()    


def exec_sys_cmd(cmd, accept_failed = False):
    print( cmd )
    ret = os.system( cmd )
    if  ret == 0:
        return ret
    else:
        if accept_failed == False:
            print('*** The installing stopped because something was wrong')
            exit(1)
        else:
            return False

def common_input( s ):
    if sys.version_info[0] == 3:
        return input( s )
    else:
        return raw_input( s )

def safe_pop(l):
    if len(l) == 0:
        return None
    else:
        return l.pop(0)

def show_help_and_exit():
    help_doc = 'usage: install.py <cmd> <args> ... \n\n\
install cmds and args:\n\
    install\n\
        all        :  install verynginx and openresty(default)\n\
        openresty  :  install openresty\n\
        verynginx  :  install verynginx\n\
    update\n\
        verynginx  :  update the installed verynginx\n\
    '
    print(help_doc)
    exit()


if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:], '', []) 
  
    cmd = safe_pop(args)
    if cmd == 'install':
        cmd = safe_pop(args)
        if cmd == 'all' or cmd == None:
            install_openresty()
            install_verynginx()
        elif cmd == 'openresty':
            install_openresty()
        elif cmd == 'verynginx':
            install_verynginx()
        else:
            show_help_and_exit()
    elif cmd == 'update':
        cmd = safe_pop(args)
        if cmd == 'verynginx':
            update_verynginx()
        else:
            show_help_and_exit()
    else:
        show_help_and_exit()

    print('*** All work finished successfully, enjoy it~')


else:
    print ('install.py had been imported as a module')

