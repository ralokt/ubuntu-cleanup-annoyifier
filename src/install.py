

import argparse
import os
import sys
import shutil



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", default = "/opt")
    parser.add_argument("--name", default = "cleanup_annoyifier")
    parser.add_argument("--virtualenv-command", default = "virtualenv")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--remove", action = "store_true")
    group.add_argument("-u", "--user-only", action = "store_true")
    parser.add_argument("--instance-only", action = "store_true")
    parser.add_argument("--force", "-f", action = "store_true")
    return parser.parse_args()


def system_check(*args, **kwargs):
    retcode = os.system(*args, **kwargs)
    if not retcode == 0:
        raise InstallException("system command returned with exit status %d" % retcode)


class InstallException(Exception):
    def __init__(self, reason, *args, **kwargs):
        self.reason = reason

    
def dest_dir(args):
    return os.path.join(args.prefix, args.name)


def this_dir():
    return os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def check_for_installation(args):
    return os.path.exists(dest_dir(args))


def copy_files(args):
    print "copying files..."
    shutil.copytree(this_dir(), dest_dir(args),
                                    ignore = shutil.ignore_patterns("env*"))
    print "done copying files."


def remove_files(args):
    print "removing files..."
    shutil.rmtree(dest_dir(args))
    print "done removing files."
    

def create_user(args):
    print "creating user..."
    os.system("useradd -r %s" % args.name)
    print "done creating user."


def remove_user(args):
    print "removting user..."
    system_check("userdel %s" % args.name)
    print "done removing user."


def _create_virtualenv(args, dest):
    system_check("%s %s" % (args.virtualenv_command, os.path.join(dest, "env")))


def create_virtualenv(args):
    _create_virtualenv(args, dest_dir(args))


def install(args):
    print "installing to", args.prefix
    if check_for_installation(args):
        if args.user_only:
            create_user(args)
            install_cron(args)
            return
        else:
            raise InstallException("already installed at %s" % args.prefix)

    copy_files(args)
    create_virtualenv(args)
    create_user(args)
    install_cron(args)


def remove(args):
    print "removing from", args.prefix
    installed = check_for_installation(args)
    if not installed and not args.force:
        raise InstallException("not installed at %s, nothing to remove" % args.prefix)
    if not args.instance_only:
        uninstall_cron(args)
        remove_user(args)
    if installed:
        remove_files(args)


def create_bootstrap_virtualenv(args):
    _create_virtualenv(args, this_dir())


def install_installation_requirements():
    system_check("pip install -r %s" % os.path.join(this_dir(), "requirements-install.txt"))


def use_bootstrap_virtualenv():
    activate_this = os.path.join(this_dir(), "env", "bin", "activate_this.py")
    execfile(activate_this, dict(__file__ = activate_this))


def handle_bootstrap_virtualenv(args):
    env_exists = os.path.exists(os.path.join(this_dir(), "env"))
    if not env_exists:
        create_bootstrap_virtualenv(args)
    use_bootstrap_virtualenv()
    if not env_exists:
        install_installation_requirements()


def main():
    args = parse_args()
    try:
        handle_bootstrap_virtualenv(args)
        global install_cron, uninstall_cron
        from install_crontab import install_cron, uninstall_cron
        if args.remove:
            remove(args)
        else:
            install(args)
    except InstallException, e:
        print >> sys.stderr, "error: ", e.reason
        sys.exit(1)


if __name__ == "__main__":
    main()

