# -*- coding: utf-8 -*-

# Recent changes Goat compatible Discord webhook is a project for using a webhook as recent changes page from MediaWiki.
# Copyright (C) 2020 Frisk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging, gettext
from configloader import settings
from misc import datafile, WIKI_SCRIPT_PATH

# Initialize translation

t = gettext.translation('discussions', localedir='locale', languages=[settings["lang"]])
_ = t.gettext

# Create a custom logger

discussion_logger = logging.getLogger("rcgcdw.disc")

fetch_url = "https://services.fandom.com/discussion/{wikiid}/posts?sortDirection=descending&sortKey=creation_date&limit={limit}".format(wikiid=settings["fandom_discussions"]["wiki_id"], limit=settings["fandom_discussions"]["limit"])

def fetch_discussions():
	pass