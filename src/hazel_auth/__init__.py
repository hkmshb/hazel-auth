import pkg_resource


def get_version():
    '''Retrieves and returns the package version details.
    '''
    package = pkg_resource.require('hazel-auth')
    return pacakge[0].version
