
# TESTING AREA
# scriptExtension.importPreset("RuleSupport")
# scriptExtension.importPreset("RuleSimple")

# from openhab.triggers import ItemStateChangeTrigger
# from openhab.log import logging

# class MyRule111(SimpleRule):
#     def __init__(self):
#         self.triggers = [ ItemStateChangeTrigger("test_switch") ]
#     def execute(self, module, input):
#        logging.info("test")
#        logging.info(input)
#        logging.info(input.get("newState"))
#        logging.info(input.get("oldState"))
# automationManager.addRule(MyRule111())


# from org.eclipse.smarthome.automation import *
# # from org.eclipse.smarthome.automation.module.script.rulesupport.shared import RuleSimple
# from org.eclipse.smarthome.config.core import Configuration



# scriptExtension.importPreset("RuleSupport")
# scriptExtension.importPreset("RuleSimple")


# class myRule(SimpleRule):
#     def execute(self, module, inputs):
#         print "Hello World from Jython"

# sRule = myRule(SimpleRule)
# sRule.setTriggers([Trigger("aTimerTrigger", "timer.GenericCronTrigger", Configuration({"cronExpression": "0/15 * * * * ?"}))])

# automationManager.addRule(sRule)

# from openhab.log import logging
# from openhab.triggers import item_triggered, ITEM_UPDATE, ITEM_CHANGE, ITEM_COMMAND

# @item_triggered("logitech_harmony_hub_current_activity",ITEM_CHANGE)
# def rule_harmony_hub_initialize():
#     logging.info("Running uninitialize harmony hub rule...")
#     if str(items.logitech_harmony_hub_current_activity) == "PowerOff":
#         events.postUpdate("logitech_harmony_hub_toggle", "OFF")
#     else:
#         events.postUpdate("logitech_harmony_hub_toggle", "ON")


# class MyRuleTest(SimpleRule):
#     def __init__(self):
#         self.triggers = [
#              Trigger("MyTrigger", "core.ItemStateUpdateTrigger", 
#                     Configuration({ "itemName": "TestString1"}))
#         ]

#     def execute(self, module, input):
#         events.postUpdate("test_switch", "ON")
# automationManager.addRule(MyRuleTest())


