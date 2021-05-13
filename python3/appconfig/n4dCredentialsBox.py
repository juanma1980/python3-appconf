#! /usr/bin/python3
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QUrl, QObject, Slot, Signal,Property
import os
import subprocess
import sys
import gettext
try:
	confText=gettext.translation("python3-appconfig")
	_ = confText.gettext
except:
	gettext.textdomain('python3-appconfig')
	_ = gettext.gettext


class Tunnel(QObject):
	onQmlTicket=Signal(str)

	@Slot(str)
	def on_ticket(self, ticket):
		ticket=ticket.replace(' ','##U+0020##').rstrip()
		self.onQmlTicket.emit(ticket)
		return True
	#def on_ticket

#class Tunnel

class n4dCredentials(QObject):
	onTicket=Signal(str)
	def __init__(self):
		super(n4dCredentials, self).__init__()
		if len(sys.argv)==2:
			server=sys.argv[1]

		self.tunnel = Tunnel()
		self.tunnel.onQmlTicket.connect(self._onTicket)

	def loginBox(self,server='localhost'):
			#self.view = QQuickView()
		self.qview = QQmlApplicationEngine()
		self.server=server
		self.qview.rootContext().setContextProperty("tunnel", self.tunnel)
		self.qview.setInitialProperties({"address": self.server})
		url = QUrl("/usr/share/appconfig/auth/login.qml")
		#self.view.setSource(url)
		self.qview.load(url)

	@Slot(str)
	def _onTicket(self,*args):
		print("A: {}".format(args))
		ticket=args[0]
		#self.view.close()
		self.onTicket.emit(ticket)
		return True

