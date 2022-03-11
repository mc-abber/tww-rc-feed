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

import unittest
import importlib
import json

test_file = """{"cooldown":60,"wiki_url":"https://wreckit-woodhouse.fandom.com/","rc_enabled":true,"lang":"en","header":{"user-agent":"RcGcDw/{version}"},"limit":10,"webhookURL":"https://discordapp.com/api/webhooks/111111111111111111/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","limitrefetch":28,"wikiname":"Wreck It Woodhouse","avatars":{"connection_failed":"https://i.imgur.com/2jWQEt1.png","connection_restored":"","no_event":"","embed":"","compact":""},"ignored":["external","newusers/create","newusers/autocreate","newusers/create2","newusers/byemail","newusers/newusers"],"show_updown_messages":true,"ignored_namespaces":[],"overview":false,"overview_time":"00:00","send_empty_overview":false,"license_detection":true,"license_regex_detect":"\\\\{\\\\{(license|lizenz|licence|copyright)","license_regex":"\\\\{\\\\{(license|lizenz|licence|copyright)(\\\\ |\\\\|)(?P<license>.*?)\\\\}\\\\}","disallow_regexes":[],"wiki_bot_login":"","wiki_bot_password":"","show_added_categories":true,"show_bots":false,"show_abuselog":false,"hide_ips":false,"discord_message_cooldown":0,"auto_suppression":{"enabled":false,"db_location":":memory:"},"logging":{"version":1,"disable_existing_loggers":false,"formatters":{"standard":{"format":"%(name)s - %(levelname)s: %(message)s"}},"handlers":{"default":{"formatter":"standard","class":"logging.StreamHandler","stream":"ext://sys.stdout"}},"loggers":{"":{"level":0,"handlers":["default"]},"rcgcdw":{},"rcgcdw.misc":{}}},"appearance":{"mode":"embed","embed":{"show_edit_changes":false,"show_footer":true,"embed_images":true,"daily_overview":{"color":16312092,"icon":""},"new":{"icon":"https://i.imgur.com/6HIbEq8.png","color":"THIS COLOR DEPENDS ON EDIT SIZE, PLEASE DON'T CHANGE"},"edit":{"icon":"","color":"THIS COLOR DEPENDS ON EDIT SIZE, PLEASE DON'T CHANGE"},"upload/overwrite":{"icon":"https://i.imgur.com/egJpa81.png","color":12390624},"upload/upload":{"icon":"https://i.imgur.com/egJpa81.png","color":null},"upload/revert":{"icon":"https://i.imgur.com/egJpa81.png","color":null},"delete/delete":{"icon":"https://i.imgur.com/BU77GD3.png","color":1},"delete/delete_redir":{"icon":"https://i.imgur.com/BU77GD3.png","color":1},"delete/restore":{"icon":"https://i.imgur.com/9MnROIU.png","color":null},"delete/revision":{"icon":"https://i.imgur.com/1gps6EZ.png","color":null},"delete/event":{"icon":"https://i.imgur.com/1gps6EZ.png","color":null},"merge/merge":{"icon":"https://i.imgur.com/uQMK9XK.png","color":null},"move/move":{"icon":"https://i.imgur.com/eXz9dog.png","color":null},"move/move_redir":{"icon":"https://i.imgur.com/UtC3YX2.png","color":null},"block/block":{"icon":"https://i.imgur.com/g7KgZHf.png","color":1},"block/unblock":{"icon":"https://i.imgur.com/bvtBJ8o.png","color":1},"block/reblock":{"icon":"https://i.imgur.com/g7KgZHf.png","color":1},"protect/protect":{"icon":"https://i.imgur.com/bzPt89Z.png","color":null},"protect/modify":{"icon":"https://i.imgur.com/bzPt89Z.png","color":null},"protect/move_prot":{"icon":"https://i.imgur.com/bzPt89Z.png","color":null},"protect/unprotect":{"icon":"https://i.imgur.com/2wN3Qcq.png","color":null},"import/upload":{"icon":"","color":null},"import/interwiki":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"rights/rights":{"icon":"","color":null},"rights/autopromote":{"icon":"","color":null},"abusefilter/abusefilter":{"icon":"https://i.imgur.com/Sn2NzRJ.png","color":null},"abusefilter/modify":{"icon":"https://i.imgur.com/Sn2NzRJ.png","color":null},"abusefilter/create":{"icon":"https://i.imgur.com/Sn2NzRJ.png","color":null},"interwiki/iw_add":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"interwiki/iw_edit":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"interwiki/iw_delete":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"curseprofile/comment-created":{"icon":"https://i.imgur.com/Lvy5E32.png","color":null},"curseprofile/comment-edited":{"icon":"https://i.imgur.com/Lvy5E32.png","color":null},"curseprofile/comment-deleted":{"icon":"","color":null},"curseprofile/comment-purged":{"icon":"","color":null},"curseprofile/comment-replied":{"icon":"https://i.imgur.com/hkyYsI1.png","color":null},"curseprofile/profile-edited":{"icon":"","color":null},"contentmodel/change":{"icon":"","color":null},"cargo/deletetable":{"icon":"","color":null},"cargo/createtable":{"icon":"","color":null},"cargo/replacetable":{"icon":"","color":null},"cargo/recreatetable":{"icon":"","color":null},"sprite/sprite":{"icon":"","color":null},"sprite/sheet":{"icon":"","color":null},"sprite/slice":{"icon":"","color":null},"managetags/create":{"icon":"","color":null},"managetags/delete":{"icon":"","color":null},"managetags/activate":{"icon":"","color":null},"managetags/deactivate":{"icon":"","color":null},"tag/update":{"icon":"","color":null},"suppressed":{"icon":"https://i.imgur.com/1gps6EZ.png","color":8092539},"discussion/forum/post":{"icon":"","color":null},"discussion/forum/reply":{"icon":"","color":null},"discussion/forum/poll":{"icon":"","color":null},"discussion/forum/quiz":{"icon":"","color":null},"discussion/wall/post":{"icon":"","color":null},"discussion/wall/reply":{"icon":"","color":null},"discussion/comment/post":{"icon":"","color":null},"discussion/comment/reply":{"icon":"","color":null}}},"fandom_discussions":{"enabled":false,"wiki_id":1885853,"wiki_url":"https://wikibot.fandom.com/","cooldown":60,"webhookURL":"https://discordapp.com/api/webhooks/111111111111111111/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","limit":5,"appearance":{"mode":"embed","embed":{"show_content":true}},"show_forums":[]}}"""
result_file = """{"cooldown":60,"wiki_url":"https://wreckit-woodhouse.fandom.com/","rc_enabled":true,"lang":"en","header":{"user-agent":"RcGcDw/{version}"},"limit":10,"webhookURL":"https://discordapp.com/api/webhooks/111111111111111111/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","limitrefetch":28,"wikiname":"Wreck It Woodhouse","avatars":{"connection_failed":"https://i.imgur.com/2jWQEt1.png","connection_restored":"","no_event":"","embed":"","compact":""},"ignored":["external","newusers/create","newusers/autocreate","newusers/create2","newusers/byemail","newusers/newusers"],"show_updown_messages":true,"ignored_namespaces":[],"overview":false,"overview_time":"00:00","send_empty_overview":false,"license_detection":true,"license_regex_detect":"\\\\{\\\\{(license|lizenz|licence|copyright)","license_regex":"\\\\{\\\\{(license|lizenz|licence|copyright)(\\\\ |\\\\|)(?P<license>.*?)\\\\}\\\\}","disallow_regexes":[],"wiki_bot_login":"","wiki_bot_password":"","show_added_categories":true,"show_bots":false,"show_abuselog":false,"hide_ips":false,"discord_message_cooldown":0,"auto_suppression":{"enabled":false,"db_location":":memory:"},"logging":{"version":1,"disable_existing_loggers":false,"formatters":{"standard":{"format":"%(name)s - %(levelname)s: %(message)s"}},"handlers":{"default":{"formatter":"standard","class":"logging.StreamHandler","stream":"ext://sys.stdout"}},"loggers":{"":{"level":0,"handlers":["default"]},"rcgcdw":{},"rcgcdw.misc":{}}},"appearance":{"mode":"embed","embed":{"show_edit_changes":false,"show_footer":true,"embed_images":true,"daily_overview":{"color":16312092,"icon":""},"new":{"icon":"https://i.imgur.com/6HIbEq8.png","color":"THIS COLOR DEPENDS ON EDIT SIZE, PLEASE DON'T CHANGE"},"edit":{"icon":"","color":"THIS COLOR DEPENDS ON EDIT SIZE, PLEASE DON'T CHANGE"},"upload/overwrite":{"icon":"https://i.imgur.com/egJpa81.png","color":12390624},"upload/upload":{"icon":"https://i.imgur.com/egJpa81.png","color":null},"upload/revert":{"icon":"https://i.imgur.com/egJpa81.png","color":null},"delete/delete":{"icon":"https://i.imgur.com/BU77GD3.png","color":1},"delete/delete_redir":{"icon":"https://i.imgur.com/BU77GD3.png","color":1},"delete/restore":{"icon":"https://i.imgur.com/9MnROIU.png","color":null},"delete/revision":{"icon":"https://i.imgur.com/1gps6EZ.png","color":null},"delete/event":{"icon":"https://i.imgur.com/1gps6EZ.png","color":null},"merge/merge":{"icon":"https://i.imgur.com/uQMK9XK.png","color":null},"move/move":{"icon":"https://i.imgur.com/eXz9dog.png","color":null},"move/move_redir":{"icon":"https://i.imgur.com/UtC3YX2.png","color":null},"block/block":{"icon":"https://i.imgur.com/g7KgZHf.png","color":1},"block/unblock":{"icon":"https://i.imgur.com/bvtBJ8o.png","color":1},"block/reblock":{"icon":"https://i.imgur.com/g7KgZHf.png","color":1},"protect/protect":{"icon":"https://i.imgur.com/bzPt89Z.png","color":null},"protect/modify":{"icon":"https://i.imgur.com/bzPt89Z.png","color":null},"protect/move_prot":{"icon":"https://i.imgur.com/bzPt89Z.png","color":null},"protect/unprotect":{"icon":"https://i.imgur.com/2wN3Qcq.png","color":null},"import/upload":{"icon":"","color":null},"import/interwiki":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"rights/rights":{"icon":"","color":null},"rights/autopromote":{"icon":"","color":null},"abusefilter/abusefilter":{"icon":"https://i.imgur.com/Sn2NzRJ.png","color":null},"abusefilter/modify":{"icon":"https://i.imgur.com/Sn2NzRJ.png","color":null},"abusefilter/create":{"icon":"https://i.imgur.com/Sn2NzRJ.png","color":null},"interwiki/iw_add":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"interwiki/iw_edit":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"interwiki/iw_delete":{"icon":"https://i.imgur.com/sFkhghb.png","color":null},"curseprofile/comment-created":{"icon":"https://i.imgur.com/Lvy5E32.png","color":null},"curseprofile/comment-edited":{"icon":"https://i.imgur.com/Lvy5E32.png","color":null},"curseprofile/comment-deleted":{"icon":"","color":null},"curseprofile/comment-purged":{"icon":"","color":null},"curseprofile/comment-replied":{"icon":"https://i.imgur.com/hkyYsI1.png","color":null},"curseprofile/profile-edited":{"icon":"","color":null},"contentmodel/change":{"icon":"","color":null},"cargo/deletetable":{"icon":"","color":null},"cargo/createtable":{"icon":"","color":null},"cargo/replacetable":{"icon":"","color":null},"cargo/recreatetable":{"icon":"","color":null},"sprite/sprite":{"icon":"","color":null},"sprite/sheet":{"icon":"","color":null},"sprite/slice":{"icon":"","color":null},"managetags/create":{"icon":"","color":null},"managetags/delete":{"icon":"","color":null},"managetags/activate":{"icon":"","color":null},"managetags/deactivate":{"icon":"","color":null},"tag/update":{"icon":"","color":null},"suppressed":{"icon":"https://i.imgur.com/1gps6EZ.png","color":8092539},"discussion/forum/post":{"icon":"","color":null},"discussion/forum/reply":{"icon":"","color":null},"discussion/forum/poll":{"icon":"","color":null},"discussion/forum/quiz":{"icon":"","color":null},"discussion/wall/post":{"icon":"","color":null},"discussion/wall/reply":{"icon":"","color":null},"discussion/comment/post":{"icon":"","color":null},"discussion/comment/reply":{"icon":"","color":null}}},"fandom_discussions":{"enabled":false,"wiki_id":1885853,"wiki_url":"https://wikibot.fandom.com/","cooldown":60,"webhookURL":"https://discordapp.com/api/webhooks/111111111111111111/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","limit":5,"appearance":{"mode":"embed","embed":{"show_content":true}},"show_forums":[]}}"""


class TestMWFormatter(unittest.TestCase):
    def setUp(self) -> None:
        with open("settings.json", "r") as c_file:
            self.current_file = c_file.read()

    def tearDown(self) -> None:
        with open("settings.json", "w") as s_file:
            s_file.write(self.current_file)

    def test_11311_migration(self):
        with open("settings.json", "w") as s_file:
            s_file.write(test_file)
        importlib.import_module("src.migrations.11311")
        with open("settings.json", "r") as c_file:
            current_settings = c_file.read()
        self.assertEqual(json.loads(result_file), json.loads(current_settings))