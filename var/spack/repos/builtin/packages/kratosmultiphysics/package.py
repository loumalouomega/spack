# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Kratosmultiphysics(CMakePackage):
    """Kratos Multiphysics (A.K.A Kratos) is a framework for building parallel multi-disciplinary simulation software."""

    tags = ["fem", "finite-elements", "hpc"]

    homepage = "https://github.com/KratosMultiphysics/Kratos"
    git      = "https://github.com/KratosMultiphysics/Kratos.git"
    url      = "https://github.com/KratosMultiphysics/Kratos/archive/refs/tags/9.4.tar.gz"

    # TODO: Improve this list
    maintainers("loumalouomega")

    version('master', branch='master')
    version('9.4', sha256='c78e505b5963e860d1ebe6d970e4469fac9f88aa88b5e2ad69abc0fa8c09f94e')
    version('9.3', sha256='20b04078b2bcfe3f7cc062fe9493538449079f360feba17a39177ab5c3bbfac4')
    version('9.2', sha256='5863e18220f04a5d8066ceea93eb682d93be19188ef9032fd5778331aa1b48f3')
    version('9.1', sha256='2a2415089ffefb288b61e7d9f8dab55564c7b84498c8edfa5677560c90c97b64')

    # TODO: Update this list
    #variant("mpi", default=True, sticky=True, description="Enable MPI parallelism")

    depends_on('boost')
    depends_on('python@3:')
    depends_on('cmake', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('trilinos', when='+trilinos')
    depends_on('parmetis', when='+metis')
    depends_on('mkl', when='+mkl')

    # # Blah, blah, blah
    # with when()

    # TODO: Define lits of applications

    def cmake_args(self):
        args = [
            '-DTRILINOS_LIBRARY_PREFIX=trilinos_', # TODO: Update
            '-DUSE_MPI=ON', # TODO: Update
            '-DINCLUDE_MMG=ON', # TODO: Update
            '-DMMG_ROOT={0}'.format(self.spec['mmg'].prefix),
            '-DCMAKE_UNITY_BUILD={0}'.format(self.spec['cmake'].prefix),
            '-DKRATOS_SHARED_MEMORY_PARALLELIZATION={0}'.format(
                'OpenMP' if self.spec['compilers'].cc == 'gcc' else 'C++11'
            ),
            '-DUSE_EIGEN_MKL=OFF', # TODO: Update
            '-DUSE_TRIANGLE_NONFREE_TPL=ON'# TODO: Update
        ]
        # TODO: USE THIS TO ADD FLAGS
        # return [
        #     self.define("DOLFINX_SKIP_BUILD_TESTS", True),
        #     self.define_from_variant("DOLFINX_ENABLE_SLEPC", "slepc"),
        #     self.define_from_variant("DOLFINX_ENABLE_ADIOS2", "adios2"),
        #     self.define("DOLFINX_UFCX_PYTHON", False),
        #     self.define("DOLFINX_ENABLE_KAHIP", "partitioners=kahip" in self.spec),
        #     self.define("DOLFINX_ENABLE_PARMETIS", "partitioners=parmetis" in self.spec),
        #     self.define("DOLFINX_ENABLE_SCOTCH", "partitioners=scotch" in self.spec),
        # ]

        return args
