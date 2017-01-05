from conans import ConanFile, CMake, tools
from glob import glob
import os


class BisonConan(ConanFile):
    name = 'bison'
    version = '3.0.4'
    license = 'MIT'
    url = 'https://github.com/sztomi/bison-conan.git'
    description = 'This is a tooling package for GNU bison'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake', 'virtualenv'
    requires = 'm4/latest@sztomi/testing'

    def source(self):
        self.tarball_url = 'https://gnu.cu.be/bison/bison-{}.tar.gz'.format(self.version)
        tgz = self.tarball_url.split('/')[-1]
        tools.download(self.tarball_url, tgz)
        tools.untargz(tgz)
        os.unlink(tgz)

    def build(self):
        self.dirname = glob('bison-*')[0]
        os.chdir(self.dirname)
        def run_in_env(cmd):
            activate = '. ../activate.sh && '
            self.run(activate + cmd)
        run_in_env('./configure --prefix={}'.format(self.package_folder))
        self.run('make')
        self.run('make install')

    def package(self):
        pass

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.env_info.path.append(os.path.join(self.package_folder, 'lib'))
        self.env_info.path.append(os.path.join(self.package_folder, 'share'))
        
