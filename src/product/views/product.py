from django.views import generic
from django.db.models import Count
from product.models import Variant, Product


class CreateProductView(generic.TemplateView):
    template_name = "products/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        return context


class ListProductView(generic.ListView):
    template_name = "products/list.html"
    model = Product
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ListProductView, self).get_context_data(**kwargs)
        # distinct_list = (
        #     Variant.objects.order_by()
        #     .values("productvariant__variant_title")
        #     .distinct()
        # )
        # print(distinct_list)
        context["variant_list"] = Variant.objects.all().annotate(
            var_count=Count("productvariant__variant_title")
        )
        return context


class SearchResultsListProductView(generic.ListView):
    model = Product
    template_name = "products/list.html"
    paginate_by = 2

    def get_queryset(self):
        title = self.request.GET.get("title")
        variant = self.request.GET.get("variant")
        price_from = self.request.GET.get("price_from")
        price_to = self.request.GET.get("price_to")
        date = self.request.GET.get("date")

        arguments = {}
        if title:
            arguments["title__icontains"] = title
        if variant:
            arguments["productvariant__variant_title"] = variant
        if price_from:
            arguments["productvariantprice__price__gte"] = price_from
        if price_to:
            arguments["productvariantprice__price__lte"] = price_to
        if date:
            arguments["created_at__year"] = date.split("-")[0]
            arguments["created_at__month"] = date.split("-")[1]
            arguments["created_at__day"] = date.split("-")[2]

        return Product.objects.filter(**arguments)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsListProductView, self).get_context_data(**kwargs)
        context["variant_list"] = Variant.objects.all()
        return context
