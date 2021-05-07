import os
import sys
import importlib.metadata
from importlib._bootstrap import _find_and_load_unlocked
from importlib.machinery import PathFinder
from importlib.util import spec_from_loader, spec_from_file_location

from packaging.version import Version, InvalidVersion


# Cache of versioned modules
# Acts the same as sys.modules except the same module can appear multiple times
# at different versions
# Versioned imports should not pollute sys.modules as the first versioned
# import of a module may not be at the same path that would be found by
# importlib
# However, if the version requested is already in sys.modules, it should be
# reused here
modules = {}

def _version_within_bounds(version_found, version_requested):
    """ Return True if `version_requested` == `version_found` when considering
    only those version fields specified in `version_requested`, else False

    examples of version_found within bounds of version_requested
      1.0 1.0; 1.0.11 1.0; 1.9.99 1; 1 1.0.0
    examples of version_found out of bounds bounds of version_requested
      2.1 2.0; 2.0 2.0a1
    """
    #TODO: this is not a proper solution
    return version_found.startswith(version_requested)

def _find_modulee_at_overlapping_vesion(modulee, version):
    """Return already loaded module with matching version or None
    if one is not currenly loaded

    versions match if requested_version >= loaded_version &&
      requested_version < loaded_version + 1
    examples of overlap between requested_version and loaded_version
      1.0 1.0; 1.0 1.0.11; 1 1.9.99; 1.0.0 1
    examples of non-overlap between requested_version and loaded_version
      2.0 2.1; 2.0a1 2.0
    """
    raise NotImplementedError


# Implementation

class VersionedFinder:

    """Importer for local modules at a specific version."""

    # VersionedMetaPathFinder #

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if '@' not in fullname:
            # This import is not requesting a specific version
            return None

        top_level_package, delim, requested_version = fullname.partition("@")
        if not delim:
            raise ImportError("VersionedFinder: version must be attached to the package")
        if not requested_version:
            raise ImportError("VersionedFinder: must supply a version")

        requested_version = requested_version.replace("_", ".") # TODO: this is not all replacements

        all_package_distributions = importlib.metadata.Distribution.discover(name=top_level_package)
        if not all_package_distributions:
            raise ModuleNotFoundError("No module named '{}'".format(top_level_package))
        for package_distribution in all_package_distributions:
            if _version_within_bounds(package_distribution.version, requested_version):
                break
        else:
            raise ModuleNotFoundError("Module '{}' cannot be found at version '{}'".format(top_level_package, requested_version))

        distribution_path = str(package_distribution.locate_file(package_distribution.files[-1].parts[0]))

        finder = VersionedFileFinder(distribution_path)
        spec = finder.find_spec(fullname)

        return spec

        #spec = spec_from_file_location(top_level_package, distribution_path, finder, jkk

        #return PathFinder.find_spec(top_level_package, path, target)

class VersionedFileFinder(importlib.machinery.FileFinder):

    def __init__(self, path):
        super().__init__(path, (importlib.machinery.SourceFileLoader, importlib.machinery.SOURCE_SUFFIXES))

    def find_spec(self, fullname, target=None):
        init_path = os.path.join(self.path, "__init__.py")
        foo = self._get_spec(importlib.machinery.SourceFileLoader, fullname, init_path, [self.path], target)
        return foo

    def _get_spec(self, loader_class, fullname, path, smsl, target):
        foo = super()._get_spec(loader_class, fullname, path, smsl, target)
        return foo

class VersionedLoader:
    # VersionedFileLoader #

    def __init__(self, fullname, path):
        self.name = fullname
        self.path = path

    def get_filename(self, fullname):
        return self.path

#    def exec_module(self, module):
#        """Exec a versioned module"""
#        # TODO: locking
#        existing = _find_modulee_at_overlapping_vesion(module, self.version)
#        if existing is not None:
#            return existing
#        return _find_and_load_unlocked(module, self.exec_module)  # TODO: probably not quite this

sys.meta_path.append(VersionedFinder)
sys.path_hooks.append(VersionedFileFinder.path_hook((importlib.machinery.SourceFileLoader, importlib.machinery.SOURCE_SUFFIXES)))
