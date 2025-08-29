from controllers.brand_controller import BrandController
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_get_all_brands():
    controller = BrandController()
    brands = controller.get_all_brands()
    assert isinstance(brands, list)
    assert all('Value' in brand.keys() and 'Label' in brand.keys() for brand in brands)

