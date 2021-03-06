#!/usr/bin/env python
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from daemons.worker import RedisWorker

import config.config as c

import models.rethink.email.emailModel as em
import models.rethink.user.userModel as um

from envelopes import Envelope

import arrow
import logging

logger = logging.getLogger(c.emailer.log_name)


class Emailer(RedisWorker):
    name = "emailer"
    def build(self):
        email = em.Email(self.data)

        if email:
            logger.info("Sending email {}".format(email.id))

            to = [ um.User(a).email if "@" not in a else a for a in email.to_addresses ]
            bcc = [ um.User(a).email if "@" not in a else a for a in email.bcc_addresses ]
            cc = [ um.User(a).email if "@" not in a else a for a in email.cc_addresses ]

            envelope = Envelope(
                from_addr="{}@transientbug.com".format(email.service),
                to_addr=to,
                bcc_addr=bcc,
                cc_addr=cc,
                subject=email.subject,
                text_body=email.content["text"],
                html_body=email.content["html"]
            )

            if c.send_email:
                envelope.send('localhost', port=25)

            if c.debug:
                logger.info(email)

            email.sent = arrow.utcnow().timestamp
            email.save()
            logger.info("Sent email {}".format(email.id))
