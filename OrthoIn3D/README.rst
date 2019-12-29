OrthoIn3D
--------

To install:

1) open the terminal (cmd.exe)
2) cd path/OrthoIn3D/OrthoIn3D/    # where path is the path where OrthoIn3D is placed
3) run the follwing command: python -m pip install e .
4) cd OrthoIn3D/
5) open setup.py , then in line 8, change the version to a higher number, save the file
6) open __init__.py, at the last line change the version number corresponding to step 5, save the the file
7) then run the following command: python setup.py sdist bdist_wheel



To launch the main script:

1) python main.py # for the original version

or 

1) python minimalGUI.py



To commit the work done on github:

1) git status  (to get the status of the current situation on the project)
2) git add file-name-here-with-extension 
  OU
2) git add --all
3) git commit -m "Editing the README to try out git add/commit"
4) git push   (to push your changes to GitHub)
