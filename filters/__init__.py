from loader import dp
from .category_filter import IsCategory

if __name__ == "filters":
    dp.filters_factory.bind(IsCategory)
