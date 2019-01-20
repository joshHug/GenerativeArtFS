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
    shell('templar', 'compile', html, '-s', md, '-d', out, '-c', 'config2.py')


def compute_grades():
    from grades.get_grades import students
    from csv import DictWriter

    fieldnames = ['Codeword', 'Total Points', 'Attendances', 'Surveys',
                  'Essay 1 Score', 'Essay 1 Peer Reviews',
                  'Essay 2 Score', 'Essay 2 Peer Reviews',
                  'Essay 3 Score', 'Essay 3 Peer Reviews',]

    with open(os.path.join(PUB, 'grades.csv'), 'w') as gradesfile:
        writer = DictWriter(gradesfile, fieldnames=fieldnames)
        writer.writeheader()
        for student in students.values():
            writer.writerow(student.serialize())


def main():
    if not os.path.exists(PUB):
        os.mkdir(PUB)
    templar('page2.html', 'content/about.md', 'about.html')
    templar('page2.html', 'content/readings.md', 'index.html')

    # compute_grades()

    pub_assets = os.path.join(PUB, 'assets')
    if os.path.exists(pub_assets):
        shutil.rmtree(pub_assets)
    shutil.copytree('assets', pub_assets)


if __name__ == '__main__':
    main()
