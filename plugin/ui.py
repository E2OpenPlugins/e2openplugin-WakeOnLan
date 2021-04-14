import enigma
import wol
from Components.config import config, configfile, getConfigListEntry, ConfigSelection
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox

def getCurrentList():
	try:
		macs = wol.getWOLList()
		arps = wol.getArpList()
		result = []
		for mac in macs:
			ip = "?"
			for arp in arps:
				if arp[1] == mac:
					ip = arp[0]
					break
			result.append(("%s\t%s" % (mac, ip), mac))
		return result
	except Exception, ex:
		print "[WOL] Failed to load config:", ex
		return []

class Config(Screen):
	skin = """
<screen position="center,center" size="560,400" title="Wake-On-LAN Configuration" >
	<ePixmap name="red"    position="0,0"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
	<ePixmap name="green"  position="140,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
	<ePixmap name="yellow" position="280,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" /> 
	<ePixmap name="blue"   position="420,0" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" /> 

	<widget name="key_red" position="0,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
	<widget name="key_green" position="140,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" /> 
	<widget name="key_yellow" position="280,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />
	<widget name="key_blue" position="420,0" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;20" transparent="1" shadowColor="background" shadowOffset="-2,-2" />

	<widget name="config" position="10,40" size="540,200" scrollbarMode="showOnDemand" />
	<widget name="status" position="10,250" size="540,130" font="Regular;16" />

	<ePixmap alphatest="on" pixmap="skin_default/icons/clock.png" position="480,383" size="14,14" zPosition="3"/>
	<widget font="Regular;18" halign="left" position="505,380" render="Label" size="55,20" source="global.CurrentTime" transparent="1" valign="center" zPosition="3">
		<convert type="ClockToText">Default</convert>
	</widget>
</screen>"""
		
	def __init__(self, session, args=0):
		self.session = session
		self.skinName = "Config_WakeOnLan"
		self.setup_title = _("Wake-On-LAN Configuration")
		Screen.__init__(self, session)
		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Ok"))
		self["key_yellow"] = Button(_("Remove"))
		self["key_blue"] = Button(_("Add"))
		self["status"] = Label(_("The list of MAC addresses above will be sent a WOL event."))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"green": self.save,
			"yellow": self.doremove,
			"blue": self.doadd,
			"save": self.save,
			"cancel": self.cancel,
			"ok": self.save,
		}, -2)
		self.menuitems = getCurrentList()
		self["config"] = MenuList(self.menuitems)

	def doadd(self):
		items = [("%s\t%s" % (x[1],x[0]), x[1]) for x in wol.getArpList()]
		self.session.openWithCallback(self.doaddDone, ChoiceBox, list=items)
	def doaddDone(self, result):
	        if not result or not result[1]:
	                return
	        mac = result[1]
	        for i in self.menuitems:
			if i[1] == mac:
				return
		self.menuitems.append(result)
		self["config"].setList(self.menuitems)

	def doremove(self):
		pass

	def save(self):
		try:
			f = open(wol.WOLLIST, 'w')
			for item in self.menuitems:
				f.write('%s\n' % item[1])
			f.close()
			self.close(True,self.session)
		except Exception, ex:
			print "[WOL] Failed to save config:", ex
			self.session.open(MessageBox, _("Failed to save configuration") + ":\n" + str(ex), type=MessageBox.TYPE_ERROR)

	def cancel(self):
		self.close(False,self.session)
