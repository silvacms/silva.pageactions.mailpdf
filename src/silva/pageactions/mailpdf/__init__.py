# -*- coding: utf-8 -*-
# Copyright (c) 2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface
from silva.core.conf.installer import DefaultInstaller
from silva.core import conf as silvaconf

silvaconf.extension_name('silva.pageactions.mailpdf')
silvaconf.extension_title('Send that page by mail')

class IExtension(Interface):
    """Extension to send mail.
    """

METADATA = {('Silva Root', 'Silva Publication',): ('mail-pageactions',)}


class MailInstaller(DefaultInstaller):
    __name__ = 'silva.pageactions.mailpdf.install'

    def install_custom(self, root):
        self.configureMetadata(root, METADATA, globals())

    def uninstall_custom(self, root):
        self.unconfigureMetadata(root, METADATA)


install = MailInstaller('silva.pageactions.mailpdf', IExtension)

