from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='OrthoIn3D',
      version='0.1',
      description='To align teeth',
      url='https://github.com/Oliviercros75/ORTHOIN3D/OrthoIn3D',
      author='Olivier Cros',
      author_email='developper@example.com',
      license='MIT',
      packages=['OrthoIn3D', 'OrthoIn3D.segmentation', 'OrthoIn3D.registration'],
      install_requires=[
          'markdown', 'numpy', 'scipy', 'vtk', 'PyQt5',
      ],
      #scripts=['bin/OrthoIn3D_launch'],
      #entry_points = {
      #  'console_scripts': ['OrthoIn3D=OrthoIn3D.command_line:main'],
      #},
      include_package_data=True,
      zip_safe=False)
