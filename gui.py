# -*- coding: utf-8 -*-
"""
   Author : Alex B


python ui.py -nopp 3  --proc_params  5 C:\\Users\\alex_\\OneDrive\\Documents\\Gallery\\2 jpg

"""
__version__='1.0.1'
import os, sys, re, time, errno, socket, getpass
import boto
import json
import tempfile
import multiprocessing
from datetime import datetime



home=None

try:
	import __builtin__ as builtins
except:
	import builtins
from pprint import pprint as pp
import traceback
try:
	import cStringIO
except ImportError:
	import io as cStringIO


	
import click
click.disable_unicode_literals_warning = True

e=sys.exit

from collections import OrderedDict
conn_pool={}


home = os.path.dirname(sys.argv[0])
if not home or not home.strip('.'):
	home = os.path.dirname(os.path.abspath(__file__))
#from include.Src import Src
#src=Src()
app_name = os.path.basename(os.path.splitext(__file__)[0])

import logging

#log=logging.getLogger('cli')

wfname=tabname='latest'



workflow=gui=None

SUCCESS = 0

CFG_FILE= 'db.config.json' 



log=None

nopp_opt=sys.argv[1]

if nopp_opt.strip() in ['-nopp']: #'Arguments must start with "Total procedure params count [-nopp]"'
	nopp=str(sys.argv[2])
	assert nopp.isdigit(), '-nopp must be count of procedure params (got "%s").' % nopp
else:
	nopp=None


		
@click.command()
@click.option('-dcf', 	'--db_config_file',   	default = './config/db_config.DEV.json', 	help = 'App config.', 				required=True )
@click.option('-pcf', 	'--proc_config_file',	default = 'config/gui/default.json', 		help = 'Process/procedure config.', required=True )
@click.option('-rte', 	'--runtime_environment',default = 'DEV',	help = 'Runtime.') # DEV/UAT/PROD
@click.option('-nopp', 	'--num_of_proc_params', default = None,		help="ParmsConfig", type=int, 										required=False)
@click.option('-pa', 	'--proc_params', 		nargs=int(nopp) if nopp else 0, help="Process/procedure params", type=str, 				required=False)
@click.option('-mf', 	'--mock_file', 			default = '', 		help="Mock file", 													required=False)
@click.option('-dd', 	'--dump_dir', 			default = './dump', help="Dump dir", 													required=False)
@click.option('-no-mf', '--no-mock_file', 		default = '', 		help="Dummy option", 												required=False)
@click.option('-ld', 	'--lame_duck', 			default = 0,	type=int,  help="Limit IQ streamer output to this row count.", 			required=False)
@click.option('-sk',  	'--skip_rows', 			default = 0,	type=int,  help="Skip number of source rows.", 							required=False)
@click.option('-dop',  	'--degree_of_parallelism', 	default = multiprocessing.cpu_count()/4 ,type=int,  help="DOP for target load.", 	required=False)
@click.option('-sp',  	'--skew_pct', 			default = 50 ,	type=int,  help = "First vs last file skew.", 							required=False)

@click.option('--dump/--no-dump', 				default = False, help="Dump input stream to file.", 									required=False)
@click.option('--tables',	 					default = False, is_flag=True, help="Print tabular debug into stdout.",					required=False)
@click.option('--daemon/--no-daemon', 			default = False, help="Run it as daemon.", 												required=False)
@click.option('-is',  	'--interval_seconds', 	default = 60 ,type=int,  help = "Daemon loop interval in seconds.", 					required=False)

#@log_calls
def main(**kwargs):
	global home, app_name, workflow, gui, conn_pool, tabname
	#pp(kwargs)
	if kwargs['runtime_environment'] in ['DEV']:
		assert 'db_config.PROD.json' not in ''.join(sys.argv), 'Please, set [-rte PROD] for prod env.'

	cfgf=kwargs.get('proc_config_file')
	assert cfgf
	if not  os.path.isfile(cfgf) :
		#log.error('Process config file does not exists:\n%s' % cfgf)
		raise Exception ('Process config file does not exists:\n%s' % cfgf)

	cdir=os.path.dirname(cfgf)
	assert cdir
	assert os.path.isdir(cdir)
	tabdir, wfname = os.path.split(cdir)
	tabfn =os.path.basename(cfgf)
	tabname,_ = os.path.splitext(tabfn)
	wffile= os.path.join('config','workflow','%s.py' % wfname)
	assert os.path.isfile(wffile), 'Workflow file "%s" does not exists in "config/workflow"' % wfname

	start_time = time.time()
	clifn='%s.py' % wfname
	clipath=os.path.join('include','gui', 'main','run.py')
	
	builtins.home=home
	builtins.app_name=app_name
	builtins.workflow=wfname
	builtins.app_init=(gui, conn_pool)
	from include.cli_utils import load_module
	log=logging.getLogger('gui')
	log.info('Host: [%s], User: [%s]' % (socket.gethostname(), getpass.getuser()))
	log.info('Home: [%s]' % home)

	if 1:
		climod=load_module(fn=clipath,app_init=app_init)
		assert hasattr(climod, wfname), 'Gui module "%s" does not have gui class "%s"'  % (clifn, wfname)
		api=getattr(climod, wfname)
		gui=api(**kwargs)
		workflow=load_module(fn=wffile,app_init=(gui, conn_pool))
		workflow.run()


	

if __name__ == "__main__":
	try:
		main()
		sys.exit(SUCCESS)
	except Exception as ex:

		#print str(e)
		err_log = cStringIO.StringIO()
		traceback.print_exc(file=err_log)
		error = err_log.getvalue()

		if not log:
			log=logging.getLogger('gui')
		
		if 1:
			print ('#' * 80)
			print ('ERROR while running gui')
			print ('#' * 80)
			if hasattr(log,'handler') and log.handler:
				log.error(error)
			else:
				print (error)
			print ('#' * 80)
			print ('#' * 80)

		
		if conn_pool:
			
			from include.Db import close_cons
			close_cons(conn_pool)

		try:
			builtins.home=home
			builtins.app_name=app_name
			builtins.workflow=wfname
			builtins.table_name=tabname
			builtins.app_init=(gui, conn_pool)
			from include.cli_utils import  send_crash_email, get_log_for_email, clierr, get_emails
			log=logging.getLogger('gui')
			pp(sys.argv)
			rte= 'PROD' if 'PROD' in sys.argv else 'DEV'
			FROM_EMAIL, TO_EMAIL =	get_emails(env=rte)
	
			err_id=clierr.get_exit_id(e)
			log_recs=get_log_for_email(log.file_name)
				
			subj='ERROR[%s]:%s' % (err_id, ','.join(sys.argv))
			#send_crash_email(sender = FROM_EMAIL, receiver = TO_EMAIL, subject = subj, message = os.linesep.join(log_recs+[txt]))

											
				
		except Exception as ex:
			print(str(ex))
			builtins.home=home
			from include.cli_utils import  clierr
			
			sys.exit(clierr.E_UNHANDLED[1])
				
		sys.exit(clierr.get_exit_id(e) if 'clierr' in vars() else 1)
