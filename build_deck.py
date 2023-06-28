import genanki
import json

import csv
import sys
import os
import re
from glob import glob

CONFIG_DECK_NAME = "deck_name"
CONFIG_VERSION = "version"
CONFIG_SOURCE_FILE = "source"
CONFIG_HEADERS = "headers"
CONFIG_FIELDS = "fields"
CONFIG_TEMPLATES = "templates"
CONFIG_STYLE = "style"

working_dir = sys.argv[1]
output_dir = os.path.join(os.getcwd(), sys.argv[2])

os.chdir(working_dir)

config_regex = r".*\.config\.json"
config_filenames = [file for file in os.listdir() if re.match(config_regex, file)]

for config_filename in config_filenames:
    with open(config_filename, "r") as config_json:
        config = json.load(config_json)

        deck_name = config[CONFIG_DECK_NAME]

        print(f'Building deck "{deck_name}"...')

        templates = []
        for template_config in config[CONFIG_TEMPLATES]:
            with open(template_config["front"]) as frontfile, open(
                template_config["back"]
            ) as backfile:
                templates.append(
                    {
                        "name": f"{template_config['name']}",
                        "qfmt": frontfile.read(),
                        "afmt": backfile.read(),
                    }
                )

        style = ""
        with open(config[CONFIG_STYLE], "r") as stylefile:
            style = stylefile.read()

        model = genanki.Model(
            1607392319,
            deck_name,
            fields=config[CONFIG_FIELDS],
            templates=templates,
            css=style,
        )

        deck = genanki.Deck(2059400110, deck_name)

        with open(config[CONFIG_SOURCE_FILE], "r") as sourcefile:
            reader = csv.reader(sourcefile)

            for row in reader:
                note = genanki.Note(
                    model=model,
                    fields=list(map(lambda i: row[i], config[CONFIG_HEADERS])),
                )
                deck.add_note(note)

        # TODO: Add media
        package = genanki.Package(deck)

        os.makedirs(output_dir, exist_ok=True)
        package.write_to_file(
            os.path.join(output_dir, f"{deck_name}.apkg")
        )

        print("Deck built!")
