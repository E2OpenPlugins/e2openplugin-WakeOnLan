import time
import os
from Plugins.Plugin import PluginDescriptor
import wol
import enigma

def configure(session, **kwargs):
	try:
		import ui
		session.openWithCallback(doneConfiguring, ui.Config)
	except Exception, ex:
		print "[WOL] Sorry, UI failed to start:", ex

def sendnow(session=None, **kwargs):
	try:
		wol.sendAllWOL()
	except Exception, ex:
		print "[WOL] failed to send out WOL packets:", ex

def doneConfiguring(session, retval):
	pass

def gotRecordEvent(self, service, event):
	if (event == enigma.iRecordableService.evStart):
		sendnow()

def autostart(reason, session=None, **kwargs):
	"called with reason=1 to during shutdown, with reason=0 at startup"
	if session and not reason:
		session.nav.record_event.append(gotRecordEvent)

description = _("Send WOL packet on PVR and recording start")

def Plugins(**kwargs):
	result = [
		PluginDescriptor(
			name="Wake-On-LAN",
			description = description,
			where = [PluginDescriptor.WHERE_SESSIONSTART],
			fnc = autostart
		),
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
