# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Cosimio(CMakePackage):
    """The CoSimIO is a small library for interprocess communication in CoSimulation contexts. It is designed for exchanging data between different solvers or other software-tools. For performing coupled simulations it is used in combination with the CoSimulationApplication.
    It is implemented as a detached interface. This means that it follows the interface of Kratos but is independent of Kratos, which allows for an easy integration into other codes / solvers
    """

    tags = ["fem", "finite-elements", "hpc", "cosimulation", "coupling"]

    homepage = "https://github.com/KratosMultiphysics/CoSimIO"
    git      = "https://github.com/KratosMultiphysics/CoSimIO.git"
    url      = "https://github.com/KratosMultiphysics/CoSimIO/archive/refs/tags/v4.3.0.tar.gz"

    # TODO: Improve this list
    maintainers("loumalouomega", "philbucher")

    version('master', branch='master')
    version("4.3.0", sha256="108a8c0b042f0eb307984accaecb2b6fc1407afd0bd4b36a4c5a98470a757a66")
    version("4.2.0", sha256="0c7e96d689b016eefd86781c0a55ce2383088cd2612aadc9697a839a0fa8d2b3")
    version("4.1.0", sha256="de02c526835d021c851dbbc1f95e4c929b10d0daccbabc80bcdc7503343678fc")
    version("4.0.0", sha256="12f38d1282b41e1ebc1d2c66d799cb7537840495c98638c698215d390403f221")
    version("3.0.0", sha256="02c902c2b28ae71241c4faf33f3e7a44f363b1d9732c53363cd33ffbbbe81eea")

    variant('mpi', default=False, description='Enable MPI')
    variant('c', default=False, description='Build C API')
    variant('python', default=True, description='Build Python API')
    variant('fortran', default=False, description='Build FORTRAN API')
    variant('testing', default=True, description='Build Testing')

    depends_on('cmake@3.13:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('python', when='+python')

    def cmake_args(self):
        args = [
            self.define('CO_SIM_IO_BUILD_TYPE', 'Release'),
            self.define('CO_SIM_IO_BUILD_MPI', 'OFF'),
            self.define('CO_SIM_IO_BUILD_TESTING', 'ON'),
            self.define('CO_SIM_IO_BUILD_C', 'OFF'),
            self.define('CO_SIM_IO_BUILD_PYTHON', 'ON'),
            self.define('CO_SIM_IO_BUILD_FORTRAN', 'OFF'),
            self.define('CO_SIM_IO_STRICT_COMPILER', 'OFF')
        ]

        if '+mpi' in self.spec:
            args.append(self.define('CO_SIM_IO_BUILD_MPI', 'ON'))

        if '+c' in self.spec:
            args.append(self.define('CO_SIM_IO_BUILD_C', 'ON'))

        if '+python' in self.spec:
            args.append(self.define('CO_SIM_IO_BUILD_PYTHON', 'ON'))

        if '+fortran' in self.spec:
            args.append(self.define('CO_SIM_IO_BUILD_FORTRAN', 'ON'))

        if '+testing' in self.spec:
            args.append(self.define('CO_SIM_IO_BUILD_TESTING', 'ON'))

        return args