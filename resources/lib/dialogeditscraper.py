import xbmc, xbmcgui

import os

import util, config, dialogbase
from util import *
from configxmlwriter import *

ACTION_EXIT_SCRIPT = (10,)
ACTION_CANCEL_DIALOG = ACTION_EXIT_SCRIPT + (9,)

CONTROL_BUTTON_EXIT = 5101
CONTROL_BUTTON_SAVE = 6000
CONTROL_BUTTON_CANCEL = 6010


#Scrapers
CONTROL_LIST_SCRAPERS = 5600
CONTROL_BUTTON_SCRAPERS_DOWN = 5601
CONTROL_BUTTON_SCRAPERS_UP = 5602
CONTROL_BUTTON_GAMEDESCPATH = 5520
CONTROL_BUTTON_GAMEDESCMASK = 5530
CONTROL_BUTTON_PARSEINSTRUCTION = 5540
CONTROL_BUTTON_DESCPERGAME = 5550
CONTROL_BUTTON_SEARCHBYCRC = 5560
CONTROL_BUTTON_USEFOLDERASCRC = 5580
CONTROL_BUTTON_USEFILEASCRC = 5590
CONTROL_BUTTON_REMOVESCRAPER = 5610
CONTROL_BUTTON_ADDSCRAPER = 5620


class EditOfflineScraper(dialogbase.DialogBaseEdit):
	
	selectedControlId = 0
	
	selectedOfflineScraper = None
	scraperSites = None
	
	
	def __init__(self, *args, **kwargs):
		Logutil.log('init Edit Offline Scraper', util.LOG_LEVEL_INFO)
		
		self.gui = kwargs[ "gui" ]
		self.scraperSites = self.gui.config.scraperSites
		self.doModal()
		
		
	def onInit(self):
		Logutil.log('onInit Edit Offline Scraper', util.LOG_LEVEL_INFO)
				
		Logutil.log('build scrapers list', util.LOG_LEVEL_INFO)
		scrapers = self.getAvailableScrapers(True)
		self.addItemsToList(CONTROL_LIST_SCRAPERS, scrapers)
		
		self.updateOfflineScraperControls()
		
	
	def onAction(self, action):		
		if (action.getId() in ACTION_CANCEL_DIALOG):
			self.close()
			
			
	def onClick(self, controlID):
		
		Logutil.log('onClick', util.LOG_LEVEL_INFO)
		
		if (controlID == CONTROL_BUTTON_EXIT): # Close window button
			Logutil.log('close', util.LOG_LEVEL_INFO)
			self.close()
		#OK
		elif (controlID == CONTROL_BUTTON_SAVE):
			Logutil.log('save', util.LOG_LEVEL_INFO)			
				
			#store selectedOfflineScraper
			if(self.selectedOfflineScraper != None):
				self.updateSelectedOfflineScraper()				
				self.scraperSites[self.selectedOfflineScraper.name] = self.selectedOfflineScraper
						
			configWriter = ConfigXmlWriter(False)
			success, message = configWriter.writeScrapers(self.scraperSites)
			
			self.close()
		#Cancel
		elif (controlID == CONTROL_BUTTON_CANCEL):
			self.close()
			
		#Offline Scraper
		elif(self.selectedControlId in (CONTROL_BUTTON_SCRAPERS_UP, CONTROL_BUTTON_SCRAPERS_DOWN)):
			
			if(self.selectedOfflineScraper != None):
				#save current values to selected ScraperSite
				self.updateSelectedOfflineScraper()
				
				#store previous selectedOfflineScrapers state
				self.scraperSites[self.selectedOfflineScraper.name] = self.selectedOfflineScraper
			
			#HACK: add a little wait time as XBMC needs some ms to execute the MoveUp/MoveDown actions from the skin
			xbmc.sleep(util.WAITTIME_UPDATECONTROLS)
			self.updateOfflineScraperControls()
			
		elif (controlID == CONTROL_BUTTON_GAMEDESCPATH):
			
			gamedescPathComplete = self.editPathWithFileMask(CONTROL_BUTTON_GAMEDESCPATH, '%s game desc path' %self.selectedOfflineScraper.name, CONTROL_BUTTON_GAMEDESCMASK)
			if(gamedescPathComplete != ''):
				
				#HACK: only use source and parser from 1st scraper
				if(len(self.selectedOfflineScraper.scrapers) >= 1):			
					self.selectedOfflineScraper.scrapers[0].source = gamedescPathComplete
		
		elif (controlID == CONTROL_BUTTON_GAMEDESCMASK):
			
			if(len(self.selectedOfflineScraper.scrapers) >= 1):
				self.selectedOfflineScraper.scrapers[0].source = self.editFilemask(CONTROL_BUTTON_GAMEDESCMASK, 'game desc filemask', self.selectedOfflineScraper.scrapers[0].source)
			
		elif (controlID == CONTROL_BUTTON_PARSEINSTRUCTION):
			
			dialog = xbmcgui.Dialog()
			
			parseInstruction = dialog.browse(1, '%s parse instruction' %self.selectedOfflineScraper.name, 'files')
			if(parseInstruction == ''):
				return
			
			control = self.getControlById(CONTROL_BUTTON_PARSEINSTRUCTION)
			control.setLabel(parseInstruction)		
			
			if(len(self.selectedOfflineScraper.scrapers) >= 1):
				self.selectedOfflineScraper.scrapers[0].parseInstruction = parseInstruction
				
		elif (controlID == CONTROL_BUTTON_ADDSCRAPER):
			
			name = ''
			
			keyboard = xbmc.Keyboard()
			keyboard.setHeading('Enter scraper name')
			keyboard.doModal()
			if (keyboard.isConfirmed()):
				name = keyboard.getText()
			
			if(name == ''):
				return
			
			site = Site()
			site.name = name
			site.scrapers = []
			self.scraperSites[name] = site
			
			control = self.getControlById(CONTROL_LIST_SCRAPERS)
			item = xbmcgui.ListItem(name, '', '', '')
			control.addItem(item)
			
			self.selectItemInList(name, CONTROL_LIST_SCRAPERS)
			
			if(self.selectedOfflineScraper != None):
				#save current values to selected ScraperSite
				self.updateSelectedOfflineScraper()
				
				#store previous selectedOfflineScrapers state
				self.scraperSites[self.selectedOfflineScraper.name] = self.selectedOfflineScraper
			
			#HACK: add a little wait time as XBMC needs some ms to execute the MoveUp/MoveDown actions from the skin
			xbmc.sleep(util.WAITTIME_UPDATECONTROLS)
			self.updateOfflineScraperControls()
			
		elif (controlID == CONTROL_BUTTON_REMOVESCRAPER):
			
			scraperSites = self.getAvailableScrapers(True)
			
			scraperIndex = xbmcgui.Dialog().select('Choose a scraper to remove', scraperSites)
			if(scraperIndex == -1):
				return
			
			scraperSite = scraperSites[scraperIndex]
																	
			scraperSites.remove(scraperSite)
			del self.scraperSites[scraperSite]
			
			if(len(scraperSites) == 0):
				scraperSites.append('None')
				site = Site()
				site.name = 'None'
				site.scrapers = []
				self.scraperSites['None'] = site
				
			control = self.getControlById(CONTROL_LIST_SCRAPERS)
			control.reset()
			self.addItemsToList(CONTROL_LIST_SCRAPERS, scraperSites)
				
			self.updateOfflineScraperControls()
			
	
	def onFocus(self, controlId):
		self.selectedControlId = controlId
	
	
	def updateOfflineScraperControls(self):
		
		Logutil.log('updateOfflineScraperControls', util.LOG_LEVEL_INFO)
		
		control = self.getControlById(CONTROL_LIST_SCRAPERS)
		selectedScraperName = str(control.getSelectedItem().getLabel())
		
		selectedSite = None
		try:
			selectedSite = self.scraperSites[selectedScraperName]
		except:
			#should not happen
			return
		
		self.selectedOfflineScraper = selectedSite
		
		#HACK: only use source and parser from 1st scraper
		firstScraper = None
		if(len(selectedSite.scrapers) >= 1):			
			firstScraper = selectedSite.scrapers[0]
		if(firstScraper == None):
			firstScraper = Scraper()
		
		pathParts = os.path.split(firstScraper.source)
		scraperSource = pathParts[0]
		scraperFileMask = pathParts[1]
		
		control = self.getControlById(CONTROL_BUTTON_GAMEDESCPATH)
		control.setLabel(scraperSource)
		
		control = self.getControlById(CONTROL_BUTTON_GAMEDESCMASK)
		control.setLabel(scraperFileMask)
		
		control = self.getControlById(CONTROL_BUTTON_PARSEINSTRUCTION)
		control.setLabel(firstScraper.parseInstruction)
		
		control = self.getControlById(CONTROL_BUTTON_DESCPERGAME)
		control.setSelected(selectedSite.descFilePerGame)
		
		control = self.getControlById(CONTROL_BUTTON_SEARCHBYCRC)
		control.setSelected(selectedSite.searchGameByCRC)
		
		control = self.getControlById(CONTROL_BUTTON_USEFILEASCRC)
		control.setSelected(selectedSite.useFilenameAsCRC)
		
		control = self.getControlById(CONTROL_BUTTON_USEFOLDERASCRC)
		control.setSelected(selectedSite.useFoldernameAsCRC)
		
	
	def updateSelectedOfflineScraper(self):
		Logutil.log('updateSelectedOfflineScraper', util.LOG_LEVEL_INFO)
		
		#desc file per game
		control = self.getControlById(CONTROL_BUTTON_DESCPERGAME)
		self.selectedOfflineScraper.descFilePerGame = bool(control.isSelected())
		
		#search game by crc
		control = self.getControlById(CONTROL_BUTTON_SEARCHBYCRC)
		self.selectedOfflineScraper.searchGameByCRC = bool(control.isSelected())
		
		#use foldername as crc
		control = self.getControlById(CONTROL_BUTTON_USEFOLDERASCRC)
		self.selectedOfflineScraper.useFoldernameAsCRC = bool(control.isSelected())
		
		#use filename as crc
		control = self.getControlById(CONTROL_BUTTON_USEFILEASCRC)
		self.selectedOfflineScraper.useFilenameAsCRC = bool(control.isSelected())
		
		