#!/usr/bin/env python3
"""
LinkUpdater - Recursively updates IP addresses in text files

This script searches through a directory tree and replaces specified IP addresses
in files with specified extensions. It's designed to handle URL updates when local 
IP addresses change.

Usage:
    python LinkUpdater.py <directory> <old_ip> <new_ip> [options]
    
Examples:
    python LinkUpdater.py /path/to/files 10.100.100.114 172.25.220.114
    python LinkUpdater.py /path/to/files 192.168.1.1 192.168.1.100 --extensions .txt .md
    python LinkUpdater.py /path/to/files 10.0.0.1 10.0.0.50 --extensions .html .htm .php .js
"""

import os
import sys
import argparse
import re
from pathlib import Path
import logging

class LinkUpdater:
    def __init__(self, directory, old_ip, new_ip, extensions=None, backup=True, dry_run=False):
        self.directory = Path(directory)
        self.old_ip = old_ip
        self.new_ip = new_ip
        self.extensions = extensions or ['.html', '.htm']
        self.backup = backup
        self.dry_run = dry_run
        self.files_processed = 0
        self.files_modified = 0
        self.replacements_made = 0
        # Normalize extensions to ensure they start with a dot
        self.extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in self.extensions]
        self.extensions = [ext.lower() for ext in self.extensions]
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def validate_inputs(self):
        """Validate the input parameters"""
        if not self.directory.exists():
            raise ValueError(f"Directory does not exist: {self.directory}")
        
        if not self.directory.is_dir():
            raise ValueError(f"Path is not a directory: {self.directory}")
        
        # Basic IP address validation
        ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        if not re.match(ip_pattern, self.old_ip):
            raise ValueError(f"Invalid old IP address format: {self.old_ip}")
        
        if not re.match(ip_pattern, self.new_ip):
            raise ValueError(f"Invalid new IP address format: {self.new_ip}")
        
        if self.old_ip == self.new_ip:
            raise ValueError("Old and new IP addresses are the same")
    
    def find_target_files(self):
        """Recursively find all files with specified extensions in the directory"""
        target_files = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                file_ext = Path(file).suffix.lower()
                if file_ext in self.extensions:
                    target_files.append(Path(root) / file)
        return target_files
    
    def backup_file(self, file_path):
        """Create a backup of the file"""
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        try:
            backup_path.write_bytes(file_path.read_bytes())
            self.logger.debug(f"Created backup: {backup_path}")
        except Exception as e:
            self.logger.error(f"Failed to create backup for {file_path}: {e}")
            raise
    
    def process_file(self, file_path):
        """Process a single file"""
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Replace all occurrences of the old IP with the new IP
            content = content.replace(self.old_ip, self.new_ip)
            
            # Count replacements made in this file
            file_replacements = content.count(self.new_ip) - original_content.count(self.new_ip)
            
            if content != original_content:
                self.files_modified += 1
                self.replacements_made += file_replacements
                
                if self.dry_run:
                    self.logger.info(f"DRY RUN - Would modify {file_path} ({file_replacements} replacements)")
                else:
                    # Create backup if requested
                    if self.backup:
                        self.backup_file(file_path)
                    
                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.logger.info(f"Modified {file_path} ({file_replacements} replacements)")
            else:
                self.logger.debug(f"No changes needed for {file_path}")
            
            self.files_processed += 1
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
    
    def run(self):
        """Main execution method"""
        try:
            self.validate_inputs()
            
            self.logger.info(f"Starting LinkUpdater")
            self.logger.info(f"Directory: {self.directory}")
            self.logger.info(f"File extensions: {', '.join(self.extensions)}")
            self.logger.info(f"Replacing: {self.old_ip} -> {self.new_ip}")
            self.logger.info(f"Backup enabled: {self.backup}")
            self.logger.info(f"Dry run: {self.dry_run}")
            
            # Find all target files
            target_files = self.find_target_files()
            
            if not target_files:
                self.logger.warning(f"No files with extensions {', '.join(self.extensions)} found in the specified directory")
                return
            
            self.logger.info(f"Found {len(target_files)} files to process")
            
            # Process each file
            for file_path in target_files:
                self.process_file(file_path)
            
            # Print summary
            self.logger.info("=" * 50)
            self.logger.info("SUMMARY")
            self.logger.info("=" * 50)
            self.logger.info(f"Files processed: {self.files_processed}")
            self.logger.info(f"Files modified: {self.files_modified}")
            self.logger.info(f"Total replacements: {self.replacements_made}")
            
            if self.dry_run:
                self.logger.info("This was a dry run - no files were actually modified")
            elif self.backup and self.files_modified > 0:
                self.logger.info("Backup files created with .bak extension")
            
        except Exception as e:
            self.logger.error(f"Error: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Recursively update IP addresses in text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/files 10.100.100.114 172.25.220.114
  %(prog)s /path/to/files 192.168.1.100 192.168.1.200 --extensions .txt .md
  %(prog)s /path/to/files 10.0.0.1 10.0.0.50 --extensions .html .htm .php .js
  %(prog)s . 192.168.1.1 192.168.1.100 --extensions txt --no-backup
        """
    )
    
    parser.add_argument('directory', help='Directory to search for files')
    parser.add_argument('old_ip', help='Old IP address to replace')
    parser.add_argument('new_ip', help='New IP address to use')
    parser.add_argument('--extensions', '-e', nargs='+', default=['.html', '.htm'],
                       help='File extensions to process (default: .html .htm). Can specify with or without dots.')
    parser.add_argument('--no-backup', action='store_true', 
                       help='Do not create backup files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making modifications')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create and run the LinkUpdater
    updater = LinkUpdater(
        directory=args.directory,
        old_ip=args.old_ip,
        new_ip=args.new_ip,
        extensions=args.extensions,
        backup=not args.no_backup,
        dry_run=args.dry_run
    )
    
    updater.run()

if __name__ == "__main__":
    main()
