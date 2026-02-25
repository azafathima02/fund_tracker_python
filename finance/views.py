from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction
from .forms import TransactionForm
from datetime import datetime
from django.db.models import Sum
from calendar import month_name

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


# ===========================
# MONTH LIST (ONLY MONTH NAMES)
# ===========================
def get_month_list():
    """Return list of months only."""
    return [
        {"value": m, "label": month_name[m]}
        for m in range(1, 13)
    ]


def dashboard(request):
    transactions = Transaction.objects.all().order_by('-date')

    total_income = 0
    total_expense = transactions.aggregate(total=Sum('amount'))['total'] or 0
    balance = 0

    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "form": form,
        "months": get_month_list(),  # only months
        "current_month": request.GET.get("month"),
        "current_year": request.GET.get("year"),
    }

    return render(request, "finance/dashboard.html", context)


def delete_transaction(request, id):
    Transaction.objects.filter(id=id).delete()
    return redirect('dashboard')


# ===============================
# EXPORT ALL TRANSACTIONS PDF
# ===============================
def export_transactions_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'

    pdf = SimpleDocTemplate(response)

    data = [["ID", "Title", "Amount", "Category", "Date"]]

    transactions = Transaction.objects.all().order_by('-date')

    for t in transactions:
        data.append([
            t.id,
            t.title,
            str(t.amount),
            t.category,
            str(t.date),
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    pdf.build([table])
    return response


def add_transaction(request):
    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    return render(request, "finance/add_transaction.html", {"form": form})


# ===============================
# ALL TRANSACTIONS PAGE
# ===============================
def all_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, "finance/transactions.html", {
        "transactions": transactions,
        "months": get_month_list(),  # ONLY MONTHS
    })


# ===============================
# EXPORT MONTHLY PDF
# ===============================
def export_monthly_pdf(request, month, year):

    transactions = Transaction.objects.filter(
        date__month=month,
        date__year=year
    ).order_by('-date')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="monthly_expenses_{month}_{year}.pdf"'
    )

    pdf = SimpleDocTemplate(response)

    data = [[f"{month_name[month]} {year} - Monthly Expenses"]]
    data.append["ID", "Title", "Amount", "Category", "Date"]

    for t in transactions:
        data.append([
            t.id,
            t.title,
            str(t.amount),
            t.category,
            str(t.date),
        ])

    table = Table(data, colWidths=[70, 120, 80, 120, 100])

    table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, 1), colors.lightblue),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 2), (-1, -1), colors.whitesmoke),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    pdf.build([table])
    return response