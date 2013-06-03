# -*- coding: utf-8 -*-
# Copyright (c) 2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import urllib

from zope import interface, schema, component
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser import absoluteURL

from Products.Silva.mail import sendmail

from silva.captcha import Captcha
from silva.core.interfaces import ISilvaObject
from silva.core.layout import interfaces
from silva.core.views.interfaces import INonCachedLayer
from silva.pageactions.base.base import PageAction
from zeam.form import silva as silvaforms

from five import grok

_ = MessageFactory("pageactions")


def MIMEPdf(pdf_data, filename=None):
    mime = MIMEBase('application', 'pdf')
    mime.set_payload(pdf_data)
    if filename is not None:
        mime.add_header('Content-Disposition', 'attachement', filename=filename)
    encode_base64(mime)
    return mime


class IMailForm(interface.Interface):
    to = schema.TextLine(title=_(u"To"), required=True)
    subject = schema.TextLine(title=_(u"Subject"), required=True)
    captcha = Captcha(title=_(u"Captcha"), required=True)


class MailThatPage(silvaforms.PublicForm):
    grok.name('mailthatpage.html')
    grok.context(ISilvaObject)
    fields = silvaforms.Fields(IMailForm)

    label = _(u"Send this page by mail")

    def __call__(self):
        interface.alsoProvides(self.request, INonCachedLayer)
        return super(MailThatPage, self).__call__()

    @silvaforms.action(_(u"Send"))
    def send(self):
        data, errors = self.extractData()
        if errors:
            self.status = _(u"Please correct the errors.")
            return silvaforms.FAILURE

        metadata = interfaces.IMetadata(self.context.get_root())
        mail_template = metadata('mail-pageactions', 'mail-body')
        mail_from = metadata('mail-pageactions', 'mail-from')

        if (not mail_from) or (not mail_template):
            self.status = _(u"Mail settings are not configured, "
                            "can't send mail at the moment.")
            return silvaforms.FAILURE

        url = absoluteURL(self.context, self.request)
        body = mail_template % {'title': self.context.get_title(), 'url': url}
        pdf = component.getMultiAdapter(
            (self.context, self.request),
            name="index.pdf").pdf()

        message = MIMEMultipart()
        message['Subject'] = data['subject']
        message['To'] = data['to']
        message['Form'] = mail_from

        message.attach(MIMEText(body, 'plain', 'UTF-8'))
        message.attach(MIMEPdf(pdf, self.context.getId()))

        try:
            sendmail(self.context,
                     message.as_string(),
                     data['to'],
                     mail_from,
                     data['subject'])
        except SMTPException, e:
            self.status = str(e)
        else:
            exit_url = url + '?' + urllib.urlencode(
                [('message_status',
                  translate(_(u"Your message has been sent."),
                            context=self.request))])
            self.redirect(exit_url)
        return silvaforms.SUCCESS


class MailPDFAction(PageAction):
    grok.order(40)
