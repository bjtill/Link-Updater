# Link-Updater
A tool to recursively update URL addresses in multiple files in multiple directories.  
______________________________________________________________________________________

Use at your own risk. I cannot provide support. All information obtained/inferred with this script is without any implied warranty of fitness for any purpose or use whatsoever.

ABOUT: 

This program provides a quick way to update URL addresses in multiple files in multiple directories.  For example, change http://10.100.100.111/anytext  to http://10.111.222.333/anytext.  The program allows specification of specific file extension(s), creates backups of files prior to modification, and allows a dry-run to see what will be modified before any changes are made.

RATIONAL:

This was created to update a local website that contains many .html pages containing links to various local .html pages. While the IP address was stable for years, it was not static and upgrades resulted in a change of local IP address. This tool was built to automate the updating of all links in all .html files rather than manually update all the addresses. 

PREREQUISITES:
1. Python3
   
COMMAND LINE OPTIONS:  

<b>Default behavior</b> (modify all .html and .htm files in all sub-directories, create backup .bak of all files modified)  

python3 link_updater_V2.ph /path/to/html/directory 10.100.111.222 100.200.300.400

<b>Perform a dry run to see what files would be changed without changing any files</b>

python3 link_updater_V2.ph /path/to/html/directory 10.100.111.222 100.200.300.400 --dry-run

<b>Run the program without creating backup files</b> 

python3 link_updater_V2.ph /path/to/html/directory 10.100.111.222 100.200.300.400 --no-backup

________________________________________________________________________________________________________________________________

<i>OPTIONS FOR MODIFYING LINKS IN FILES WITH DIFFERENT EXTENSIONS</i>

<b>Process only .txt files</b>

python3 link_updater_V2.ph /path/to/files 10.100.111.222 100.200.300.400 --extensions .txt

<b>Process multiple file types</b>

python3 link_updater_V2.ph /path/to/files 10.100.111.222 100.200.300.400 --extensions .html .htm .php .js .css

<b>Process .txt and .md files</b>

python3 link_updater_V2.ph /path/to/files 192.168.1.1 192.168.1.100 --extensions .txt .md

<b>You can specify extensions with or without the dot</b>

python3 link_updater_V2.ph /path/to/files 10.0.0.1 10.0.0.50 --extensions txt html php
 
<b>Example for configuration files</b>

python3 link_updater_V2.ph /path/to/config 192.168.1.100 192.168.1.200 --extensions .conf .cfg .ini

<b>Example for development files</b>

python3 link_updater_V2.ph /var/www 10.0.0.1 10.0.0.50 --extensions .html .htm .php .js .css
