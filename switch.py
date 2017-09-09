#!/usr/bin/env python3

import os
import sys

try:
   input = raw_input
except NameError:
   pass

def debug(whatever):
	pass
	#print(whatever)

def error_ifNotInit(repo):
	if not os.path.exists(repo):
		print('\nFatal: This is not a context repository')
		print('You can initialise a repository here with')
		print(sys.argv[0] + ' init')
		exit(-1)

def error_ifDuplicateContext(repo, contextName):
	if os.path.exists(repo + '/' + contextName):
		print('\nA context with that name already exists.')
		print('Hint: were you trying to checkout to another context?')
		print('      ' + sys.argv[0] + ' ck' + ' ' + sys.argv[2])
		exit(-1)

def error_ifNoSuchContext(repo, contextName):
	if not os.path.exists(repo + '/' + contextName):
		print('\nNo such context exists')
		print('Hint: were you trying to add another context?')
		print('      ' + sys.argv[0] + ' add' + ' ' + sys.argv[2])
		exit(-1)

def show_help():
	print(sys.argv[0] + ' <command> <context>')
	print(' '*(len*(sys.argv[0]) + 1) + 'add: Add a new context.')
	print(' '*(len*(sys.argv[0]) + 1) + 'Your current context is freezed and')
	print(' '*(len*(sys.argv[0]) + 1) + 'a new blank context is created\n')

	print(' '*(len*(sys.argv[0]) + 1) + 'ck: Checkout to another existing context')
	print(' '*(len*(sys.argv[0]) + 1) + 'current context is switched with the target context')


class Switch: # God has instructed me to use OOP. That's why.
	def __init__(self):
		self.repo = '.contexts'
		self.ignoreFile = '.contextignore'
		self.ignore = [self.repo, self.ignoreFile, '.DS_Store']
		self.current_context_file = self.repo + '/' + '.current_context_qwsedrfx'

		if os.path.exists(self.ignoreFile): 
			# add files in ignoreFile to list of ignored files
			with open(self.ignoreFile, 'r') as fp:
				self.ignore.extend( [entry for entry in fp if entry[0] != '#'] )


	def createRepo(self): # not a constructor ( __init__ )
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

		self.changeContext(contextName)
		debug('exit: createContext()')

	def currentStatus(self):
		error_ifNotInit(self.repo)
		print('currently in context:')
		print(self.__getCurrentContext())

	def changeContext(self, contextName):
		debug("enter: changeContext()")

		error_ifNotInit(self.repo)
		error_ifNoSuchContext(self.repo, contextName)

		self.__freezeContext()
		self.__expandContext(contextName)
		debug("exit: changeContext()")

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

		elif sys.argv[1] in ['help', '-h', '--help']:
			show_help()
		else:
			print('unknown command')


	elif len(sys.argv) == 3:
		if sys.argv[1] in ['add', '--add', '-a', '-add']:
			switch.createContext( ''.join(sys.argv[2:]) )
		elif sys.argv[1] in ['checkout', 'ck', '-ck', '--ck']:
			switch.changeContext( ''.join(sys.argv[2:]) )
		else:
			show_help()

	else:
		show_help()

	exit(0)


