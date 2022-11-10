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


import logging
from src.discord.message import DiscordMessage
from src.api import formatter
from src.api.context import Context
from src.api.util import embed_helper, compact_author, clean_link, sanitize_to_markdown, sanitize_to_url


# TemplateClassification - https://community.fandom.com/wiki/Help:Template_types
# templateclassification/tc-changed - Changing the type of a template


@formatter.embed(event="templateclassification/tc-changed")
def embed_templateclassification_changed(ctx: Context, change: dict) -> DiscordMessage:
    embed = DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url)
    embed_helper(ctx, embed, change, set_desc=False)
    embed["url"] = ctx.client.create_article_path(sanitize_to_url(change["title"]))
    embed["title"] = ctx._("Changed the type of {article}").format(article=sanitize_to_markdown(change["title"]))
    embed["description"] = ctx._("Type changed from {old} to {new}").format(
        old=change["logparams"]["oldtype"], new=change["logparams"]["newtype"])
    return embed


@formatter.compact(event="templateclassification/tc-changed")
def compact_templateclassification_changed(ctx: Context, change: dict):
    author, author_url = compact_author(ctx, change)
    link = clean_link(ctx.client.create_article_path(sanitize_to_url(change["title"])))
    content = ctx._(
        "[{author}]({author_url}) changed the type of [{article}]({article_url}) from {old} to {new}").format(
        author=author, author_url=author_url, article=sanitize_to_markdown(change["title"]), article_url=link,
        old=change["logparams"]["oldtype"], new=change["logparams"]["newtype"])
    return DiscordMessage(ctx.message_type, ctx.event, ctx.webhook_url, content=content)
