#!/usr/bin/env python3
from __future__ import print_function
import os
import sys


try:
	from colorama import Fore, Back, Style
except:
	print("unmet dependency colorama")
	print("install with: pip install colorama")

try:
   input = raw_input
except NameError:
   pass

def debug(whatever):
	pass
	#print(whatever)

def update():
	script_dir = '/'.join(os.path.realpath(__file__).split('/')[0:-1]) + '/'
	getInfo = '&& echo "Getting update information" && git fetch'
	getUpdate = '&& echo "Downloading updates" && git pull'

	os.system( 'cd ' + script_dir + getInfo + getUpdate)

def error_ifAlreadyInit(repo):
	if os.path.exists(repo):
		print( Fore.RED + '\nAlready a context repository' + Style.RESET_ALL )
		print( Fore.YELLOW + 'Hint: ' + Style.RESET_ALL + 'You can list available contexts with:')
		print( Fore.YELLOW + '      ' + sys.argv[0] + ' ls' + Style.RESET_ALL )
		exit(-1)

def error_ifNotInit(repo):
	if not os.path.exists(repo):
		print( Fore.RED + '\nfatal: Not a context repository' + Style.RESET_ALL )
		print( Fore.YELLOW + 'Hint: '  + Style.RESET_ALL + 'You can initialise a repository here with' )
		print( Fore.YELLOW + '      ' + sys.argv[0] + ' init' + Style.RESET_ALL )
		exit(-1)

def error_ifDuplicateContext(repo, contextName):
	if os.path.exists(repo + '/' + contextName):
		print( Fore.RED + '\nA context with the ' + contextName + ' name already exists.' )
		print( Fore.YELLOW + 'Hint: ' + Style.RESET_ALL + 'were you trying to checkout to another context?' )
		print( Fore.YELLOW + '      ' + sys.argv[0] + ' ck' + ' ' + sys.argv[2] + Style.RESET_ALL )
		exit(-1)

def error_ifNoSuchContext(repo, contextName):
	if not os.path.exists(repo + '/' + contextName):
		print( Fore.RED + '\nNo such context exists' + Style.RESET_ALL )
		print( Fore.YELLOW + 'Hint: ' + Style.RESET_ALL + 'were you trying to add another context?' )
		print( Fore.YELLOW + '      ' + Style.RESET_ALL +  sys.argv[0] + ' add' + ' ' + sys.argv[2])
		exit(-1)

def error_ifCurrentContext(repo, contextFile, contextName, message):
	currentContext = ''
	with open(repo + '/' + contextFile, 'r') as fp:
		for line in fp:
			currentContext = line
			break

	if currentContext == contextName:
		print(message)
		exit(-1)
	return False


def show_help():
	print(sys.argv[0] + ' <command> <context>')
	print(' '*(len(sys.argv[0]) + 1) + Fore.YELLOW + 'add: Add a new context.' + Style.RESET_ALL )
	print(' '*(len(sys.argv[0]) + 1) + 'Your current context is freezed and')
	print(' '*(len(sys.argv[0]) + 1) + 'a new blank context is created')
	print(' '*(len(sys.argv[0]) + 1) + "all options: ['add', '--add', '-a', '-add']\n")

	print(' '*(len(sys.argv[0]) + 1) + Fore.YELLOW + 'ck: Checkout to another existing context' + Style.RESET_ALL )
	print(' '*(len(sys.argv[0]) + 1) + 'current context is switched with the target context')
	print(' '*(len(sys.argv[0]) + 1) + "all options: ['checkout', 'ck', '-ck', '--ck', 'cd']")




class Switch: # God has instructed me to use OOP. That's why.
	def __init__(self):
		self.repo = '.contexts'
		self.ignoreFile = '.contextignore'
		self.ignore = [self.repo, self.ignoreFile, '.DS_Store']
		self.current_context_filename = '.current_context_qwsedrfx'
		self.current_context_file = self.repo + '/' + self.current_context_filename

		if os.path.exists(self.ignoreFile): 
			# add files in ignoreFile to list of ignored files
			with open(self.ignoreFile, 'r') as fp:
				self.ignore.extend( [entry for entry in fp if entry[0] != '#'] )


	def createRepo(self): # not a constructor ( __init__ )
		error_ifAlreadyInit(self.repo)
		debug('enter: createRepo()')
		print('\nEnter a context name for the files already in this folder:\n')
		os.system('ls -l')

		name = input('\nContext name: ')

		user_sucks_at_naming = len(name) == 0 or name[0] == '\\'
		while user_sucks_at_naming:
			print('rly?')
			name = input('Context name: ')
			user_sucks_at_naming = len(name) == 0 or name[0] == '\\'			
		
		os.system('mkdir ' + self.repo)

		# update current context
		with open(self.current_context_file, 'w') as fp:
			fp.write(name)


		self.createContext(name)
		print('done.')
		debug('exit: createRepo()')

	def createContext(self, contextName):
		debug('enter: createContext()')
		# dialogue
		error_ifNotInit(self.repo)
		error_ifDuplicateContext(self.repo, contextName)

		os.system('mkdir ' + self.repo + '/' + contextName)
		print("\nCreating new context")
		self.changeContext(contextName)
		debug('exit: createContext()')

	def currentStatus(self):
		error_ifNotInit(self.repo)
		print('\nCurrently in context: ' + Fore.YELLOW + self.__getCurrentContext() + Style.RESET_ALL)
		print('Available contexts:')
		for context in self.__getAvailableContexts():
			print(' ' + Fore.BLUE + context + Style.RESET_ALL , end='')
		print('')

	def changeContext(self, contextName):
		debug("enter: changeContext()")

		error_ifNotInit(self.repo)
		error_ifNoSuchContext(self.repo, contextName)

		self.__freezeContext()
		self.__expandContext(contextName)
		print("Now in context: " + Fore.YELLOW + contextName + Style.RESET_ALL )
		debug("exit: changeContext()")

	def removeContext(self,  contextName):
		debug('enter: removeContext()')

		error_ifNotInit(self.repo)
		error_ifNoSuchContext(self.repo, contextName)

		error_message = Fore.RED + 'Error: Cannot delete an active context.' + Style.RESET_ALL + 
			'\nPlease change to a different context to delete the current one.'
		error_ifCurrentContext(self.repo, self.contextFile, contextName, error_message)

		confirmation = input('Are you sure you want to ' Fore.RED + 'delete' +  Style.RESET_ALL + ' context: ' + Fore.YELLOW + contextName + Style.RESET_ALL + ' [y/N]')
		if confirmation.lower() not in ['y', 'yes']:
			print("Aborted.")
			exit(0)

		os.system("rm -r " + self.repo + '/' + contextName)
		print("Removed context " + contextName)

		debug('exit: removeContext()')

	def renameContext(self, currentName, newName):
		debug('enter: renameContext()')

		error_ifNotInit(self.repo)
		error_ifNoSuchContext(self.repo, currentName)
		error_ifDuplicateContext(self.repo, newName)

		os.system('mv ' + self.repo + '/' + currentName + ' ' + self.repo + '/' + newName)

		if self.__getCurrentContext() == contextName:
			with open(self.current_context_file, 'w') as fp:
				fp.write(newName)
		
		debug('exit: renameContext()')

	def __expandContext(self, contextName):
		debug('enter: __expandContext()')
		error_ifNotInit(self.repo)
		error_ifNoSuchContext(self.repo, contextName)

		# update current context
		with open(self.current_context_file, 'w') as fp:
			fp.write(contextName)

		# Move all files in that context to PWD
		os.system('mv ' + self.repo + '/' + contextName + '/*' + ' ' + './' + ' >/dev/null 2>&1')
		debug('exit: __expandContext()')

	def __getAvailableContexts(self):
		error_ifNotInit(self.repo)

		contexts = os.listdir(self.repo + '/')

		return [ i for i in contexts if i not in [self.current_context_filename]]



	def __getCurrentContext(self):
		error_ifNotInit(self.repo)

		with open(self.current_context_file, 'r') as fp:
			for line in fp: return line

	def __freezeContext(self):
		debug('enter: __freezeContext()')
		error_ifNotInit(self.repo)

		contextName = self.__getCurrentContext()

		files = os.listdir('./')
		
		# move all files that are not in ignore list
		for file in [x for x in files if x not in self.ignore]:
			os.system('mv' + ' "' + file + '" "' + self.repo + '/' + contextName + '/' + file + '"')
		debug('exit: __freezeContext()')

if __name__ == '__main__':
	switch = Switch()

	if len(sys.argv) == 1:
		switch.currentStatus()

	elif len(sys.argv) == 2:
		if sys.argv[1] in ['init']:
			switch.createRepo()
		elif sys.argv[1] in ['ls', 'list', 'show']:
			switch.currentStatus()
		elif sys.argv[1] in ['help', '-h', '--help']:
			show_help()
		elif sys.argv[1] in ['update', '--update']:
			update()
		else:
			print( Fore.RED + '\nunknown command' + Style.RESET_ALL )
			show_help()


	elif len(sys.argv) > 2:
		if sys.argv[1] in ['add', '--add', '-a', '-add']:
			switch.createContext( ''.join(sys.argv[2:]) )
		elif sys.argv[1] in ['checkout', 'ck', '-ck', '--ck', 'cd']:
			print("") # because there is no \n in changeContext() dialogue
			switch.changeContext( ''.join(sys.argv[2:]) )
		elif sys.argv[1] in ['mv', 'rename']:
			switch.renameContext( ''.join(sys.argv[2:]))
		elif sys.argv[1] in ['rm', 'delete', 'remove']:
			switch.removeContext( sys.argv[2], sys.argv[3] )
		else:
			show_help()

	else:
		show_help()

	exit(0)


