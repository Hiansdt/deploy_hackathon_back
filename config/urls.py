
from django.contrib import admin
from django.urls import path, include
from usuario.router import router as usuario_router
from rest_framework.routers import DefaultRouter
from app.views import LivroViewSet, AutorViewSet, GeneroViewSet, CarrinhoViewSet, CarrinhoLivroViewSet, CompraViewSet, CompraLivroViewSet, ComentViewSet, FavoriteViewSet
from django.conf import settings
from django.conf.urls.static import static
from uploader.router import router as uploader_router

router = DefaultRouter()
router.register(r"livros", LivroViewSet)
router.register(r"autores", AutorViewSet)
router.register(r"generos", GeneroViewSet)
router.register(r"carrinhos", CarrinhoViewSet)
router.register(r"carrinhoLivros", CarrinhoLivroViewSet)
router.register(r"compras", CompraViewSet)
router.register(r"compraLivros", CompraLivroViewSet)
router.register(r"coments", ComentViewSet)
router.register(r"favorites", FavoriteViewSet)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from usuario.views import login, register, forget_password, check_token_reset_password, change_password, edit_account, upload_user_foto
from app.views.livro import getBooksOfFilters, searchBooks, getBooksToSlides
from app.views.favorite import getFavoritesOfUser
from app.views.carrinhoLivro import getBookCartOfUser
from app.views.carrinho import get_cart_user
from app.views.coment import getComentsOfBook

urlpatterns = [
    path("api/", include(usuario_router.urls)),
    path("admin/", admin.site.urls),
    path("api/media/", include(uploader_router.urls)),
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/login/', login, name='login'),
    path('api/register/', register, name='register'),
    path('api/forget_password/', forget_password, name='forget_password'),
    path('api/check_token/', check_token_reset_password, name='checkToken'),
    path('api/change_password/', change_password, name='change_password'),
    path('api/edit_account/', edit_account, name='edit_account'),
    path('api/upload_user_foto/', upload_user_foto, name='upload_user_foto'),

    path('api/get_books_of_filters/', getBooksOfFilters, name='getBooksOfFilters'),
    path('api/search_books/', searchBooks, name='searchBooks'),
    path('api/get_favorites_of_user/', getFavoritesOfUser, name='getFavoritesOfUser'),
    path('api/get_cart_user/', get_cart_user, name='get_cart_user'),
    path('api/get_books_cart_of_user/', getBookCartOfUser, name='getBookCartOfUser'),
    path('api/get_coments_of_book/', getComentsOfBook, name='getComentsOfBook'),
    path('api/get_books_to_slides/', getBooksToSlides, name='getBooksToSlides'),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/", include(router.urls)),
] 
urlpatterns += static(settings.MEDIA_ENDPOINT, document_root=settings.MEDIA_ROOT)
