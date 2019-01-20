import os
import shutil
import subprocess
import sys

PUB = 'published'

def shell(*args):
    """Call shell command and return its stdout. args are space-separated."""
    cmd = ' '.join(args)
    print('$', cmd)
    stdout = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
    stdout_str = stdout.decode('utf-8').strip()
    print(stdout_str)
    return stdout_str

def templar(html, md, out):
    out = os.path.join(PUB, out)
    shell('templar', 'compile', html, '-s', md, '-m', '-d', out)

def main():
    if not os.path.exists(PUB):
        os.mkdir(PUB)
    templar('page.html', 'content/about.md', 'about.html')
    templar('page.html', 'content/readings.md', 'index.html')

    pub_assets = os.path.join(PUB, 'assets')
    if os.path.exists(pub_assets):
        shutil.rmtree(pub_assets)
    shutil.copytree('assets', pub_assets)

if __name__ == '__main__':
    main()
