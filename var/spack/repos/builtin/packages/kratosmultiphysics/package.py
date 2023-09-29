#  |  /           |
#  ' /   __| _` | __|  _ \   __|
#  . \  |   (   | |   (   |\__ `
# _|\_\_|  \__,_|\__|\___/ ____/
#                  Multi-Physics
# Copyright (c) 2016-2023, Pooyan Dadvand, Riccardo Rossi, CIMNE (International Center for Numerical Methods in Engineering)
# All rights reserved. BSD-4 license. See https://github.com/KratosMultiphysics/Kratos/blob/master/kratos/license.txt

from spack import *

class Kratosmultiphysics(CMakePackage):
    """Kratos Multiphysics (A.K.A Kratos) is a framework for building parallel multi-disciplinary simulation software."""

    homepage = "https://github.com/KratosMultiphysics/Kratos"
    git      = "https://github.com/KratosMultiphysics/Kratos.git"
    url      = "https://github.com/KratosMultiphysics/Kratos/archive/refs/tags/9.4.tar.gz"

    version('develop', branch='master')
    version('9.4', sha256='c78e505b5963e860d1ebe6d970e4469fac9f88aa88b5e2ad69abc0fa8c09f94e')
    version('9.3', sha256='20b04078b2bcfe3f7cc062fe9493538449079f360feba17a39177ab5c3bbfac4')
    version('9.2', sha256='5863e18220f04a5d8066ceea93eb682d93be19188ef9032fd5778331aa1b48f3')
    version('9.1', sha256='2a2415089ffefb288b61e7d9f8dab55564c7b84498c8edfa5677560c90c97b64')

    depends_on('cmake', type='build')
    depends_on('mpi')
    depends_on('trilinos')
    depends_on('metis')
    depends_on('mkl')

    def cmake_args(self):
        args = [
            '-DTRILINOS_LIBRARY_PREFIX=trilinos_',
            '-DUSE_MPI=ON',
            '-DINCLUDE_MMG=ON',
            '-DMMG_ROOT={0}'.format(self.spec['mmg'].prefix),
            '-DCMAKE_UNITY_BUILD={0}'.format(self.spec['cmake'].prefix),
            '-DKRATOS_SHARED_MEMORY_PARALLELIZATION={0}'.format(
                'OpenMP' if self.spec['compilers'].cc == 'gcc' else 'C++11'
            ),
            '-DUSE_EIGEN_MKL=OFF',
            '-DUSE_TRIANGLE_NONFREE_TPL=ON'
        ]

        return args
