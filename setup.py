from setuptools import setup, find_packages

setup(
    name='traffic_video_analytics',
    version='0.1.0',
    description='Traffic Video Analytics Package',
    author='Konstantin VERNER',
    author_email='konst.verner@gmail.com',
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        # Assuming Nomeroff Net does not have specific versioning in its setup.py,
        # you can specify a commit or tag if needed by appending `@commit_hash` or `@tag_name`
        'nomeroff-net @ git+https://github.com/konverner/nomeroff-net.git'
    ],
    dependency_links=[
        # This link will allow pip to find the Git repository when installing your package
        'git+https://github.com/konverner/nomeroff-net.git#egg=nomeroff-net'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)
