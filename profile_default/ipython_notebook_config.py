#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Configuration file for ipython-notebook.

c = get_config()

# Include our extra templates
c.NotebookApp.extra_template_paths = ['/srv/templates/']
