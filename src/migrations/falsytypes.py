from src.configloader import settings, load_settings
from src.argparser import command_args
import logging
import shutil
import time
import json
import sys

logger = logging.getLogger("rcgcdw.migrations.falsytypes")
new_settings = settings.copy()


def run():
	change = False
	try:
		if "avatars" in new_settings:
			avatars = new_settings["avatars"]
			for key, value in avatars.items():
				if not value and value is not None:
					new_settings["avatars"][key] = None
					change = True
		if "event_appearance" in new_settings:
			events = new_settings["event_appearance"]
			for key, value in events.items():
				if not value.get("icon", None) and value.get("icon", None) is not None:
					new_settings["event_appearance"][key]["icon"] = None
					change = True
	except KeyError:
		logger.exception("Failed to migrate falsy types.")
		sys.exit(1)
	if change:
		logger.info("Running migration falsytypes")
		shutil.copy(command_args.settings.name, "{}.{}.bak".format(command_args.settings.name, int(time.time())))
		with open(command_args.settings.name, "w", encoding="utf-8") as new_write:
			new_write.write(json.dumps(new_settings, indent=4))
		load_settings()
		logger.info("Migration falsytypes has been successful.")
	else:
		logger.debug("Ignoring migration falsytypes")


run()
