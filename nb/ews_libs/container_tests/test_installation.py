from __future__ import print_function

import importlib


def test():
    for module_name in [
        'numpy',
        'scipy',
        'pandas',
        'statsmodels',
        'pytables',
        'xarray',
        'dask',
        'PIL',
        'sqlalchemy',
        'psycopg2',
        'pymongo',
        'rasterio',
        'shapely',
        'fiona',
        'rasterio',
        'geopandas',
        'mercantile',
        'pyproj',
        'hdf4',
        'hdf5',
        'h5py',
        'netcdf4',
        'matplotlib',
        'seaborn',
        'bokeh',
        'holoviews',
        'geoviews',
        'notebook',
        'flask',
        'marshmallow',
        'theano',
        'tensorflow',
        'keras'
    ]:
        print("Importing {}:".format(module_name))
        module = None
        try:
            module = importlib.import_module(module_name)
        except (ImportError, AttributeError):
            try:
                module = importlib.import_module(module_name)
            except (ImportError, AttributeError):
                print("   Import failed")
        if module is None:
            continue
        try:
            print("   version={}".format(module.__version__))
        except AttributeError:
            print("   No version available")

    print("Importing gdal:")
    from osgeo import gdal
    print("   version={}".format(gdal.__version__))

    print("Importing tvtk:")
    from tvtk.api import tvtk
    from tvtk.common import configure_input

    cs = tvtk.ConeSource()
    cs.resolution = 36
    m = tvtk.PolyDataMapper()
    configure_input(m, cs.output)
    a = tvtk.Actor()
    a.mapper = m
    p = a.property
    p.representation = 'w'
    print("    OK")
