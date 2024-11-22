from main import redis, Product
import time


key = 'order_complete'
group = 'inventory_group'

try:
    redis.xgroup_create(key, group)
    print('Group created.')

except:
    print('Group already exists.')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        for result in results:
            obj = result[1][0][1]
            try:
                product = Product.get(obj['product_id'])
                product.quantity = product.quantity - int(obj['quantity'])
                product.save()
                print('Quantity reduced.')
            except:
                print('Product not received, set refund status.')
                redis.xadd('order_refund', obj, '*')
    except Exception as e:
        print(str(e))
    time.sleep(2)
