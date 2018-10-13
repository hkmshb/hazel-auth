import pkg_resources


def get_version():
    '''Retrieves and returns the package version details.
    '''
    package = pkg_resources.require('hazel-auth')
    return package[0].version


def configure_models():
    from hazel_db import meta
    from . import models

    meta.attach_model(models.User, meta.BASE)
    meta.attach_model(models.Role, meta.BASE)
    meta.attach_model(models.UserRole, meta.BASE)
    meta.attach_model(models.ActivityToken, meta.BASE)
