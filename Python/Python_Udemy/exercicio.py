# Exercícios
# Aumente os preços dos produtos a seguir em 10%
# Gere novos_produtos por deep copy (cópia profunda)
import copy

products = [
    {'nome': 'Produto 5', 'preco': 10.00},
    {'nome': 'Produto 1', 'preco': 22.32},
    {'nome': 'Produto 3', 'preco': 10.11},
    {'nome': 'Produto 2', 'preco': 105.87},
    {'nome': 'Produto 4', 'preco': 69.90},
]

new_products = [
    {**product,'preco': round(product['preco'] + product['preco'] * 0.10, 2)}
    for product in copy.deepcopy(products)
    ]


new_products_sorted_by_name = sorted(new_products, key=lambda d: d['nome'], reverse= True)

new_products_sorted_by_price = sorted(new_products, key= lambda d: d['preco'])

print('products sorted by name desc')
for product in new_products_sorted_by_name:
    print(product)

print()

print('products sorted by price asc')

for product in new_products_sorted_by_price:
    print(product)
print()

print('original products')
for product in products:
    print(product)
