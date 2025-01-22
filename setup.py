from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
import os

# Set CUDA architecture flags before importing torch
os.environ['TORCH_CUDA_ARCH_LIST'] = '6.0;6.1;7.0;7.5;8.0;8.6;9.0'

# Add CUB version check ignore
os.environ['THRUST_IGNORE_CUB_VERSION_CHECK'] = '1'

os.path.dirname(os.path.abspath(__file__))

setup(
    name="diff_gaussian_rasterization",
    packages=['diff_gaussian_rasterization'],
    ext_modules=[
        CUDAExtension(
            name="diff_gaussian_rasterization._C",
            sources=[
                "cuda_rasterizer/rasterizer_impl.cu",
                "cuda_rasterizer/forward.cu",
                "cuda_rasterizer/backward.cu",
                "rasterize_points.cu",
                "ext.cpp"
            ],
            extra_compile_args={
                "nvcc": [
                    "-I" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "third_party/glm/"),
                    '--allow-unsupported-compiler',
                    # Add architecture flags explicitly
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal
                    '-gencode=arch=compute_61,code=sm_61',  # Pascal (GTX 1070/1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (RTX 2000)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (RTX 3000 early)
                    '-gencode=arch=compute_86,code=sm_86',  # Ampere (RTX 3000 later)
                    '-gencode=arch=compute_90,code=sm_90',  # Ada Lovelace (RTX 4000)
                    "-gencode=arch=compute_90,code=compute_90",  # Future compatibility - added comma here
                    '-D__CUDA_NO_HALF_OPERATORS__',
                    '-D__CUDA_NO_HALF_CONVERSIONS__',
                    '-D__CUDA_NO_HALF2_OPERATORS__',
                    '-DTHRUST_IGNORE_CUB_VERSION_CHECK',
                ],
                "cxx": ["/MD", "/wd4819", "/wd4251", "/wd4244", "/wd4267", "/wd4275", "/wd4018", "/wd4190", "/wd4624", "/wd4067", "/wd4068", "/EHsc"],
            },
            define_macros=[
                ('THRUST_IGNORE_CUB_VERSION_CHECK', None),
            ],
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    }
)