import time
import os
from Plugins.Plugin import PluginDescriptor
import wol

def configure(session, **kwargs):
	try:
		import ui
		session.openWithCallback(doneConfiguring, ui.Config)
	except Exception, ex:
		print "[WOL] Sorry, UI failed to start:", ex

def sendnow(session, **kwargs):
	try:
		wol.sendAll()
	except Exception, ex:
		print "[WOL] failed to send out WOL packets:", ex

def doneConfiguring(session, retval):
	pass

description = _("Send WOL packet on PVR and recording start")

def Plugins(**kwargs):
	result = [
		PluginDescriptor(
			name="Wake-On-LAN",
			description = description,
			where = PluginDescriptor.WHERE_PLUGINMENU,
			fnc = configure
		),
		PluginDescriptor(
			name="Send Wake-On-LAN",
			description = description,
			where = PluginDescriptor.WHERE_EXTENSIONSMENU,
			fnc = sendnow)
	]
	return result
