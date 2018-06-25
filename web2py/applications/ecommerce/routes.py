# -*- coding: utf-8 -*-

from gluon.fileutils import abspath
from gluon.languages import read_possible_languages


possible_languages = read_possible_languages(abspath('applications', app, 'languages'))
routers = {
    app: dict(
        default_language = 'pt-br',
        languages = [lang for lang in possible_languages if lang != 'default'],
    )
}
