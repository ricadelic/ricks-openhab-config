from time import sleep

from org.slf4j import Logger, LoggerFactory

log = LoggerFactory.getLogger("org.openhab.core.automation.jsr223.jython.startup_delay")

log.info("Checking for initialized context")

while True:
    try:
        scriptExtension.importPreset("RuleSupport")
        if automationManager is not None:
            break
    except:
        log.info("Context not initialized yet... waiting 10s before checking again")
        sleep(10)

log.info("Context initialized... waiting 60s before allowing scripts to load")
sleep(60)
log.info("Complete")

