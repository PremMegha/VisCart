from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django import forms

from customers.models import Client, Domain


# -----------------------------
# FORM
# -----------------------------
class TenantForm(forms.ModelForm):
    domain = forms.CharField(help_text="example: tenant1.localhost")

    class Meta:
        model = Client
        fields = ["name", "schema_name"]

    def save(self, commit=True):
        tenant = super().save(commit=False)
        if commit:
            tenant.save()
        return tenant


# -----------------------------
# TENANT PAGE (ADMIN ONLY)
# -----------------------------
@staff_member_required
def tenant_page(request):
    tenants = Client.objects.all().order_by("-created_on")

    edit_tenant = None
    form = TenantForm()

    # EDIT MODE
    tenant_id = request.GET.get("edit")
    if tenant_id:
        edit_tenant = get_object_or_404(Client, id=tenant_id)
        primary_domain = edit_tenant.domains.filter(is_primary=True).first()

        form = TenantForm(
            instance=edit_tenant,
            initial={
                "domain": primary_domain.domain if primary_domain else ""
            }
        )

    # SAVE / UPDATE
    if request.method == "POST":
        form = TenantForm(request.POST, instance=edit_tenant)

        if form.is_valid():
            with transaction.atomic():
                tenant = form.save()
                domain_name = form.cleaned_data["domain"]

                # Ensure only one primary domain
                Domain.objects.filter(tenant=tenant).update(is_primary=False)

                Domain.objects.update_or_create(
                    tenant=tenant,
                    domain=domain_name,
                    defaults={"is_primary": True},
                )

            messages.success(request, "Tenant saved successfully ✅")
            return redirect("tenant_page")

    context = {
        "tenants": tenants,
        "form": form,
        "edit_tenant": edit_tenant,
    }

    return render(request, "tenant_page.html", context)


# -----------------------------
# SEND TEST MESSAGE (ADMIN ONLY)
# -----------------------------
@staff_member_required
def send_test_message(request, tenant_id: int):
    tenant = get_object_or_404(Client, id=tenant_id)

    # Placeholder – Telegram logic will be added later
    messages.success(
        request,
        f"Test message triggered for tenant: {tenant.name} ✅"
    )

    return redirect("tenant_page")
