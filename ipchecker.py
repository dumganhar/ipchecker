#!/usr/bin/python
# coding=utf-8

import os
import sys
import json
import urllib2
import traceback
from datetime import datetime

def mylog(content):
	cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print('[%s]: %s' % (cur_time, content))

def execute_command(cmd):
	return os.system(cmd)

def submmit_new_ip(ip):
	os.chdir('ip')
	if 0 != execute_command('git diff origin/master --stat --exit-code'):
		mylog('Submmit new IP: ' + ip)
		execute_command('git commit -am "Update IP" > /dev/null')
		execute_command('git push origin master 2> /dev/null')
	os.chdir('..')

def main():
	# mylog('-------------------------------------------')
	# execute_command('whoami')
	cur_dir = os.path.dirname(os.path.realpath(__file__))
	# mylog("main entry, current dir: " + cur_dir)
	os.chdir(cur_dir)

	url = 'http://ipinfo.io'
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'curl/7.51.0')
	resp = urllib2.urlopen(req)

	status = resp.getcode()
	if status == 200:
		# content_type = resp.headers.getheader('content-type')
		# content = resp.info
		content = resp.read()
		# mylog(content)

		resp_obj = json.loads(content)
		ip = resp_obj['ip']

		ip_file = os.path.join(cur_dir, 'ip', 'ip.txt')
		with open(ip_file, "r") as f:
			old_ip = f.read()

		if old_ip != ip:
			mylog('Replace IP from: ' + old_ip + ' to: ' + ip)
			with open(ip_file, "w") as f:
				f.write(ip)
		else:
			mylog('IP is the same, no need to replace!')
		submmit_new_ip(ip)
	# mylog('===========================================')


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		traceback.print_exc()
		sys.exit(1)
