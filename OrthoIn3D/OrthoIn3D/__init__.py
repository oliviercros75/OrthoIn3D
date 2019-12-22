from markdown import markdown

from .segmentation.cut import prepare_polydata
from .segmentation.cut import cartesian_product
from .segmentation.cut import get_plane
from .segmentation.cut import cut

from .segmentation.field import add_brush
from .segmentation.field import add_field
from .segmentation.field import mean_vertex
from .segmentation.field import veclen
from .segmentation.field import compute_laplacian
from .segmentation.field import scipy_splu
from .segmentation.field import compute_field
from .segmentation.field import save_stl_old
from .segmentation.field import generate_gengiva
from .segmentation.field import upsample_line
from .segmentation.field import dist_poly2point
from .segmentation.field import save_stl

from .segmentation.viewer import get_cusps
from .segmentation.viewer import show_field
from .segmentation.viewer import select_spline


def show_version():
    print('Version: 0.1')