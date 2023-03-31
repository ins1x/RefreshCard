# RefreshCard.py

Reconnect PCMCIA SCSI Laptop Add-On Card  
  
More information on device search: https://learn.microsoft.com/ru-ru/windows-hardware/drivers/devtest/devcon-find

### Config

Windows:
Before using please change DEVMASK variable  
In order obtain PID or VID your device  
``` Start -> Run -> cmd -> devcon.exe hwids *  ```
And find your device by name.  

Linux:
Before using please change MOD_PATH and MODNAME  
Use lsmod to find your module  

### Requiremets
- Python 3.x  
- To work on windows, use the utility [DevCon.exe](https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/devcon) by Microsoft  