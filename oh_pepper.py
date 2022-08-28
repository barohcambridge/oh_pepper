#!/usr/bin/env python

import os.path
import qi


class OhPepperService:

    NAME = 'oh_pepper'

    SERVICES = {
        'dialog': 'ALDialog',
        'packagemanager': 'PackageManager',
        'tts': 'ALTextToSpeech',
    }

    def __init__(self, session):
        self.session = session
        self.logger = qi.Logger(self.NAME)
        for name, service in self.SERVICES.items():
            setattr(self, name, session.service(service))
        self.load_topics()
        self.hello()

    @property
    def package(self):
        """Containing package"""
        return self.packagemanager.package('oh_pepper')

    def load_topics(self):
        """Load all dialog topics"""
        package = self.package
        path = package['path']
        for dialog in self.package['dialogs']:
            for lang, filename in dialog['topics'].items():
                topic = self.dialog.loadTopic(os.path.join(path, filename))
                self.logger.info("Registered %s (%s) from %s" %
                                 (topic, lang, filename))
                self.dialog.activateTopic(topic)

    def hello(self):
        self.tts.say("Hello world")


def main():
    app = qi.Application()
    app.start()
    session = app.session
    service = OhPepperService(session)
    session.registerService(service.NAME, service)
    app.run()


if __name__ == "__main__":
    main()
