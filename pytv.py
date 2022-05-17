#!/usr/bin/env python
# _*_ coding: utf-8 _*_


import argparse
import os
import subprocess
import textwrap
import sys


def check_program(prog):
    """
    check_program(prog)
        Comprueba que un programa esté instalado.
    Args:
        prog: (string) Programa a ejecutar.
    """
    try:
        devnull = open(os.devnull)
        subprocess.Popen([prog], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print '[ERROR]: %s no está instalado' % prog
            exit(1)


def watch(canal):
    """
    watch(canal)
        Obtiene la información del canal (Nombre y url del streaming).
    Args:
        canal: (string) Canal a visualizar.
    """

    # En python no hay "switch", pero se puede emular con un diccionario
    d_chan = {
        'antena3': ['Antena 3', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-antena3_1'],
        'lasexta': ['La sexta', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-lasexta_1'],
        'nova': ['Nova', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-eventos6_1'],
        'xplora': ['Xplora',
                   'rtmp://antena3fms35geobloqueolivefs.fplive.net:1935/antena3fms35geobloqueolive-live/stream-xplorageo_1']
    }

    info_canal = d_chan.get(canal, None)

    if info_canal:
        launch_mplayer(info_canal)
    else:
        print '[ERROR] El canal ' + canal + 'no está incluido en' \
              + 'la lista'
        print '\tConsulta la lista de canales soportados en la ayuda.'
        exit(1)


def launch_mplayer(info_canal):
    """
    launch_mplayer(url)
        Ejecuta mplayer en background.

    Args:
        info_canal: -(string) Dirección del streaming.
    """
    n_canal = info_canal[0]
    url = info_canal[1]

    devnull = open(os.devnull, 'w')
    try:
        print 'Canal: %s' % n_canal

        mp_cache = 10240  # in KB
        mplayer_order = 'mplayer -really-quiet -cache ' + str(mp_cache) \
                        + ' ' + url
        order = mplayer_order + ' ' + url

        subprocess.Popen([order], stdout=devnull,
                         stderr=devnull, shell=True)
        print
        print '(mplayer está ejecutándose en background.' \
              + 'Puedes cerrar esta ventana.)'
        print
        exit(0)
    except NameError:
        print "[ERROR]:", sys.exc_info()[0]
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Capturador de"
                                                 " televisión online",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''
                                     Lista de canales disponibles:
                                     antena3    Antena 3
                                     lasexta    La Sexta
                                     nova       Nova
                                     xplora     Xplora
                                     '''))

    parser.add_argument(dest='canal',
                        help=" Canal para ver")

    args = parser.parse_args()

    # Imprimir un pequeño header
    os.system('clear')  # Limpiar pantalla
    print '========'
    print '= pytv ='
    print '========'

    # Comprobar que están instalados rtmpdump y mplayer
    check_program('rtmpdump')
    check_program('mplayer')

    # Ver el streaming
    watch(args.canal)
