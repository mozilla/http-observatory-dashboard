from livereload import Server
from subprocess import call


def twiddlethumbs():
    pass

def regen():
    print('Regenerating via "make publish"')
    call(['make', 'publish'])


server = Server()
server.watch('templates/*', regen, delay=1)
server.watch('dist/data/results.json', regen, delay=1)
server.watch('dist/js/*', twiddlethumbs, delay=1)
server.watch('dist/css/*', twiddlethumbs, delay=1)

server.serve(root='dist', port=5501, liveport=35729)
