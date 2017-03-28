import argparse
import shutil
import os
from udacity_pa import udacity

nanodegree = 'nd889'
projects = ['sudoku']

def submit(args):
  filenames = ['solution.py', 'README']

  if os.path.exists('README'):
    raise RuntimeError("Unable to copy SubmissionReadme to README because README exists already!")

  shutil.copy('SubmissionReadme.md', 'README')
  try:
    udacity.submit(nanodegree, projects[0], filenames, 
                   environment = args.environment,
                   jwt_path = args.jwt_path)
  finally:
    os.unlink('README')
