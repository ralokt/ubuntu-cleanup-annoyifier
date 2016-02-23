#!/usr/bin/python2

from crontab import CronTab
import sys

CRONTAB_TAG = "ubuntu-cleanup-annoifier"

def install_cron():
    my_cron = CronTab(user=True)
    
#    job  = my_cron.new(command=executable_path(args))
    job = my_cron.new(command="dummy123")
    job.minute.on(0)
    job.hour.on(0)
    job.enable()
    job.set_comment(CRONTAB_TAG)
    
    my_cron.write_to_user( user=True )

def uninstall_cron():
    my_cron = CronTab(user=True)
    my_cron.remove_all(comment=CRONTAB_TAG)
    my_cron.write_to_user( user=True )

if __name__ == "__main__":
    if sys.argv[1] == "i":
        install_cron()
    elif sys.argv[1] == "u":
        uninstall_cron()



