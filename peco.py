# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals, )

from subprocess import Popen, PIPE, STDOUT


class Peco(object):
    def filter(self, source):
        peco_filterd = Popen(["peco", '--query', '"$LBUFFER"'], stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
        return peco_filterd.communicate(input=source)
