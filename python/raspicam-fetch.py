#!/usr/bin/python
import logging
logging.basicConfig(level=logging.INFO)
from ftplib import FTP
import os
ftp = FTP('10.0.0.6')
while not ftp.login():
    os.sleep(5)
#ftp.cwd('/media/...')
for d in ftp.nlst():
    if os.path.isdir(d):
        logging.info('Already have directory %s' % d)
        if False:
            continue
    else:
        logging.info('Creating %s' % d)
        os.mkdir(d)
    logging.info('Entering %s' % d)
    os.chdir(d)
    ftp.cwd(d)
    logging.info('Fetching %s directory listing' % d)
    file_exists_count = 0
    for f in ftp.nlst():
        if os.path.isfile(f) and (ftp.size(f) == os.path.getsize(f)):
            if file_exists_count < 3:
                logging.info('File %s already exists and is the correct size' % f)
            elif file_exists_count == 3:
                logging.info('...')
            file_exists_count += 1
            continue
        logging.info('Fetching %s' % f)
        ftp.retrbinary('RETR '+f, open(f, 'wb').write)
    if file_exists_count >= 3:
        logging.info('%d files already existed and were the correct size' % file_exists_count)
    logging.info('Returning to parent directory')
    os.chdir('..')
    ftp.cwd('..')
