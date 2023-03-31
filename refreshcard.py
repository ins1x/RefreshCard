#!/usr/bin/python -W
#-*- encoding: utf-8 -*-
# Script emulating reconnect PCMCIA SCSI Laptop Add-On Card wireless card
__version__ = "2.1.1 build 02.04.2011"

import os,sys
import ConfigParser 

config = ConfigParser.RawConfigParser() #Define global configfile variable
CurDir = os.getcwd()# get current directory
SettingsFileName = 'settings.cfg'
ConfigFileDest = CurDir + '/' + SettingsFileName #Settings file destination

def os_checker():
	"""Check operation system"""
	if os.name == 'nt':
		#check configfile
		if os.path.isfile(ConfigFileDest) == False:
			configwindows_proc()
		elif os.path.isfile(ConfigFileDest) == True:
			DEVMASK = config.get('windows','DEVMASK')
			DEVCON_PATH = config.get('windows','DEVCON_PATH')
			refresh_card_win(DEVMASK,DEVCON_PATH)
	elif os.name == 'posix':
		#check configfile
		if os.path.isfile(ConfigFileDest) == False:
			configlinux_proc()
		elif os.path.isfile(ConfigFileDest) == True:
			MODULEPATH = config.get('linux','MODULEPATH')
			MODULENAME = config.get('linux','MODULENAME')
			refresh_card_nix(MODULEPATH,MODULENAME)
	else:
		#Not-supported OS if os.name != 'nt' or  'posix'
		print >> sys.stderr, "Sorry your operating system not supported"
		sys.exit(1)

def configwindows_proc():
	config.add_section('windows')
	print 'Start config windows proc'
	#BUG here!!!
	config.set('windows','DEVMASK','*SUBSYS_3A151186*')
	config.set('windows','DEVCON_PATH','C:\WINDOWS\system32\devcon.exe')
	config_write_sub()
	refresh_card_win('*SUBSYS_3A151186*','C:\WINDOWS\system32\devcon.exe')
	
def refresh_card_win(DEVMASK,DEVCON_PATH):
	import subprocess
	#Support Windows XP
	#if devcon.exe exist do
	if os.path.isfile(DEVCON_PATH):
		#Disable device[PATH_TO_PROGRAM, 'action','MASK']
		if 0 == subprocess.call([DEVCON_PATH, 'disable', DEVMASK], shell=True):
			print '---------------------------------------------------------'
		if 0 == subprocess.call([DEVCON_PATH, 'enable', DEVMASK], shell=True):
			print '---------------------------------------------------------'
		else:
			print >> sys.stderr, "Cant do operation.You card not supported!Change DEVMASK"
			sys.exit(1)
	else:
		print ('devcon.exe not found.Please install him to C:\windows\system32')

def configlinux_proc():
	"""Prepairing and create configfile"""
	#Support Debian,Ubuntu,Mint
	KERNELDIR = '/lib/modules/'#Default modules directory
	KERNELLIST = os.listdir(KERNELDIR)#List of installed kernel headers
	config.add_section('linux')
	print 'Choose your kernel:Enter number item'
	for i in range(len(KERNELLIST)):
		print (i,KERNELLIST[i])
	Knum = input()
	#BUG here!!!
	CARD_MODULES_DIR = KERNELDIR + KERNELLIST[Knum] + '/kernel/drivers/net/wireless/'#Wireless drivers folder
	print 'Choose your driver.Notice - open shell and write "lsmod" to find module'
	DRIVERLIST = os.listdir(CARD_MODULES_DIR)
	for i in range(len(DRIVERLIST)):
		print (i,DRIVERLIST[i])
	Dnum = input()
	DRIVERPATH = CARD_MODULES_DIR + DRIVERLIST[Dnum]
	if os.path.isfile(DRIVERPATH) == True:
		config.set('linux','MODULEPATH',DRIVERPATH)
		config.set('linux','MODULENAME',DRIVERLIST[Dnum])
		config_write_sub()
		refresh_card_nix(DRIVERPATH,DRIVERLIST[Dnum])#refresh_card_nix(modulepath,modulename)
	elif os.path.isdir(DRIVERPATH) == True:
		print 'Choose your driver here.Notice - open shell and write "lsmod" to find module'	
		DRIVERPATHsub = os.listdir(DRIVERPATH)
		for i in range(len(DRIVERPATHsub)):
			print (i,DRIVERPATHsub[i])
		Dsnum = input()
		DRIVERPATHFULL = DRIVERPATH + DRIVERPATHsub[Dsnum]
		if os.path.isfile(DRIVERPATHFULL) == True:
			config.set('linux','MODULEPATH',DRIVERPATHFULL)
			config.set('linux','MODULENAME',DRIVERPATHsub[Dsnum])
			config_write_sub()
			refresh_card_nix(DRIVERPATHFULL,DRIVERPATHsub[Dsnum])
		else:
			print >> sys.stderr, "Error Many subdirectories"
			sys.exit(1)
	else:
		print >> sys.stderr, "Error in choose module"
		sys.exit(1)
		
def refresh_card_nix(MODULEPATH,MODULENAME):
	"""Refresh card main procedure:
		Using refresh_card_nix(MODULEPATH,MODULENAME)
		MODULEPATH  - path to your wireless driver module .ko
		MODULENAME - name your wireless driver module"""
	print(MODULEPATH,MODULENAME)
	#Disable module
	#os.system('sudo rmmod ' + MODULENAME)#Disable module
	#Enable module
	#os.system('sudo insmod ' + MODULEPATH)#Enable module

def config_write_sub():
	"""Macros save configuration file"""
	with open(SettingsFileName, 'wb') as configfile:
		config.write(configfile)

def walkdir_sub(directory):
	"""Subdirectoies search macros"""
	for root, dirs, files in os.walk(directory):
		for name in files:
			print(os.path.join(root, name))
		for name in dirs:
			print(os.path.join(root, name))

if __name__ == "__main__":
	os_checker()
