#!/usr/bin/env python
# _*_ coding: utf-8 _*_


"""
File:       pytv.py
Version:    1.0
Author:     Rubén Hortas <rubenhortas@gmail.com>
Website:    http://rubenhortas.blogspot.com.es
Github:     http://github.com/rubenhortas/pytv
License:    CC BY-NC-SA 3.0
            http://creativecommons.org/licenses/by-nc-sa/3.0/
"""

import argparse
import os
import subprocess
import textwrap


def Check_prog(prog):
    """
    Check_prog(prog)
        Comprueba que un programa esté instalado.
    Args:
        - prog: (string) Programa a ejecutar.
    """
    try:
        devnull = open(os.devnull)
        subprocess.Popen([prog], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print '[ERROR]: %s no está instalado' % prog
            exit(1)


def Watch(canal):
    """
    Watch(canal)
        Obtiene la información del canal (Nombre y url del streaming).
    Args:
        - canal: (string) Canal a visualizar.
    """

    # En python no hay "switch", pero se puede emular con un diccionario
    d_chan = {
        'antena3': ['Antena 3', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-antena3_1'],
        'lasexta': ['La sexta', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-lasexta_1'],
        'nova': ['Nova', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-eventos6_1'],
        'xplora': ['Xplora', 'rtmp://antena3fms35geobloqueolivefs.fplive.net:1935/antena3fms35geobloqueolive-live/stream-xplorageo_1']
    }

    c_info = d_chan.get(canal, None)

    if c_info:
        Launch_mplayer(c_info)
    else:
        print '[ERROR] El canal ' + canal + 'no está incluido en' \
                + 'la lista'
        print '\tConsulta la lista de canales soportados en la ayuda.'
        exit(1)


def Launch_mplayer(c_info):
    """
    Launch_mplayer(url)
        Ejecuta mplayer en background.

    Argumentos:
        url -- (string) Dirección del streaming.
    """
    n_canal = c_info[0]
    url = c_info[1]

    devnull = open(os.devnull, 'w')
    try:
        print 'Canal: %s' % n_canal
        p = subprocess.Popen(['mplayer', url], stdout=devnull,
                             stderr=devnull, shell=False)
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
                                     antena3    - Antena 3
                                     lasexta    - La Sexta
                                     nova       - Nova
                                     xplora     - Xplora
                                     '''))

    parser.add_argument(dest='canal',
                        help=" Canal para ver")

    args = parser.parse_args()
    canal = args.canal

    # Imprimir un pequeño header
    os.system('clear')  # Limpiar pantalla
    print '========'
    print '= pytv ='
    print '========'

    # Comprobar que están instalados rtmpdump y mplayer
    Check_prog('rtmpdump')
    Check_prog('mplayer')

    # Ver el streaming
    Watch(canal)
