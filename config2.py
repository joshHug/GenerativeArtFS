import os
import re
from datetime import datetime
from templar.api.config import ConfigBuilder
from templar.api.rules.compiler_rules import MarkdownToHtmlRule
from templar.api.rules.table_of_contents import HtmlTableOfContents
from templar.api.rules.core import SubstitutionRule

# Path of the current file -- best not to change this
FILEPATH = os.path.dirname(os.path.abspath(__file__))

# Path to public_html base dir
PH_PATH = "../../../"

if os.path.isfile("PH_PATH"):
    f = open("PH_PATH", 'r')
    for line in f:
        PH_PATH = line.rstrip()

PH_ASSETS_PATH = os.path.join(PH_PATH, "assets")

##################
# Configurations #
##################

class HomePageLinkRule(SubstitutionRule):
    pattern = r'<home-page-link>'
    def substitute(self, match):
        return PH_PATH

config = ConfigBuilder().add_template_dirs(
    os.path.join(FILEPATH, "templates"),
).add_variables({
    'datetime': '{dt:%A}, {dt:%B} {dt.day}, {dt:%Y} at {dt:%l}:{dt:%M} {dt:%p}'.format(dt=datetime.now()),
    'class': 'CS 195',
}).append_compiler_rules(
    MarkdownToHtmlRule(),
).append_postprocess_rules(
    HomePageLinkRule(src='md$', dst='html$'),
    HtmlTableOfContents(),
).build()
