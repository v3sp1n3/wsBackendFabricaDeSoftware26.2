from rest_framework.routers import DefaultRouter

from .api_views import AutorViewSet, LivroViewSet


router = DefaultRouter()
router.register("autores", AutorViewSet, basename="autor")
router.register("livros", LivroViewSet, basename="livro")

urlpatterns = router.urls