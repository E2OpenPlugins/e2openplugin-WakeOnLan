import time
import os
from Plugins.Plugin import PluginDescriptor
import wol
import enigma

def configure(session, iface=None, **kwargs):
	try:
		import ui
		session.openWithCallback(doneConfiguring, ui.Config)
	except Exception, ex:
		print "[WOL] Sorry, UI failed to start:", ex

def sendnow(session=None, iface=None, **kwargs):
	try:
		wol.sendAllWOL()
	except Exception, ex:
		print "[WOL] failed to send out WOL packets:", ex

def doneConfiguring(session, retval):
	pass

def gotRecordEvent(service, event):
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
			name=_("Configure Wake-On-LAN"),
			description = description,
			where = PluginDescriptor.WHERE_NETWORKSETUP,
			fnc={"ifaceSupported": lambda x: configure,
				"menuEntryName": lambda x: _("Send Wake-on-LAN"),
				"menuEntryDescription": lambda x: description}
		),
		PluginDescriptor(
			name=_("Send Wake-On-LAN"),
			description = description,
			where = PluginDescriptor.WHERE_NETWORKSETUP,
			fnc={"ifaceSupported": lambda x: sendnow,
				"menuEntryName": lambda x: _("Send Wake-on-LAN"),
				"menuEntryDescription": lambda x: description}
		),
	]
	return result
