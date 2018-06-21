# -*- coding: utf-8 -*-

from gluon.contrib.appconfig import AppConfig
from gluon.storage import Storage
from gluon.tools import Auth

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")


appconfig = AppConfig(reload=True)


if request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb', lazy_tables=True)
    # ---------------------------------------------------------------------
    # store sessions and tickets in Memcache
    # ---------------------------------------------------------------------
    from gluon.contrib.gae_memcache import MemcacheClient
    from gluon.contrib.memdb import MEMDB
    cache.memcache = MemcacheClient(request)
    cache.ram = cache.disk = cache.memcache
    session.connect(request, response, db=MEMDB(cache.memcache.client))
else:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(appconfig.get('db.uri'),
             pool_size=appconfig.get('db.pool_site'),
             migrate_enabled=appconfig.get('db.migrate'),
             check_reserved=appconfig.get('db.migrate') and ['all'] or None,
             lazy_tables=appconfig.get('db.lazy'))


# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=appconfig.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
# auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else appconfig.get('smtp.server')
mail.settings.sender = appconfig.get('smtp.sender')
mail.settings.login = appconfig.get('smtp.login')
mail.settings.tls = appconfig.get('smtp.tls') or False
mail.settings.ssl = appconfig.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# response page configuration and default data
# -------------------------------------------------------------------------
response.page = Storage()
response.page.title = appconfig.get('app.name')
