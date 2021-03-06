# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot


class BlackholeOutputBot(Bot):
    "Discard messages"

    def process(self):
        self.receive_message()
        self.acknowledge_message()


BOT = BlackholeOutputBot
