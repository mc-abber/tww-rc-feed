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
import datetime
from src.discord.message import DiscordMessage
from src.api import formatter
from src.api.context import Context
from src.api.util import embed_helper, sanitize_to_url, parse_mediawiki_changes, clean_link, compact_author, \
	sanitize_to_markdown, compact_summary

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
	embed["title"] = sanitize_to_markdown(change["filter"])
	embed["url"] = ctx.client.create_article_path("Special:AbuseLog/{entry}".format(entry=change["id"]))
	embed.add_field(ctx._("Title"), "[{target}]({target_url})".format(target=change.get("title", ctx._("Unknown")),
		target_url=clean_link(ctx.client.create_article_path(sanitize_to_url(change.get("title", ctx._("Unknown")))))), inline=True)
	embed.add_field(ctx._("Performed"), abusefilter_actions(change["action"], ctx._, change["action"]), inline=True)
	embed.add_field(ctx._("Action taken"), "\n".join([abusefilter_results(result, ctx._, result) for result in results]))
	embed_helper(ctx, embed, change, is_anon=abuse_filter_is_ip(change), set_desc=False)
	return embed


@formatter.compact(event="abuselog")
def compact_abuselog(ctx: Context, change: dict):
	results = change["result"].split(",")
	action = abuselog_action(results)
	author, author_url = compact_author(ctx, change, is_anon=abuse_filter_is_ip(change))
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

# rights/blockautopromote - AbuseFilter filter block auto promote
def block_expiry(change: dict, ctx: Context) -> str:
    if change["logparams"]["duration"] in ["infinite", "indefinite", "infinity", "never"]:
        return ctx._("for infinity and beyond")
    else:
        if "expiry" in change["logparams"]:
            expiry_date_time_obj = datetime.datetime.strptime(change["logparams"]["expiry"], '%Y-%m-%dT%H:%M:%SZ')
            timestamp_date_time_obj = datetime.datetime.strptime(change["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
            timedelta_for_expiry = (expiry_date_time_obj - timestamp_date_time_obj).total_seconds()
        elif isinstance(change["logparams"]["duration"], int):
            timedelta_for_expiry = change["logparams"]["duration"]
        else:
            return change["logparams"]["duration"]  # Temporary? Should be rare? We will see in testing
        years, days, hours, minutes = timedelta_for_expiry // 31557600, timedelta_for_expiry % 31557600 // 86400, \
                                        timedelta_for_expiry % 86400 // 3600, timedelta_for_expiry % 3600 // 60
        if not any([years, days, hours, minutes]):
            return ctx._("for less than a minute")
        time_names = (
            ctx.ngettext("year", "years", years), ctx.ngettext("day", "days", days), ctx.ngettext("hour", "hours", hours),
            ctx.ngettext("minute", "minutes", minutes))
        final_time = []
        for num, timev in enumerate([years, days, hours, minutes]):
            if timev:
                final_time.append(
                    ctx._("for {time_number} {time_unit}").format(time_unit=time_names[num], time_number=int(timev)))
        return ctx._(", ").join(final_time)


@formatter.embed(event="rights/blockautopromote", mode="embed")
def embed_rights_blockautopromote(ctx, change):
    embed = DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url)
    user = change["title"].split(':', 1)[1]
    try:
        ipaddress.ip_address(user)
        embed["url"] = ctx.client.create_article_path("Special:Contributions/{user}".format(user=user))
    except ValueError:
        embed["url"] = ctx.client.create_article_path(sanitize_to_url(change["title"]))
    embed["title"] = ctx._("Blocked autopromotion of {user} {time}").format(user=user, time=block_expiry(change, ctx))
    embed_helper(ctx, embed, change)
    return embed


@formatter.compact(event="rights/blockautopromote", mode="compact")
def compact_rights_blockautopromote(ctx, change):
    user = change["title"].split(':', 1)[1]
    restriction_description = ""
    author, author_url = compact_author(ctx, change)
    parsed_comment = compact_summary(ctx)
    try:
        ipaddress.ip_address(user)
        link = clean_link(ctx.client.create_article_path("Special:Contributions/{user}".format(user=user)))
    except ValueError:
        link = clean_link(ctx.client.create_article_path(sanitize_to_url(change["title"])))
    content = ctx._(
        "[{author}]({author_url}) blocked the autopromotion of [{user}]({user_url}) {time}{comment}").format(author=author,
                                                                                                          author_url=author_url,
                                                                                                          user=sanitize_to_markdown(user),
                                                                                                          time=block_expiry(
                                                                                                              change, ctx),
                                                                                                          user_url=link,
                                                                                                          comment=parsed_comment)
    return DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url, content=content)


# rights/restoreautopromote - AbuseFilter filter restore auto promote

@formatter.embed(event="rights/restoreautopromote", mode="embed")
def embed_rights_restoreautopromote(ctx, change):
    embed = DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url)
    embed["url"] = ctx.client.create_article_path(sanitize_to_url(change["title"]))
    user = change["title"].split(':', 1)[1]
    embed["title"] = ctx._("Restored autopromotion of {user}").format(user=sanitize_to_markdown(user))
    embed_helper(ctx, embed, change)
    return embed


@formatter.compact(event="rights/restoreautopromote")
def compact_rights_restoreautopromote(ctx, change):
    author, author_url = compact_author(ctx, change)
    link = clean_link(ctx.client.create_article_path(sanitize_to_url(change["title"])))
    user = change["title"].split(':', 1)[1]
    parsed_comment = compact_summary(ctx)
    content = ctx._("[{author}]({author_url}) restored the autopromotion capability of [{user}]({user_url}){comment}").format(author=author,
                                                                                                   author_url=author_url,
                                                                                                   user=sanitize_to_markdown(user),
                                                                                                   user_url=link,
                                                                                                   comment=parsed_comment)
    return DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url, content=content)
