from models.category import (
    Category,
    CategoryData,
)


async def listing():
    return await CategoryData.from_queryset(Category.all())
