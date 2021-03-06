from core.log import logging, LOG_PREFIX
from core.rules import rule
from core.triggers import when

# STARTUP RULE SHOULD BE ADDED...
@rule("Licht gang automatisch uit")
@when("Item light_gang_plafond_toggle changed")
@when("Item sensor_motion_gang_voordeur_motion_status received update")
@when("Item sensor_motion_gang_woonkamer_motion_status received update")
@when("Item timer_rule_automate_gang_licht_init_hardware received command OFF")
def rule_automate_gang_licht(event):
    function = 'rule_automate_gang_licht'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.info("rule_automate_gang_licht started")
    if str(items.timer_rule_automate_gang_licht_off) == "NULL":                                                                     # initialize timer (set to off, so it's initialized)
        events.sendCommand("timer_rule_automate_gang_licht_off","OFF")                
    if str(items.sensor_motion_gang_voordeur_motion_status) == "NULL":                                                              # initializing hardware stuff
        events.sendCommand("sensor_motion_gang_voordeur_motion_status","OFF")   
    if str(items.sensor_motion_gang_woonkamer_motion_status) == "NULL":
        events.sendCommand("sensor_motion_gang_woonkamer_motion_status","OFF")  
    if str(items.light_gang_plafond_toggle) == "NULL":                                                                              
        self.log.debug("@@@@ rule_automate_gang_licht: Light device is in unknown state, rescheduling rule")
        events.sendCommand("timer_rule_automate_gang_licht_init_hardware","ON")                                                     # Reschedule in 30 seconds until the items are in a proper state
    else:
        if str(items.timer_rule_automate_gang_licht_init_hardware) != "OFF":                                                        # Turn off timer if it's still running
            events.postUpdate("timer_rule_automate_gang_licht_init_hardware","OFF")
        if str(items.light_gang_plafond_toggle) == "ON":                                                                            # if light is on, but timer is off, set timer
            if str(items.timer_rule_automate_gang_licht_off) == "OFF":
                log.debug("@@@@ rule_automate_gang_licht: Light is on but timer is off, setting timer to 2 minutes...")
                events.sendCommand("timer_rule_automate_gang_licht_off","ON")
            else:
                if "motion" in str(event):                                                                                          # timer is on. check if event is triggered by motion, if so, enable timer                         
                    log.debug("@@@@ rule_automate_gang_licht: Motion sensors triggered, extending timer with 2 minutes...")
                    events.sendCommand("timer_rule_automate_gang_licht_off","ON")               

@rule("Licht gang automatisch uit - timer expired")
@when("Item timer_rule_automate_gang_licht_off changed from ON to OFF")                                                             # Licht moet uit na 2 minuten, de uitvoer in het script is het meest compleet.
def rule_automate_gang_licht_timer_expired(event):
    function = 'rule_automate_gang_licht_timer_expired'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.debug("@@@@ Timer has expired: timer_rule_automate_gang_licht_off")
    events.sendCommand("light_gang_plafond_toggle", "OFF")