# -*- coding: utf-8 -*-

from gluon.contrib.appconfig import AppConfig

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")


appconfig = AppConfig(reload=True)

