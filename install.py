#!/usr/bin/python

import os,shutil

if os.path.isfile('devcon.exe') == True and os.path.isfile('C:/WINDOWS/system32/devcon.exe') == False:
	shutil.copyfile('devcon.exe', 'C:/WINDOWS/system32/')
