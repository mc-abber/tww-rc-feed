#  This file is part of Recent changes Goat compatible Discord webhook (RcGcDw).
#
#  RcGcDw is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  RcGcDw is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with RcGcDw.  If not, see <http://www.gnu.org/licenses/>.

import ipaddress
import logging
from src.discord.message import DiscordMessage
from src.api import formatter
from src.api.context import Context
from src.api.util import embed_helper, sanitize_to_url, parse_mediawiki_changes, clean_link, compact_author, sanitize_to_markdown

# Order results from most drastic first to less drastic last
abuselog_results = ["degroup", "blockautopromote", "rangeblock", "block", "disallow", "throttle", "warn", "tag", ""]
abusefilter_results = lambda string, _, default: {"degroup": _("**Removed from privileged groups**"), "blockautopromote": _("**Removed autopromoted groups**"), "rangeblock": _("**IP range blocked**"), "block": _("**Blocked user**"), "disallow": _("Disallowed the action"), "throttle": _("Throttled actions"), "warn": _("Warning issued"), "tag": _("Tagged the edit"), "": _("None")}.get(string, default)
abusefilter_actions = lambda string, _, default: {"edit": _("Edit"), "upload": _("Upload"), "move": _("Move"), "stashupload": _("Stash upload"), "delete": _("Deletion"), "createaccount": _("Account creation"), "autocreateaccount": _("Auto account creation")}.get(string, default)

logger = logging.getLogger("extensions.base")

# AbuseFilter - https://www.mediawiki.org/wiki/Special:MyLanguage/Extension:AbuseFilter
# Processing Abuselog LOG events, separate from RC logs


def abuselog_action(results):
	action = "unknown"
	for result in abuselog_results:
		if result in results:
			action = "abuselog/{}".format(result)
			break
	return action


def abuse_filter_is_ip(change):
	is_ip = False
	try:
		ipaddress.ip_address(change["user"])
	except ValueError:
		pass
	else:
		is_ip = True
	return is_ip


@formatter.embed(event="abuselog")
def embed_abuselog(ctx: Context, change: dict):
	results = change["result"].split(",")
	action = abuselog_action(results)
	embed = DiscordMessage(ctx.message_type, action, ctx.webhook_url)
	author = change["user"]
	author_url = ctx.client.create_article_path("User:{}".format(sanitize_to_url(change["user"])))
	if abuse_filter_is_ip(change):
		author_url = ctx.client.create_article_path("Special:Contributions/{user}".format(user=sanitize_to_url(change["user"])))
		ip_mapper = ctx.client.get_ipmapper()
		logger.debug("current user: {} with cache of IPs: {}".format(change["user"], ip_mapper.keys()))
		if change["user"] not in list(ip_mapper.keys()):
			try:
				contibs = ctx.client.make_api_request(
					"?action=query&format=json&list=usercontribs&uclimit=max&ucuser={user}&ucstart={timestamp}&ucprop=".format(
						user=sanitize_to_url(change["user"]), timestamp=change["timestamp"]), "query",
					"usercontribs")
			except (ServerError, MediaWikiError):
				logger.warning("WARNING: Something went wrong when checking amount of contributions for given IP address")
				if ctx.settings.get("hide_ips", False):
					author = ctx._("Unregistered user")
				else:
					author = change["user"] + "(?)"
			else:
				ip_mapper[change["user"]] = len(contibs)
				logger.debug("Current params user {} and state of map_ips {}".format(change["user"], ip_mapper))
				if ctx.settings.get("hide_ips", False):
					author = ctx._("Unregistered user")
				else:
					author = "{author} ({contribs})".format(author=change["user"], contribs=len(contibs))
		else:
			logger.debug("Current params user {} and state of map_ips {}".format(change["user"], ip_mapper))
			author = "{author} ({amount})".format(
				author=change["user"] if ctx.settings.get("hide_ips", False) is False else ctx._("Unregistered user"),
				amount=ip_mapper[change["user"]])
	embed.set_author(author, author_url)
	embed["title"] = sanitize_to_markdown(change["filter"])
	embed["url"] = ctx.client.create_article_path("Special:AbuseLog/{entry}".format(entry=change["id"]))
	embed.add_field(ctx._("Title"), "[{target}]({target_url})".format(target=change.get("title", ctx._("Unknown")),
		target_url=clean_link(ctx.client.create_article_path(sanitize_to_url(change.get("title", ctx._("Unknown")))))), inline=True)
	embed.add_field(ctx._("Performed"), abusefilter_actions(change["action"], ctx._, change["action"]), inline=True)
	embed.add_field(ctx._("Action taken"), ctx._(", ").join([abusefilter_results(result, ctx._, result) for result in results]))
	return embed


@formatter.compact(event="abuselog")
def compact_abuselog(ctx: Context, change: dict):
	results = change["result"].split(",")
	action = abuselog_action(results)
	author = change["user"]
	author_url = clean_link(ctx.client.create_article_path("User:{user}".format(user=sanitize_to_url(change["user"]))))
	if abuse_filter_is_ip(change):
		author_url = clean_link(ctx.client.create_article_path("Special:Contributions/{user}".format(user=sanitize_to_url(change["user"]))))
		if ctx.settings.get("hide_ips", False):
			author = ctx._("Unregistered user")
	message = ctx._("[{author}]({author_url}) triggered *[{abuse_filter}]({details_url})*, performing the action \"{action}\" on *[{target}]({target_url})* - action taken: {result}.").format(
		author=author, author_url=author_url, abuse_filter=sanitize_to_markdown(change["filter"]),
		details_url=clean_link(ctx.client.create_article_path("Special:AbuseLog/{entry}".format(entry=change["id"]))),
		action=abusefilter_actions(change["action"], ctx._, change["action"]), target=change.get("title", ctx._("Unknown")),
		target_url=clean_link(ctx.client.create_article_path(sanitize_to_url(change.get("title", ctx._("Unknown"))))),
		result=ctx._(", ").join([abusefilter_results(result, ctx._, result) for result in results]))
	return DiscordMessage(ctx.message_type, action, ctx.webhook_url, content=message)

# abusefilter/modify - AbuseFilter filter modification


@formatter.embed(event="abusefilter/modify")
def embed_abuselog_modify(ctx: Context, change: dict):
	embed = DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url)
	embed_helper(ctx, embed, change)
	embed["url"] = ctx.client.create_article_path(
		"Special:AbuseFilter/history/{number}/diff/prev/{historyid}".format(number=change["logparams"]['newId'],
																			historyid=change["logparams"]["historyId"]))
	embed["title"] = ctx._("Edited abuse filter number {number}").format(number=change["logparams"]['newId'])
	return embed


@formatter.compact(event="abusefilter/modify")
def compact_abuselog_modify(ctx: Context, change: dict):
	author, author_url = compact_author(ctx, change)
	link = clean_link(ctx.client.create_article_path(
		"Special:AbuseFilter/history/{number}/diff/prev/{historyid}".format(number=change["logparams"]['newId'],
																			historyid=change["logparams"][
																				"historyId"])))

	content = ctx._("[{author}]({author_url}) edited abuse filter [number {number}]({filter_url})").format(author=author,
																									   author_url=author_url,
																									   number=change[
																										   "logparams"][
																										   'newId'],
																									   filter_url=link)
	return DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url, content=content)

# abusefilter/create - AbuseFilter filter creation


@formatter.embed(event="abusefilter/create")
def embed_abuselog_create(ctx: Context, change: dict):
	embed = DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url)
	embed_helper(ctx, embed, change)
	embed["url"] = ctx.client.create_article_path("Special:AbuseFilter/{number}".format(number=change["logparams"]['newId']))
	embed["title"] = ctx._("Created abuse filter number {number}").format(number=change["logparams"]['newId'])
	return embed


@formatter.compact(event="abusefilter/create")
def compact_abuselog_create(ctx: Context, change: dict):
	author, author_url = compact_author(ctx, change)
	link = clean_link(
		ctx.client.create_article_path("Special:AbuseFilter/{number}".format(number=change["logparams"]['newId'])))
	content = ctx._("[{author}]({author_url}) created abuse filter [number {number}]({filter_url})").format(author=author,
																										author_url=author_url,
																										number=change[
																											"logparams"][
																											'newId'],
																										filter_url=link)
	return DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url, content=content)
