from os import listdir
import sys

REPO = ".contexts"
IGNORE_LIST = ".ctxignore"


def exists(name):
	if os.path.exists(name):
		return True
	return False

REPO_EXISTS = exists(REPO)
IGNORE_EXISTS = exists(IGNORE_LIST)

def getCurrentContext():
	# returns name of current context
	name = ''
	with open(REPO + 'current_context_name', 'r') as fp:
		name = fp[0] # will 'with open()' close file if returned from here?
	return name


def getFilesandFolders():
	# Returns a list of files and folders
	# except 'REPO' , 'IGNIGNORE_LIST'
	# and files or folders ignored by
	# IGNORE_LIST

	nodes = listdir('./')

	ignored = [REPO, IGNORE_LIST, '.DS_Store']

	if IGNORE_EXISTS:
		with open(IGNORE_LIST, 'r') as fp:
			ignored.extend( entry for entry in fp if entry[0] != '#' )
			# ignore entries starting with '#'

	return [file for file in nodes if file not ignored]

def freezeCurrentContext():
	# stores current context files
	nodes = getFilesandFolders()
	currentContext = getCurrentContext()
	for node in nodes:
		os.system('mv ' + node + ' ' + REPO + '/' + currentContext + '/' + node)

def expandContext(contextName):
	if not exists(REPO + '/' + contextName):
		print("No such context exists")
		exit(-4)

	# This might fail if a file is already in another context root A
	# But a file with the same name is added in current context B and added
	# to ignore list.

	os.system('mv ' + REPO + '/*' + ' ./')



def addContext(contextName):
	# creates a new context
	# Fails if there are any files other than those
	# ignored

	if exists(REPO + '/' + contextName):
		print("Context with the same name already exists")
		exit(-3)

	freezeCurrentContext()

	with open(REPO + "current_context_name", 'w') as fp:
		fp.write(contextName)


def changeContext(contextName):
	# freezes current context
	# and expands the new context

	if not exists(REPO + '/' + contextName):
		print("No such context exists.")
		print("Hint: Are you trying to create a new context?")
		exit(-4)

	freezeCurrentContext()
	expandContext(contextName)


if __name__ == '__main__':
	if sys.argv[1] in ['ck', 'checkout', '-ck']:
		if len(sys.argv) > 2:
			changeContext(sys.argv[2])
		else:
			print("new context name not specified")
	elif sys.argv[1] in ['add', '-a', '--add']:
		if len(sys.argv) > 2:
			addContext(sys.argv[2])
	elif sys.argv[1] in ['init', '--init']:
		init()
	else:
		print("jandubam")




