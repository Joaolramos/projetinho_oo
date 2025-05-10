#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
# Adiciona o diretório principal ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from template.template import *
if __name__ == "__main__":
    app = App()
    app.run()
