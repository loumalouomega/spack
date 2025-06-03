# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
from spack.util.executable import Executable, ProcessError
from spack.util.system import dso_suffix
from spack import *
from spack import tty

class Cosimio(CMakePackage):
    """The CoSimIO is a small library for interprocess communication in CoSimulation contexts.
    It is designed for exchanging data between different solvers or other software-tools.
    For performing coupled simulations it is used in combination with the CoSimulationApplication.
    It is implemented as a detached interface. This means that it follows the interface of
    Kratos but is independent of Kratos, which allows for an easy integration into other codes / solvers.
    """

    tags = ["fem", "finite-elements", "hpc", "cosimulation", "coupling"]

    homepage = "https://github.com/KratosMultiphysics/CoSimIO"
    git      = "https://github.com/KratosMultiphysics/CoSimIO.git"
    url      = "https://github.com/KratosMultiphysics/CoSimIO/archive/refs/tags/v4.3.0.tar.gz"

    maintainers("loumalouomega", "philbucher", "pooyan-dadvand")

    version('master', branch='master')
    version("4.3.1", sha256="9e57839175c06a3d2e8694f95f718707ae465867958ef3bc6b554f775915082b")
    version("4.3.0", sha256="108a8c0b042f0eb307984accaecb2b6fc1407afd0bd4b36a4c5a98470a757a66")
    version("4.2.0", sha256="0c7e96d689b016eefd86781c0a55ce2383088cd2612aadc9697a839a0fa8d2b3")
    version("4.1.0", sha256="de02c526835d021c851dbbc1f95e4c929b10d0daccbabc80bcdc7503343678fc")
    version("4.0.0", sha256="12f38d1282b41e1ebc1d2c66d799cb7537840495c98638c698215d390403f221")
    version("3.0.0", sha256="02c902c2b28ae71241c4faf33f3e7a44f363b1d9732c53363cd33ffbbbe81eea")

    variant('mpi', default='openmpi', description='Enable MPI support', values=('none', 'openmpi', 'intel-mpi'), multi=False)
    variant('c', default=True, description='Build C API')
    variant('python', default=True, description='Build Python API')
    variant('fortran', default=False, description='Build FORTRAN API')
    variant('testing', default=True, description='Build Testing')
    variant('build_type', default='Release', description='CMake build type', values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('strict_compiler', default=False, description='Enable strict compiler flags')
    variant('mpi_communication', default=False, description='Enable MPI communication interface (requires +mpi)')

    depends_on('cmake@3.13:', type='build')
    depends_on('openmpi', when='mpi=openmpi')
    depends_on('intel-mpi', when='mpi=intel-mpi')
    depends_on('python', when='+python')
    depends_on('pybind11', when='+python')
    depends_on('cosimio+c', when='+fortran')

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define('CMAKE_BUILD_TYPE', spec.variants['build_type'].value),
            self.define_from_variant('CO_SIM_IO_STRICT_COMPILER', 'strict_compiler')
        ]

        options = {
            'c':       'CO_SIM_IO_BUILD_C',
            'python':  'CO_SIM_IO_BUILD_PYTHON',
            'fortran': 'CO_SIM_IO_BUILD_FORTRAN',
            'testing': 'CO_SIM_IO_BUILD_TESTING',
        }

        for var, cmake_opt in options.items():
            args.append(self.define_from_variant(cmake_opt, var))

        if spec.variants['mpi'].value == 'none':
            args.append(self.define('CO_SIM_IO_BUILD_MPI', 'OFF'))
        else:
            args.append(self.define('CO_SIM_IO_BUILD_MPI', 'ON'))
            # Add MPI communication variant only if MPI is enabled
            args.append(self.define_from_variant('CO_SIM_IO_BUILD_MPI_COMMUNICATION', 'mpi_communication'))

        return args

    def check(self, spec, prefix):
        if spec.variants['testing'].value:
            with working_dir(self.build_directory):
                self.ctest(parallel=False)

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == 'ldflags':
            if spec.variants['fortran'].value and spec.compiler.name in ['gcc', 'clang', 'apple-clang']:
                if not self.compiler.fc:
                    tty.debug('CoSimIO flag_handler: No Fortran compiler (self.compiler.fc) defined. Cannot determine libgfortran path.')
                    return flags

                fc_exe = Executable(self.compiler.fc)
                libgfortran_path = None

                try:
                    path_shared_cmd_args = ['--print-file-name', 'libgfortran.' + dso_suffix]
                    path_shared = fc_exe(*path_shared_cmd_args, output=str, error=subprocess.PIPE).strip()
                    if os.path.exists(path_shared) and path_shared != ('libgfortran.' + dso_suffix):
                        libgfortran_path = path_shared
                        tty.debug(f"CoSimIO flag_handler: Found shared libgfortran: {libgfortran_path}")
                    else:
                        path_static_cmd_args = ['--print-file-name', 'libgfortran.a']
                        path_static = fc_exe(*path_static_cmd_args, output=str, error=subprocess.PIPE).strip()
                        if os.path.exists(path_static) and path_static != 'libgfortran.a':
                            libgfortran_path = path_static
                            tty.debug(f"CoSimIO flag_handler: Found static libgfortran: {libgfortran_path}")
                        else:
                            # This warning occurs if both shared and static lookups fail to find a valid path.
                            tty.warn(f"CoSimIO flag_handler: Could not find libgfortran using '{self.compiler.fc} --print-file-name'. Fortran linking may rely on default system paths.")
                except ProcessError as e:
                    # This warning occurs if the fc_exe command itself fails.
                    tty.warn(f"CoSimIO flag_handler: Command '{self.compiler.fc} --print-file-name' failed while searching for libgfortran. stderr: {e.stderr.strip() if e.stderr else 'N/A'}")
                except Exception as e:
                    tty.warn(f"CoSimIO flag_handler: An unexpected error occurred while searching for libgfortran: {str(e)}")

                if libgfortran_path and os.path.isfile(libgfortran_path):
                    lib_dir = os.path.dirname(libgfortran_path)
                    tty.debug(f"CoSimIO flag_handler: Adding linker flags: -L{lib_dir} -lgfortran")
                    # Append flags, letting the linker handle potential duplicates.
                    flags.append('-L' + lib_dir)
                    flags.append('-lgfortran')
        return flags
