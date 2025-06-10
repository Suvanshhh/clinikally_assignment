import httpx

async def fetch_product(product_id: int):
    url = f"https://dummyjson.com/products/{product_id}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            return resp.json()
        return None

async def fetch_products(product_ids: list[int]):
    products = []
    for pid in product_ids:
        product = await fetch_product(pid)
        if product:
            products.append(product)
    return products
