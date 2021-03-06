# -*- coding: utf-8 -*-

from intelmq.lib.bot import ParserBot

CLASSIFICATION = {
    "c2server": "c2-server",
    "scanning host": "scanner",
    "malicious host": "infected-system",
    "spamming": "spam",
    "malware domain": "malware-distribution",
    "malware ip": "malware-distribution",
    "malware distribution": "malware-distribution",
}


class AlienVaultParserBot(ParserBot):
    """Parse data from the AlienVault API"""

    def parse_line(self, row, report):
        values = row.split("#")

        # Send one event per classification
        classification_types = []
        if values[3].strip().find(";") > 0:
            classification_types.extend(values[3].split(";"))
        else:
            classification_types.append(values[3])

        for ctype in classification_types:

            event = self.new_event(report)

            if ctype.lower() in CLASSIFICATION:
                event.add('classification.type',
                          CLASSIFICATION[ctype.lower()])
            else:
                event.add('classification.type', "undetermined")

            if len(values[6].strip()) > 0:
                geo_coordinates = values[6].strip().split(",")
                if len(geo_coordinates) == 2:
                    geo_latitude = geo_coordinates[0]
                    geo_longitude = geo_coordinates[1]

            event.add('source.ip', values[0].strip())
            event.add('source.geolocation.cc',
                      values[4].strip())
            event.add('source.geolocation.city',
                      values[5].strip())
            event.add('source.geolocation.latitude',
                      geo_latitude.strip())
            event.add('source.geolocation.longitude',
                      geo_longitude.strip())

            event.add("raw", row)

            yield event


BOT = AlienVaultParserBot
