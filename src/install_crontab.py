#!/usr/bin/python2

from crontab import CronTab
import sys

CRONTAB_TAG = "ubuntu-cleanup-annoyifier"

def install_cron(args):
    my_cron = CronTab(user = args.name)
    
#    job  = my_cron.new(command = executable_path(args))
    job = my_cron.new(command = "dummy123")
    job.minute.on(0)
    job.hour.on(0)
    job.enable()
    job.set_comment(CRONTAB_TAG)
    
    my_cron.write_to_user(user = args.name)

def uninstall_cron(args):
    my_cron = CronTab(user = args.name)
    my_cron.remove_all(comment = CRONTAB_TAG)
    my_cron.write_to_user(user = args.name)




