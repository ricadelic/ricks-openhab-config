import sys
from core import osgi
from org.slf4j import LoggerFactory



__all__ = []

oh1_actions = osgi.find_services("org.openhab.core.scriptengine.action.ActionService", None) or []
oh2_actions = osgi.find_services("org.eclipse.smarthome.model.script.engine.action.ActionService", None) or []

_module = sys.modules[__name__]
for s in oh1_actions + oh2_actions:
    action_class = s.actionClass
    name = action_class.simpleName
    setattr(_module, name, action_class)
    __all__.append(name)
    LoggerFactory.getLogger("org.openhab.core.automation.examples").info(str(action_class))
    LoggerFactory.getLogger("org.openhab.core.automation.examples").info(name)



