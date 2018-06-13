scriptExtension.importPreset("RuleSupport")
scriptExtension.importPreset("RuleSimple")

from openhab.triggers import ChannelEventTrigger,item_triggered,ITEM_UPDATE, ItemCommandTrigger
from openhab.log import logging
from openhab.actions import Pushover

class rule_xiaomi_switch_slaapkamer_all_off(SimpleRule):
    def __init__(self):
        self.device_1 = "mihome:sensor_switch:158d00016c0af6:button"
        self.device_2 = "mihome:sensor_switch:158d000210bee8:button"
        self.triggers = [ 
                            ChannelEventTrigger(channelUID=self.device_1, event="SHORT_PRESSED"),
                           # ChannelEventTrigger(channelUID=self.device_1, event="DOUBLE_PRESSED"),
                            ChannelEventTrigger(channelUID=self.device_1, event="LONG_PRESSED"),
                          #  ChannelEventTrigger(channelUID=self.device_1, event="LONG_RELEASED")
                            ChannelEventTrigger(channelUID=self.device_2, event="SHORT_PRESSED"),
                           # ChannelEventTrigger(channelUID=self.device_2, event="DOUBLE_PRESSED"),
                            ChannelEventTrigger(channelUID=self.device_2, event="LONG_PRESSED")
                          #  ChannelEventTrigger(channelUID=self.device_2, event="LONG_RELEASED")
                        ]
    # maak 4 modules
    def execute(self, module, input):
        triggered_event = str(input['event']).replace(self.device + " triggered ", "")
        logging.info("SWITCH INGEDRUKT: " + triggered_event)

        if triggered_event == "SHORT_PRESSED":
            if items.rule_xiaomi_switch_slaapkamer_all_off_timer == ON:
                logging.info("*** Timer cancelled...")    
                events.postUpdate("rule_xiaomi_switch_slaapkamer_all_off_timer", "OFF")
                Pushover.pushover("All off timer cancelled...", "Telefoon_prive_rick01")
            else:
                # toggle bedroom light
                
                logging.info("!!! Timer not running...")
                #Pushover.pushover("All off timer not running...", "Telefoon_prive_rick01")
                
        elif triggered_event == "DOUBLE_PRESSED":

            # toggle bedroom light (sfeerlicht)
            pass

        elif triggered_event == "LONG_PRESSED":
            # check if items.rule_xiaomi_switch_slaapkamer_all_off_timer is OFF (or NULL)
            if items.rule_xiaomi_switch_kantoor_all_off_timer != ON:
                events.sendCommand("rule_xiaomi_switch_slaapkamer_all_off_timer", "ON")
                Pushover.pushover("ALLES UIT KNOP: Timer gestart", "Telefoon_prive_rick01")
                logging.info("*** All off timer started (60 seconds)")
            else:
                logging.info("*** All off timer is already running (<60 seconds)")
                Pushover.pushover("All off timer is already running...", "Telefoon_prive_rick01")
                pass
        elif triggered_event == "LONG_RELEASED":
            pass
            
automationManager.addRule(rule_xiaomi_switch_slaapkamer_all_off())

class rule_all_off_execute(SimpleRule):
    def __init__(self):
        self.triggers = [ItemCommandTrigger("rule_xiaomi_switch_slaapkamer_all_off_timer", command="OFF") ]
    def execute(self, module, input):
        logging.info("rule_all_off_execute running.....")
        
        group = itemRegistry.getItem("settings_all_off_selection")
        for item_setting in group.getAllMembers():
            # get corresponding setting
            if str(item_setting.state) == "ON":
                #logging.info("*** Processing setting item: '" + item_setting.name + "'")
                substring_setting           = "_setting_all_off"
                substring_actuator          = "_toggle"
                #substring_actuator_computer = "_turn_off"       # hoe maak ik een toggle
                # validate item_setting, should contain substring
                if item_setting.name.endswith(substring_setting):
                    item_actuator_name = item_setting.name[:-len(substring_setting)] + substring_actuator
                    #validate if item_actuator exists
                    if item_actuator_name in items:
                        item_actuator_state = items[item_actuator_name]
                        if item_actuator_state != OFF:
                            logging.info("*** Item'" + item_actuator_name + "' is '" + str(item_actuator_state) + "', turning item OFF")
                            events.sendCommand(item_actuator_name,"OFF")
                        else:
                            #logging.info("!!! Item'" + item_actuator_name + "' is '" + str(item_actuator_state) + "', NOT TURNING ITEM OFF")
                            pass
                    else:
                        logging.info("!!! Item '" + item_actuator_name + "' doesn't exist! - Not processsing item yet") # should be send to whatapp / pushover
                else:
                    # log error / to whatsapp / pushover (v2)
                    pass
        Pushover.pushover("ALLES UIT KNOP: Uitgevoerd", "Telefoon_prive_rick01")
automationManager.addRule(rule_all_off_execute())

# class rule_remote_3_a_test(SimpleRule):
#     def __init__(self):
#         self.triggers = [ ChannelEventTrigger(channelUID="rfxcom:lighting4:d10d8fa9:518143") ]
#     def execute(self, module, input):
#         logging.info("Rule rule_remote_3_a_test started...")
#         logging.info(input)
# automationManager.addRule(rule_remote_3_a_test())

@item_triggered("remote_3_a_1_command_id", ITEM_UPDATE)
@item_triggered("remote_3_a_2_command_id", ITEM_UPDATE)
def rule_remote_3_a_command_id_updated():
    logging.info("Rule rule_remote_3_a_command_id_updated running...")
    events.sendCommand("light_keuken_dimmer_plafond","ON")

@item_triggered("remote_3_b_1_command_id", ITEM_UPDATE)
@item_triggered("remote_3_b_2_command_id", ITEM_UPDATE)
def rule_remote_3_b_command_id_updated():
    logging.info("Rule remote_3_b_command_id running...")
    events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_1_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_1_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_1_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_1_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")




# @item_triggered("remote_2_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_2_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_2_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_2_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_2_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_2_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_2_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_2_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")




# @item_triggered("remote_3_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_3_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_3_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_3_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_3_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_3_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_3_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_3_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")




# @item_triggered("remote_4_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_4_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_4_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_4_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_4_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_4_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_4_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_4_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")




# @item_triggered("remote_5_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_5_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_5_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_5_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_5_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_5_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_5_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_5_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")