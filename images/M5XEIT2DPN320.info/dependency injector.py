#https://stackoverflow.com/questions/58993788/how-to-allow-relative-import-when-using-importlib-to-load-a-module
import sys
import importlib.abc
import sys
import types

class DependencyInjectorFinder(importlib.abc.MetaPathFinder):
    def __init__(self, loader):
        # we'll write the loader in a minute, hang tight
        self._loader = loader
    def find_spec(self, fullname, path, target=None):
        """Attempt to locate the requested module
        fullname is the fully-qualified name of the module,
        path is set to __path__ for sub-modules/packages, or None otherwise.
        target can be a module object, but is unused in this example.
        """
        if self._loader.provides(fullname):
            return self._gen_spec(fullname)
    def _gen_spec(self, fullname):
        spec = importlib.machinery.ModuleSpec(fullname, self._loader)
        return spec

class DependencyInjectorLoader(importlib.abc.Loader):
    _COMMON_PREFIX = "myapp.virtual."
    def __init__(self):
        self._services = {}
        # create a dummy module to return when Python attempts to import
        # myapp and myapp.virtual, the :-1 removes the last "." for
        # aesthetic reasons :) 
        self._dummy_module = types.ModuleType(self._COMMON_PREFIX[:-1])
        # set __path__ so Python believes our dummy module is a package
        # this is important, since otherwise Python will believe our
        # dummy module can have no submodules
        self._dummy_module.__path__ = []
    def provide(self, service_name, module):
        """Register a service as provided via the given module
        A service is any Python object in this context - an imported module,
        a class, etc."""
        self._services[service_name] = module
    def provides(self, fullname):
        if self._truncate_name(fullname) in self._services:
            return True
        else:
            # this checks if we should return the dummy module,
            # since this evaluates to True when importing myapp and
            # myapp.virtual
            return self._COMMON_PREFIX.startswith(fullname)
    def create_module(self, spec):
        """Create the given module from the supplied module spec
        Under the hood, this module returns a service or a dummy module,
        depending on whether Python is still importing one of the names listed
        in _COMMON_PREFIX.
        """
        service_name = self._truncate_name(spec.name)
        if service_name not in self._services:
            # return our dummy module since at this point we're loading
            # *something* along the lines of "myapp.virtual" that's not
            # a service
            return self._dummy_module
        module = self._services[service_name]
        return module
    def exec_module(self, module):
        """Execute the given module in its own namespace
        This method is required to be present by importlib.abc.Loader,
        but since we know our module object is already fully-formed,
        this method merely no-ops.
        """
        pass
    def _truncate_name(self, fullname):
        """Strip off _COMMON_PREFIX from the given module name
        Convenience method when checking if a service is provided.
        """
        return fullname[len(self._COMMON_PREFIX):]

class DependencyInjector:
    """
    Convenience wrapper for DependencyInjectorLoader and DependencyInjectorFinder.
    """
    def __init__(self):
        self._loader = DependencyInjectorLoader()
        self._finder = DependencyInjectorFinder(self._loader)
    def install(self):
        sys.meta_path.append(self._finder)
    def provide(self, service_name, module):
        self._loader.provide(service_name, module)