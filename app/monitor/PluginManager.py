#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imp

class PluginManager(object):
    #path = "plugins"
    path = os.path.join(os.path.dirname(__file__), "Plugins")
    __plugins = []

    def __init__(self):
        pass

    def LoadAllPlugin(self):
        files = os.listdir(self.path)
        for f in files:
            if not f.endswith('.py') or f.startswith('_'):
                continue
            name = f[:-3]
            fh, filename, desc = imp.find_module(name, [self.path])
            try:
                module = imp.load_module(name, fh, filename, desc)
            finally:
                if fh: fh.close()

            if hasattr(module, "__all__"):
                attrs = [getattr(module, x) for x in module.__all__]
                self.__plugins.append(attrs[0]())

    def GetPluginByName(self, name):
        for plugin in self.__plugins:
            if name == plugin.name:
                return plugin
        return None



if __name__ == '__main__':
    m = PluginManager()
    m.LoadAllPlugin()
    module = m.GetPluginByName('Modbus')
    module.get()
