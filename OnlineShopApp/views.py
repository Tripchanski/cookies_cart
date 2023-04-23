from django.shortcuts import render
from .models import Product
# Create your views here.

def show_product(request):
    context = {}
    products = Product.objects.all()
    context['products'] = products
    # Створюємо відповідь клієнту
    response = render(request, 'shop.html', context)  
    # Перевіряємо тип запиту чи є він "POST"
    if request.method == 'POST':
        # Отримуємо дані з cookie під назвою "cart", якщо він нічого не містить в собі, то надаємо йому значення None
        list_product_from_cookie = request.COOKIES.get('cart', None)
        # Отримуєм id продукта з запиту
        product_id = request.POST.get('id')
        # если куки файлов существует
        if list_product_from_cookie != None:
            #добавляем новый куки на основе старого
            response.set_cookie('cart', list_product_from_cookie+" "+product_id)      
        else:
            #создаем новый куки файл
            response.set_cookie('cart', product_id)
    # возвращяем запрос
    return response


def show_cart(request):
    #Сохраняем куки cart в cookies, если в нем ничего нет то становится None
    cookies = request.COOKIES.get('cart', None)
    context = {}
    # если куки не пустые
    if cookies != None:
        #создаем список
        list_products = []
        # раздиляем list_pk через пробел
        list_pk = cookies.split(' ')
        # Перебираем pk_list
        for pk in list_pk:
            # Получаем объекты из класса Product по pk, которые есть в корзине
            product = Product.objects.get(pk = pk)
            # Добавление в список list_products
            list_products.append(product)
    
        context['list_products'] = list_products
    return render(request, 'cart.html', context)