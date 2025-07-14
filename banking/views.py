from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import RegisterForm,TransactionForm,DateFilterForm
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    transactions = []
    total_balance = 0
    form = DateFilterForm()

    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')

        if request.method == 'POST':
            form = DateFilterForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                transactions = transactions.filter(date__range=(start_date, end_date))

        # Calculate total balance based on user transactions
        total_balance = sum(
            t.amount if t.transaction_type == 'Deposit' else -t.amount
            for t in Transaction.objects.filter(user=request.user)
        )

    context = {
        'transactions': transactions,
        'form': form,
        'total_balance': total_balance
    }
    return render(request, 'home.html', context)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
            #return HttpResponse("registration successful")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def deposit(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'Deposit'
            transaction.save()
            messages.success(request, 'Deposit successful!')
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'deposite.html', {'form': form})

@login_required
def withdraw(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            total_balance = sum(
                t.amount if t.transaction_type == 'Deposit' else -t.amount
                for t in Transaction.objects.filter(user=request.user)
            )
            if amount > total_balance:
                messages.error(request, 'Insufficient balance!')
            else:
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.transaction_type = 'Withdrawal'
                transaction.save()
                messages.success(request, 'Withdrawal successful!')
                return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'withdraw.html', {'form': form})