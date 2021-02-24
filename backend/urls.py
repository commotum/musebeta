from django.urls import path, re_path
from django.views.generic import TemplateView
from . import api
from . import redirect

urlpatterns = [
    path('images/<str:image>', redirect.images_redirect),
    path('api/get-models', api.get_models),
    path('api/rename-model', api.rename_model),
    path('api/fork-model', api.fork_model),
    path('api/delete-model', api.delete_model),
    path('api/train-model', api.train_model),
    path('api/get-model', api.get_model),
    path('api/generate-model', api.generate_model),
    path('api/read-train-model', api.read_train_model),
    path('api/get-model-steps', api.get_model_samples),
    path('train', TemplateView.as_view(template_name="train.html")),
    path('generate', TemplateView.as_view(template_name="generate.html")),
    path('history', TemplateView.as_view(template_name="history.html")),
    path('', TemplateView.as_view(template_name="index.html")),
]
