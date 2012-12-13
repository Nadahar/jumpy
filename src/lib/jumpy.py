import os, os.path, sys, imp, traceback
import __builtin__
from py4j.java_gateway import GatewayClient, JavaGateway
import vmsg

try: pms
except NameError:
	host, port = os.environ['JGATEWAY'].split(':')
	client = GatewayClient(address=host, port=int(port))
	gateway = JavaGateway(client)
	__builtin__.pms = gateway.entry_point
#	__builtin__.pms = JavaGateway(client).entry_point
	__builtin__.pms._addItem = pms.addItem
	__builtin__.pms._addPath = pms.addPath
	__builtin__.pms._setEnv = pms.setEnv
	__builtin__.pms._addPlayer = pms.addPlayer
	# new constants:
	__builtin__.PMS_UNRESOLVED = -64
	__builtin__.PMS_FOLDER = -32
	__builtin__.PMS_ACTION = -2
	__builtin__.PMS_MEDIA = -1
	# constants from net.pms.formats.Format:
	__builtin__.PMS_AUDIO = 1
	__builtin__.PMS_IMAGE = 2
	__builtin__.PMS_VIDEO = 4
	__builtin__.PMS_UNKNOWN = 8
	__builtin__.PMS_PLAYLIST = 16
	__builtin__.PMS_ISO = 32
	__builtin__.PMS_CUSTOM = 64
	# new constants (net.pms.formats.Format|FEED) where FEED=4096
	__builtin__.PMS_AUDIOFEED = 4097
	__builtin__.PMS_IMAGEFEED = 4098
	__builtin__.PMS_VIDEOFEED = 4100
	# util() constants
	__builtin__.PMS_VERSION = 1;
	__builtin__.PMS_HOME = 2;
	__builtin__.PMS_PROFILEDIR = 3;
	__builtin__.PMS_LOGDIR = 4;
	__builtin__.PMS_PLUGINJAR = 5;
	__builtin__.PMS_RESTART = 6;
	__builtin__.PMS_FOLDERNAME = 7;
	__builtin__.PMS_GETPROPERTY = 8;
	__builtin__.PMS_SETPROPERTY = 9;
	__builtin__.PMS_SETPMS = 10;
	__builtin__.PMS_REBOOT = 11;
	__builtin__.PMS_XMBPATH = 12;
	__builtin__.PMS_ICON = 13;
	# constants from net.pms.encoders.Player
	__builtin__.PMS_VIDEO_SIMPLEFILE_PLAYER = 0
	__builtin__.PMS_AUDIO_SIMPLEFILE_PLAYER = 1
	__builtin__.PMS_VIDEO_WEBSTREAM_PLAYER = 2
	__builtin__.PMS_AUDIO_WEBSTREAM_PLAYER = 3
	__builtin__.PMS_MISC_PLAYER = 4
	__builtin__.PMS_NATIVE = "NATIVE"

def flatten(list):
	a = []
	for item in list:
		a.append(item.replace(' , ',' ,, '))
	return '[%s]' % ' , '.join(a)

def pms_addItem(itemtype, name, argv, thumb = None, data = None):
	if type(argv).__name__ == 'list':
		argv = flatten(argv)
	pms._addItem(itemtype, name, argv, thumb, data)

# convenience wrappers
def pms_addFolder(name, cmd, thumb=None):
	pms_addItem(PMS_FOLDER, name, cmd, thumb)

def pms_addAudio(name, cmd, thumb=None):
	pms_addItem(PMS_AUDIO, name, cmd, thumb)

def pms_addImage(name, cmd, thumb=None):
	pms_addItem(PMS_IMAGE, name, cmd, thumb)

def pms_addVideo(name, cmd, thumb=None):
	pms_addItem(PMS_VIDEO, name, cmd, thumb)

def pms_addPlaylist(name, cmd, thumb=None):
	pms_addItem(PMS_PLAYLIST, name, cmd, thumb)

def pms_addISO(name, cmd, thumb=None):
	pms_addItem(PMS_ISO, name, cmd, thumb)

def pms_addAudiofeed(name, cmd, thumb=None):
	pms_addItem(PMS_AUDIOFEED, name, cmd, thumb)

def pms_addImagefeed(name, cmd, thumb=None):
	pms_addItem(PMS_IMAGEFEED, name, cmd, thumb)

def pms_addVideofeed(name, cmd, thumb=None):
	pms_addItem(PMS_VIDEOFEED, name, cmd, thumb)

def pms_addAction(name, cmd, thumb=None, playback=None):
	pms_addItem(PMS_ACTION, name, cmd, thumb, playback)

def pms_addCmd(name, cmd, ok='Success', fail='Failed', thumb=None):
	pms_addItem(PMS_ACTION, name, cmd, thumb, '+CMD : %s : %s' % (ok, fail))

def pms_addConsoleCmd(name, cmd, thumb=None):
	pms_addItem(PMS_ACTION, name, cmd, '#console' if thumb is None else thumb, '+CMDCONSOLE')

def pms_addMedia(name, format, cmd, thumb=None):
	pms_addItem(PMS_MEDIA, name, cmd, thumb, format)

def pms_addPath(path=None):
	pms._addPath(path)

def pms_setPath(path=None): # deprecated
	pms._addPath(path)

def pms_setEnv(name=None, val=None):
	pms._setEnv(name, val)

def pms_util(action, arg1=None, arg2=None):
	return pms.util(action, arg1, arg2)

# 'varargs' version to use with 'String...' on java side:
#def pms_util(action, *args):
#	argarray = JavaGateway(client).new_array(gateway.jvm.java.lang.String, len(args))
#	for i in range(len(args)):
#		argarray[i] = args[i]
#	return pms.util(action, argarray)

def pms_version():
	return pms_util(PMS_VERSION)

def pms_getHome():
	return pms_util(PMS_HOME)

def pms_getProfileDir():
	return pms_util(PMS_PROFILEDIR)

def pms_getLogDir():
	return pms_util(PMS_LOGDIR)

def pms_getPluginJar():
	return pms_util(PMS_PLUGINJAR)

def pms_restart():
	return pms_util(PMS_RESTART)

def pms_reboot():
	return pms_util(PMS_REBOOT)

def pms_getFolderName():
	return pms_util(PMS_FOLDERNAME)

def pms_getXmbPath():
	return pms_util(PMS_XMBPATH)

def pms_getProperty(key):
	return pms_util(PMS_GETPROPERTY, key)

def pms_setProperty(key, val):
	pms_util(PMS_SETPROPERTY, key, val)

def pms_setIcon(fmt, img):
	pms_util(PMS_ICON, fmt, img)

def pms_addPlayer(name, cmd, supported, mediatype=PMS_VIDEO, purpose=PMS_MISC_PLAYER, desc=None, playback=None):
	if type(cmd).__name__ == 'list':
		cmd = flatten(cmd)
	pms._addPlayer(name, cmd, supported, mediatype, purpose, desc, playback)

__builtin__.pms.addFolder = pms_addFolder
__builtin__.pms.addAudio = pms_addAudio
__builtin__.pms.addImage = pms_addImage
__builtin__.pms.addVideo = pms_addVideo
__builtin__.pms.addPlaylist = pms_addPlaylist
__builtin__.pms.addISO = pms_addISO
__builtin__.pms.addAudiofeed = pms_addAudiofeed
__builtin__.pms.addImagefeed = pms_addImagefeed
__builtin__.pms.addVideofeed = pms_addVideofeed
__builtin__.pms.addAction = pms_addAction
__builtin__.pms.addCmd = pms_addCmd
__builtin__.pms.addConsoleCmd = pms_addConsoleCmd
__builtin__.pms.addMedia = pms_addMedia
__builtin__.pms.addItem = pms_addItem
__builtin__.pms.addPath = pms_addPath
__builtin__.pms.setPath = pms_addPath # deprecated
__builtin__.pms.setEnv = pms_setEnv
__builtin__.pms.version = pms_version
__builtin__.pms.getHome = pms_getHome
__builtin__.pms.getProfileDir = pms_getProfileDir
__builtin__.pms.getLogDir = pms_getLogDir
__builtin__.pms.getPluginJar = pms_getPluginJar
__builtin__.pms.restart = pms_restart
__builtin__.pms.reboot = pms_reboot
__builtin__.pms.getFolderName = pms_getFolderName
__builtin__.pms.getXmbPath = pms_getXmbPath
__builtin__.pms.getProperty = pms_getProperty
__builtin__.pms.setProperty = pms_setProperty
__builtin__.pms.setIcon = pms_setIcon
__builtin__.pms.addPlayer = pms_addPlayer

lib = os.path.dirname(os.path.realpath(__file__))
resources = os.path.join(lib, 'resources')

def pms_vmsg(**kwargs):
	if not 'out' in kwargs:
		kwargs['out'] = os.environ['OUTFILE']
	vmsg.vmsg(**kwargs)

def pms_info(msg, seconds=4):
	pms_vmsg(msg=msg, seconds=seconds, fill='white', background='#3465a4', pointsize=20)

def pms_ok(msg, seconds=4):
	pms_vmsg(msg=msg, seconds=seconds, fill='white', background='#3465a4', pointsize=20,
		img='"%s"' % os.path.join(resources,'apply-160.png'), imggrav='north')

def pms_warn(msg, seconds=4):
	pms_vmsg(msg=msg, seconds=seconds, fill='white', background='#3465a4', pointsize=20,
		img='"%s"' % os.path.join(resources,'messagebox_warning-160.png'), imggrav='north')

def pms_err(msg, seconds=4):
	pms_vmsg(msg=msg, seconds=seconds, fill='white', background='#3465a4', pointsize=20,
		img='"%s"' % os.path.join(resources,'button_cancel-160.png'), imggrav='north')

__builtin__.pms.vmsg = pms_vmsg
__builtin__.pms.info = pms_info
__builtin__.pms.ok = pms_ok
__builtin__.pms.warn = pms_warn
__builtin__.pms.err = pms_err

# flush regularly to stay in sync with java output
class flushed(object):
	def __init__(self, s):
		self.s = s
	def write(self, x):
		try: self.s.write(x)
		except UnicodeEncodeError: self.s.write(x.encode('ascii', 'ignore'))
		self.s.flush()
sys.stdout = flushed(sys.stdout)

__builtin__.sys = sys


if __name__ == "__main__" and len(sys.argv) == 1:

	if sys.platform.startswith('win32'):
		try:
			# reset %pms% to short paths so we don't get into trouble with cmd /c
			from ctypes import windll, create_unicode_buffer, sizeof
			buf = create_unicode_buffer(512)
			windll.kernel32.GetShortPathNameW(u'%s' % sys.executable, buf, sizeof(buf))
			py = buf.value
			windll.kernel32.GetShortPathNameW(u'%s' % sys.argv[0], buf, sizeof(buf))
			pms_util(PMS_SETPMS, '%s %s' % (py, buf.value))

			# in Windows 'convert.exe' has a name conflict with a system utility
			# (ntfs partition converter) and python's underlying CreateProcess()
			# invocation doesn't seem to search the current %path% to resolve
			# the executable
			for path in os.environ.get('Path').split(os.path.pathsep):
				convert = os.path.join(path, 'convert.exe')
				if os.path.exists(convert):
					windll.kernel32.GetShortPathNameW(u'%s' % convert, buf, sizeof(buf))
					pms_setEnv('imconvert', buf.value)
					break;
		except:
			traceback.print_exc(file=sys.stderr)

	sys.stderr.write("\npython %s.%s.%s\n" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro))

elif __name__ == "__main__":

	# we're running via system call:
	# interpret the args as a function call and see what happens

	args = []
	for arg in sys.argv[2:]:
		# check if it's a constant
		if arg[0:4] == "PMS_":
			try:
				args.append(str(eval(arg)))
				continue
			except: pass
		# it must be a string
		if sys.argv[1] == 'vmsg':
			args.append(arg)
		else:
			args.append(repr(arg))

	code = 'output=pms_%s(%s)' % (sys.argv[1], ','.join(args))
	sys.stderr.write("calling pms.%s\n" % code[11:])

	try:
		exec code
		if output: print output
	except:
		traceback.print_exc(file=sys.stderr)
		sys.stderr.write("Error: invalid syntax.\n")
		sys.exit(-1)


